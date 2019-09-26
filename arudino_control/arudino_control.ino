
#define RELAY1  7
void setup()

{


Serial.begin(9600);
  pinMode(RELAY1, OUTPUT);

}

  void loop()

{


if (Serial.available()) {
        char serialListener = Serial.read();
       //int serialListener = Serial.read();
        Serial.println(serialListener);
        if (serialListener == '0') {
  digitalWrite(RELAY1,0);           // Turns ON Relays 1
   Serial.println("Light ON");
   //delay(5000);                                      // Wait 2 seconds
        }
        else if (serialListener == '1') {
 digitalWrite(RELAY1,1);          // Turns Relay Off
   Serial.println("Light OFF");
   //delay(5000);       
   }
    }




}
