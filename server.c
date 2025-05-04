#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <fcntl.h>
#include <linux/i2c-dev.h>
#include <sys/ioctl.h>
#include <stdint.h>
#include <curl/curl.h>

#define MAX30100_ADDRESS 0x57
#define REG_IR_DATA_H 0x05

int open_i2c_device(const char *device_path) {
    int fd = open(device_path, O_RDWR);
    if (fd < 0) {
        perror("開啟 I2C 裝置失敗");
        exit(1);
    }
    return fd;
}

void set_i2c_slave(int fd, int addr) {
    if (ioctl(fd, I2C_SLAVE, addr) < 0) {
        perror("設定 I2C 地址失敗");
        exit(1);
    }
}

uint16_t read_ir_data(int fd) {
    uint8_t reg = REG_IR_DATA_H;
    if (write(fd, &reg, 1) != 1) {
        perror("寫入資料暫存器失敗");
        return 0;
    }

    uint8_t data[2];
    if (read(fd, data, 2) != 2) {
        perror("讀取 IR 資料失敗");
        return 0;
    }

    return (data[0] << 8) | data[1];
}

void trigger_buzzer() {
    CURL *curl = curl_easy_init();
    if (curl) {
        CURLcode res;
        curl_easy_setopt(curl, CURLOPT_URL, "http://192.168.51.56/buzz");
        res = curl_easy_perform(curl);
        if (res != CURLE_OK) {
            fprintf(stderr, "蜂鳴器觸發失敗: %s\n", curl_easy_strerror(res));
        }
        curl_easy_cleanup(curl);
    }
}

int main() {
    const char *i2c_device = "/dev/i2c-1";
    int fd = open_i2c_device(i2c_device);
    set_i2c_slave(fd, MAX30100_ADDRESS);

    while (1) {
        uint16_t ir = read_ir_data(fd);
        printf("IR 值: %u\n", ir);

        if (ir < 3000) {
            printf("偵測不到手指，觸發蜂鳴器！\n");
            trigger_buzzer();
            sleep(5); // 等待 5 秒避免連續觸發
        }

        sleep(1);
    }

    close(fd);
    return 0;
}
