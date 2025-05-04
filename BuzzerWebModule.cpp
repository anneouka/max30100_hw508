#include "BuzzerWebModule.h"
#include <Arduino.h>

BuzzerWebModule::BuzzerWebModule(WebServer& srv, int pin)
  : server(srv), buzzerPin(pin) {}

void BuzzerWebModule::setup() {
  pinMode(buzzerPin, OUTPUT);
  digitalWrite(buzzerPin, LOW);
  server.on("/beep", HTTP_ANY, [this]() { handleBeep(); });
}

void BuzzerWebModule::handleBeep() {
  digitalWrite(buzzerPin, HIGH);
  delay(200);
  digitalWrite(buzzerPin, LOW);
  server.send(200, "text/plain", "BEEP OK");
}

void BuzzerWebModule::handle() {
  // 預留未來功能
}
