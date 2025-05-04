#ifndef BUZZER_WEB_MODULE_H
#define BUZZER_WEB_MODULE_H

#include <WebServer.h>

class BuzzerWebModule {
public:
  BuzzerWebModule(WebServer& server, int pin);
  void setup();
  void handle();

private:
  WebServer& server;
  int buzzerPin;
  void handleBeep();
};

#endif
