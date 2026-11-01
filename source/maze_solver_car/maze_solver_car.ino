#include "navigator.h"

void setup() {

  Serial.begin(9600);

  delay(1000);

  initNavigator();
}

void loop() {

  navigateMaze();

}