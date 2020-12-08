#include <ESP8266WiFi.h>                                            
#include <FirebaseArduino.h>                                             
#define FIREBASE_HOST "RFID_SCAN.firebaseio.com"                         
#define FIREBASE_AUTH "06dEpqanFgadms466dvqAwnQLwLI"                   
#define WIFI_SSID "NUS_GUEST"                                           
#define WIFI_PASSWORD "789126"                                    

String fireStatus = "";                                                     
int id = D3;                                                                
void setup()
{
  Serial.begin(9600);
  delay(1000);
  pinMode(LED_BUILTIN, OUTPUT);      
  pinMode(led, OUTPUT);                 
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);                                     
  Serial.print("Connecting to ");
  Serial.print(WIFI_SSID);
  while (WiFi.status() != WL_CONNECTED) 
  {
    Serial.print(".");
    delay(500);
  }
  Serial.println();
  Serial.print("Connected to ");
  Serial.println(WIFI_SSID);
  Serial.print("IP Address is : ");
  Serial.println(WiFi.localIP());                                                      
  Firebase.begin(FIREBASE_HOST, FIREBASE_AUTH);                                       
  Firebase.setString("RFID_SCAN", "OFF");                                         
}

void loop() {
  fireStatus = Firebase.getString("RFID_STATUS");                                      
  if (fireStatus == "ON") 
  {                                                          
    Serial.println("SCAN INITIATED");                         
    digitalWrite(LED_BUILTIN, LOW);                                                  
    digitalWrite(led, HIGH);                                                          
  } 
  else if (fireStatus == "OFF") 
  {                                                  
    Serial.println("ID_AUTHENTICATED");
    digitalWrite(LED_BUILTIN, HIGH);                                               
    digitalWrite(led, LOW);                                                        
  }
  else 
  {
    Serial.println("Wrong Credential! RESCAN ");
  }
}
