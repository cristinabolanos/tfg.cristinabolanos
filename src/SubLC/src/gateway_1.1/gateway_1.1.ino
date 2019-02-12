/*
 * Author: Cristina Bolaños Peño
 * SubLC_Gateway v1.0.0
 * 
 * Visit https://bitbucket.org/cristibp11/tfg.cristinabolanos/src/default/
 */

#include <DallasTemperature.h>
#include <DHT.h>
#include <filter.h>
#include <OneWire.h>
#include <OpenGarden.h>
#include <Ports.h>
#include <RemoteReceiver.h>
#include <RemoteSwitch.h>
#include <RF12.h>
#include <RTClib.h>
#include <LowPower.h>

DateTime now;
unsigned long start, current;
long interval = 5000000; //milliseconds
String commands = "";
bool newCommand = false;
int RESET = 12;

void convertTime(uint8_t value){
  if(value<10){
    switch (value){
    case 0:Serial.print("00");break;
    case 1:Serial.print("01");break;
    case 2:Serial.print("02");break;
    case 3:Serial.print("03");break;
    case 4:Serial.print("04");break;
    case 5:Serial.print("05");break;
    case 6:Serial.print("06");break;
    case 7:Serial.print("07");break;
    case 8:Serial.print("08");break;
    case 9:Serial.print("09");break;
    }
  }
  else
    Serial.print(value, DEC);
}

void printData () {
  now = OpenGarden.getTime();
  OpenGarden.printTime(now);
  Serial.println();
  // Print day info
  Serial.print(now.day(), DEC);
  Serial.print("/");
  Serial.print(now.month(), DEC);
  Serial.print("/");
  Serial.print(now.year(), DEC);

  Serial.print(",");
  // Print hour info
  convertTime(now.hour());
  Serial.print(":");
  convertTime(now.minute());
  Serial.print(":");
  convertTime(now.second());
  
  Serial.print(",");
  // Print luminosity (%)
  Serial.print(OpenGarden.readLuminosity());
  
  Serial.print(',');
  // Print temperature (ºC)
  Serial.print(OpenGarden.readAirTemperature());
  
  Serial.print(',');
  // Print humidity (%RH)
  Serial.print(OpenGarden.readAirHumidity());
  
  Serial.print(',');
  // Print soil moisture (?)
  Serial.println(OpenGarden.readSoilMoisture());
}

void setup() {
    Serial.begin(9600);
    OpenGarden.initSensors();
    OpenGarden.initRTC();
    OpenGarden.setTime();
    start = millis();
}


void loop() {
  current = millis();
  
  OpenGarden.sensorPowerON();
  delay(500);
  printData();
  OpenGarden.sensorPowerOFF();

  while (!newCommand && (current - start > interval))
  if (newCommand){
    
  }
}

void serialEvent(){
    
}

void(* resetFunc)(void) = 0;
