/*
 * Autora: Cristina Bolaños Peño
 * Compilador: C++
 * Pasos:
 *  1) Seguir los pasos de: http://highlowtech.org/?p=1695 y http://highlowtech.org/?p=1706
 *  2) (Si primera vez programando ATtiny) Herramientas -> Quemar Bootloader.
 *  3) Instalar librería de https://www.cooking-hacks.com/media/cooking/images/documentation/open_garden/Open_Garden_Libraries_V2.4.zip como ZIP.
 *  4) Problema con Ports.h de OpenGardenNode -> http://forum.arduino.cc/index.php?topic=554398.0 -> https://jeelabs.net/boards/6/topics/307 -> https://github.com/arduino/Arduino/wiki/Arduino-IDE-1.5-3rd-party-Hardware-specification
 */

 /*
  * Reads up all environment information and sends it to our gateway:
  *  - Luminosity (
      Light resistance : ~1k Ohm
      Dark resistance : ~10k Ohm
      Max voltage : 150V
      Max power: 100mW
    )
    - 
  *
  *

#include <DHT22.h>
#include <OpenGardenNode.h>
#include <Ports.h>
#include <RF12.h>
  */

Payload nodePacket;
 
void setup() {
    //Initialize the transceiver
    OpenGardenNode.initRF(1); //Write here the number for your node ID  (1, 2 or 3)
    OpenGardenNode.initSensors(); //Initialize sensors power  
}

void loop() {
    OpenGardenNode.sensorPowerON();  //Turns on the sensor power supply
    OpenGardenNode.readSensors();    //Read all node sensors
    OpenGardenNode.sensorPowerOFF(); //Turns off the sensor power supply
    
    OpenGardenNode.sendPackage();  // Send data via RF asking for ACK
    OpenGardenNode.nodeWait(60);   //Enter low power mode for 60 seconds (max: 60 seconds)
}
