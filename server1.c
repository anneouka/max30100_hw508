#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <fcntl.h>
#include <termios.h>
#include <string.h>
#include <time.h>
#include <errno.h>

// 假設你有以下這些函數
extern int read_max30100(int *ir_value, int *red_value, int *bpm);

int main() {
    FILE *csv_file = fopen("data_log.csv", "a");
    if (csv_file == NULL) {
        perror("Failed to open CSV file");
        return 1;
    }

    // 如果檔案剛建立，寫入標題（簡單判斷檔案大小）
    fseek(csv_file, 0, SEEK_END);
    if (ftell(csv_file) == 0) {
        fprintf(csv_file, "Timestamp,IR,RED,BPM\n");
        fflush(csv_file);
    }

    printf("開始讀取 MAX30100 資料並記錄到 CSV + ThingSpeak...\n");

    while (1) {
        int ir_value = 0, red_value = 0, bpm = 0;

        // 讀取 MAX30100 數據
        if (read_max30100(&ir_value, &red_value, &bpm) != 0) {
            fprintf(stderr, "讀取 MAX30100 失敗\n");
            sleep(1);
            continue;
        }

        // 顯示資料
        printf("IR: %d  RED: %d\n", ir_value, red_value);
        printf("BPM: %d\n", bpm);

        // 寫入 CSV
        time_t now = time(NULL);
        fprintf(csv_file, "%ld,%d,%d,%d\n", now, ir_value, red_value, bpm);
        fflush(csv_file);

        // 上傳到 ThingSpeak（替換 YOUR_API_KEY）
        char cmd[512];
        snprintf(cmd, sizeof(cmd),
                 "curl -s -X GET \"https://api.thingspeak.com/update?api_key=YOUR_API_KEY&field1=%d&field2=%d&field3=%d\"",
                 ir_value, red_value, bpm);
        system(cmd);

        sleep(1); // 每秒回圈
    }

    fclose(csv_file);
    return 0;
}
