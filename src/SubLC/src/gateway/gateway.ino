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

DateTime now;

void setup() {
    Serial.begin(9600);
    OpenGarden.initSensors();
    OpenGarden.initRTC();
    OpenGarden.setTime();
}


void loop() {
    OpenGarden.sensorPowerON();
    delay(500);

    // Get time and print time of the day
    now = OpenGarden.getTime();
    Serial.print(now.hour(), DEC);
    Serial.print(':');
    Serial.print(now.minute(), DEC);
    Serial.print(':');
    Serial.print(now.second(), DEC);
    Serial.print(',');
    
    // Read and print results as < luminosity(%),humidity(%RH),temperature(ºC),soilmoisture(values with out calibration) >
    Serial.print(OpenGarden.readLuminosity());
    Serial.print(',');
    Serial.print(OpenGarden.readAirTemperature());
    Serial.print(',');
    Serial.print(OpenGarden.readAirHumidity());
    Serial.print(',');
    Serial.println(OpenGarden.readSoilMoisture());
    
    OpenGarden.sensorPowerOFF();  //Turns off the sensor power supply
    delay(2000);   //Wait 2 seconds
    //delay(600000);   //Wait 10 minutes
}
