/*

    Serial communication code for Arduino Uno.

*/

void setup() {
    Serial.begin(9600);
    // Serial.begin(115200);
}


void loop() {
  if (Serial.available() > 0) {
    String data = Serial.readStringUntil('\n'); //Read until end of line token
    Serial.print("You sent me: ");  // Send it using utf-8 encoding
    Serial.println(data);
  }
}