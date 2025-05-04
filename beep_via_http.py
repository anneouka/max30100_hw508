import requests

# 替換為 Pico 的 IP 地址，例如：192.168.1.123
pico_ip = "192.168.1.123"
url = f"http://{pico_ip}/beep"

try:
    response = requests.post(url)
    print(f"回應：{response.text}")
except Exception as e:
    print(f"發送失敗：{e}")

