#include<ESP8266WiFi.h>
#include<SPI.h>
#include "MFRC522.h"
#define RST_PIN D3
#define SS_PIN D4
MFRC522 mfrc522(SS_PIN, RST_PIN);

void setup() 
{
  Serial.begin(9600);
  SPI.begin();
  mfrc522.PCD_Init();
}

void loop() 
{
  if ( !mfrc522.PICC_IsNewCardPresent() )
  {
    delay(50);
    return;
  }

  if ( !mfrc522.PICC_ReadCardSerial() )
  {
    delay(50);
    return;
  }

  Serial.print(F("Card UID: "));
  dump_byte_array(mfrc522.uid.uidByte, mfrc522.uid.size);
  Serial.println();
}

void dump_byte_array(byte *buffer, byte bufferSize) 
{
  for ( byte i = 0; i< bufferSize; i++ )
   {
    Serial.print(buffer[i] < 0x10 ? " 0" : " ");
    Serial.print(buffer[i], HEX);
  }
}
