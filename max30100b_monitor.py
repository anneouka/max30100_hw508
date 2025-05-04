import max30100
import time
import statistics

sensor = max30100.MAX30100()
sensor.enable_spo2()

print("MAX30100 initialized")
print("Reading MAX30100 data...")

bpm_window = []
abnormal_bpm_data = []
abnormal_mode = False
last_upload_time = 0

def simulate_cloud_upload(bpm):
    print(f"[DEBUG] 模擬上傳 BPM={bpm} 到雲端")

def check_abnormal(bpm):
    return bpm < 50 or bpm > 120

try:
    while True:
        sensor.read_sensor()
        ir = sensor.ir
        red = sensor.red

        print(f"IR: {ir}  RED: {red}")

        if sensor.buffer_full:
            bpm = sensor.get_heart_rate()

            if bpm is not None:
                print(f"BPM: {int(bpm)}")
                bpm_window.append(bpm)

                # 保持最近 10 筆的 BPM 資料
                if len(bpm_window) > 10:
                    bpm_window.pop(0)

                avg_bpm = statistics.mean(bpm_window)

                # 判斷異常
                if check_abnormal(bpm):
                    if not abnormal_mode:
                        print("⚠️  進入異常觀察模式...")
                        abnormal_mode = True
                        abnormal_bpm_data = []

                    abnormal_bpm_data.append(bpm)

                    # 每 5 秒模擬上傳
                    if time.time() - last_upload_time > 5:
                        simulate_cloud_upload(int(bpm))
                        last_upload_time = time.time()

                else:
                    if abnormal_mode and len(abnormal_bpm_data) > 0:
                        print("🚨 心跳異常確認！")
                        print(f"最小 BPM: {int(min(abnormal_bpm_data))}")
                        print(f"最大 BPM: {int(max(abnormal_bpm_data))}")
                        print(f"平均 BPM: {int(statistics.mean(abnormal_bpm_data))}")
                        abnormal_mode = False
                        abnormal_bpm_data = []

            else:
                print("無法計算 BPM，等待更多數據...")

        else:
            print("請將手指放在感測器上")

        time.sleep(1)

except KeyboardInterrupt:
    print("Exiting...")
