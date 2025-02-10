#include <Arduino.h>
#include <iot_board.h>

// put function declarations here:

const char *devEui = "70B3D57ED006E0FE"; 
const char *appEui = "0000000000000000";
const char *appKey = "CAD61DE30297FF5E48431DDA4C000054";

 char myStr[50];
 char outStr[255];

byte recvStatus = 0;
int count_sent = 0;

boolean runEvery(unsigned long interval)
{
 static unsigned long previousMillis = 0;
 unsigned long currentMillis = millis();
 if (currentMillis - previousMillis >= interval)
 {
   previousMillis = currentMillis;
   return true;
 }
 return false;
}

void onLoRaReceive (sBuffer *Data_Rx, bool isConfirmed, uint8_t fPort){
   String s = String((char *) Data_Rx->Data, HEX);
   Serial.println(s);
}

void setup() {

  IoTBoard::init_serial();
  IoTBoard::init_spi();
  if (IoTBoard::init_lorawan()) {
    lorawan->setDeviceClass(CLASS_A);
    lorawan->setDataRate(SF9BW125);
    // set channel to random
    lorawan->setChannel(MULTI);
    lorawan->setDevEUI(devEui);
    lorawan->setAppEUI(appEui);
    lorawan->setAppKey(appKey);
    lorawan->onMessage(&onLoRaReceive);
    // Join procedure
    bool isJoined;
    do {
      Serial.println("Joining...");
      isJoined = lorawan->join();

      // wait for 10s to try again
      delay(10000);
    } while (!isJoined);
    Serial.println("Joined to network");

  } else {
    Serial.println("Error");
  }
}

void loop() {

  if (runEvery(10000)) {
    sprintf(myStr, "Hello-%d", count_sent);
    lorawan->sendUplink(myStr, strlen(myStr), 1, 2);
    count_sent++;
  }
  lorawan->readData(outStr);
  // Check Lora RX
  lorawan->update();
  delay(1);
}
