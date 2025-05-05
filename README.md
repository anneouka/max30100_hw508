# max30100_hw508
# MAX30100 Buzzer Module (Arduino / Pico W)

這個專案使用 Raspberry Pi Pico W 建立一個蜂鳴器模組，支援透過 Wi-Fi 網頁 API 控制蜂鳴器發出「嗶」聲。設計目的是搭配 MAX30100 血氧偵測器，當心率異常時由 Raspberry Pi 發送指令，觸發警示。

## 硬體需求

- Raspberry Pi Pico W
- 主動蜂鳴器 x1
- 杜邦線 x 若干
- Wi-Fi 網路（需與 Raspberry Pi 在同一網段）

## 接線方式

| Pico W 腳位 | 元件        |
|-------------|-------------|
| GPIO 15     | 蜂鳴器 +     |
| GND         | 蜂鳴器 -     |

## Wi-Fi 設定


在 `max30100_main.ino` 中修改以下欄位，設定你家中的 Wi-Fi：

```cpp
const char* ssid = "iSpan-R201";
const char* password = "66316588";
