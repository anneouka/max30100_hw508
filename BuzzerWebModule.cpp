#include <WiFi.h>
#include <WebServer.h>
#include "BuzzerWebModule.h"

const char* ssid = "iSpan-R201";
const char* password = "66316588";

WebServer server(80);
BuzzerWebModule buzzer(server, 15);  // 使用 GP15

void setup() {
  Serial.begin(115200);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("");
  Serial.println("WiFi connected.");
  Serial.println(WiFi.localIP());

  buzzer.setup();
  server.begin();
}

void loop() {
  server.handleClient();
  buzzer.handle();  // 目前沒事做，預留擴充
}
