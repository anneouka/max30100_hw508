import smbus2 as smbus
import time
import RPi.GPIO as GPIO
import serial
import requests

UPLOAD_INTERVAL = 10  # 單位：秒
last_upload_time = time.time()

I2C_BUS = 1
MAX30100_ADDRESS = 0x57

# MAX30100 Registers
REG_MODE_CONFIGURATION = 0x06
REG_SPO2_CONFIGURATION = 0x07
REG_LED_CONFIGURATION = 0x09

# Buzzer pin
BUZZER_PIN = 17

# 心跳偵測參數
PEAK_THRESHOLD = 30000
MIN_PEAK_INTERVAL = 0.4

bus = smbus.SMBus(I2C_BUS)
ser = serial.Serial("/dev/serial0", 115200, timeout=1)
time.sleep(2)

def read_sensor_data():
    data = bus.read_i2c_block_data(MAX30100_ADDRESS, 0x05, 4)
    ir_value = (data[0] << 8) | data[1]
    red_value = (data[2] << 8) | data[3]
    return ir_value, red_value

def init_max30100():
    bus.write_byte_data(MAX30100_ADDRESS, REG_MODE_CONFIGURATION, 0x40)
    time.sleep(0.1)
    bus.write_byte_data(MAX30100_ADDRESS, REG_MODE_CONFIGURATION, 0x03)
    bus.write_byte_data(MAX30100_ADDRESS, REG_SPO2_CONFIGURATION, 0x27)
    bus.write_byte_data(MAX30100_ADDRESS, REG_LED_CONFIGURATION, 0x4F)
    print("MAX30100 initialized")

def init_buzzer():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(BUZZER_PIN, GPIO.OUT)
    GPIO.output(BUZZER_PIN, GPIO.LOW)

def set_buzzer(on):
    GPIO.output(BUZZER_PIN, GPIO.HIGH if on else GPIO.LOW)

def estimate_bpm(ir_history, timestamps):
    peaks = []
    for i in range(1, len(ir_history) - 1):
        if ir_history[i] > PEAK_THRESHOLD and ir_history[i] > ir_history[i - 1] and ir_history[i] > ir_history[i + 1]:
            if len(peaks) == 0 or (timestamps[i] - timestamps[peaks[-1]] > MIN_PEAK_INTERVAL):
                peaks.append(i)

    if len(peaks) >= 2:
        intervals = [timestamps[peaks[i]] - timestamps[peaks[i - 1]] for i in range(1, len(peaks))]
        avg_interval = sum(intervals) / len(intervals)
        bpm = 60 / avg_interval
        return int(bpm)
    else:
        return None

# 🔧 這是你要自己實作的資料庫上傳函式：
def upload_to_cloud(bpm):
    # TODO: 這裡根據你的資料庫格式實作，比如 HTTP POST、Firebase、Supabase、MySQL 等
    print(f"[DEBUG] 模擬上傳 BPM={bpm} 到雲端")

def main():
    global last_upload_time

    init_max30100()
    init_buzzer()

    print("Reading MAX30100 data...")

    ir_history = []
    timestamps = []
    history_size = 50

    try:
        while True:
            ir, red = read_sensor_data()
            now = time.time()

            if ir < 10000:
                print("請將手指放在感測器上")
                requests.post("http://192.168.51.152/beep")
                set_buzzer(True)
                ir_history.clear()
                timestamps.clear()
                time.sleep(1)
                continue

            print(f"IR: {ir}  RED: {red}")

            ir_history.append(ir)
            timestamps.append(now)

            if len(ir_history) > history_size:
                ir_history.pop(0)
                timestamps.pop(0)

            bpm = estimate_bpm(ir_history, timestamps)
            if bpm:
                print(f"BPM: {bpm}")
                if bpm < 50 or bpm > 120:
                    print("⚠️ 心跳異常！觸發蜂鳴器")
                    requests.post("http://192.168.51.152/beep")
                    set_buzzer(True)
                else:
                    set_buzzer(False)

                # ✅ 正確縮排：只在有 BPM 結果時上傳
                if time.time() - last_upload_time >= UPLOAD_INTERVAL:
                    upload_to_cloud(bpm)
                    last_upload_time = time.time()
            else:
                print("無法計算 BPM，等待更多數據...")

            time.sleep(0.1)

    except KeyboardInterrupt:
        print("Exiting...")
    finally:
        GPIO.cleanup()

if __name__ == "__main__":
    main()
