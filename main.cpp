#include <Arduino.h>
#include <WiFi.h>
#include <ArduinoJson.h>
#include <HTTPClient.h>
#include "HX711.h"

const char *ssid = "mega";
const char *password = "jerkovac";

const int DOUT=22;
const int SCK_PIN=18;
const int tipkalo=13;

const long LOADCELL_OFFSET = 50682624;
const long LOADCELL_DIVIDER = 5895655;

int tipkalo_pom,pomocna;
HX711 scale;


StaticJsonDocument <200> doc;



WiFiServer server(80);
WiFiClient client;
long sila;
int id=0;
float sila_raw=0;
float prava_sila;


void setup()
{
  pinMode(tipkalo,INPUT_PULLDOWN);
  Serial.begin(9600);
  Serial.println("Initializing the scale");
  scale.begin(DOUT,SCK_PIN);
  scale.set_scale();
  
  scale.tare();
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED)
  {
    delay(250);
    Serial.print(".");
  }
  Serial.println("");

  Serial.println("IP adresa: ");
  Serial.println(WiFi.localIP());

  server.begin();
}
  

 

void loop()
{ 

  tipkalo_pom=digitalRead(tipkalo);
  pomocna=tipkalo_pom;
   if (pomocna==1){
    id=1;
   }

   else if(pomocna==0) {
    id=2;
   }
  

    
  for(int i=0;i<5;i++){
    sila_raw=sila_raw+(scale.get_units(10));

    delay(200);
  }
  
  sila_raw=sila_raw/5;
  prava_sila=map(sila_raw,5000,9000,0,70);
  
   doc["sila"]=prava_sila;
   doc["id"]=id;
   
   

   String json;
   String jsonPretty;

   serializeJson(doc,json);
    delay(1000);

 
    Serial.println(json);
   
   const char *serverName= "http://192.168.91.136/sila";
    HTTPClient http;
    http.begin(serverName);
  
  
    http.addHeader("Content-Type","application/json");
    
    
    int httpResponseCode =http.POST(json);
    delay(2000);
    
    

    Serial.println(httpResponseCode);
    Serial.println(http.getString());
    http.end();

    

   }

