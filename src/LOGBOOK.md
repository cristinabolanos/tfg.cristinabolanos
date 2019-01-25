# ENTORNO DE DESARROLLO EMPLEADO #

SO: Windows 10

IDE: [Arduino 1.8.8](https://www.arduino.cc/en/Main/Software)

ATTiny Core: [ATtinyCore 1.2.2](https://github.com/SpenceKonde/ATTinyCore)

# NOVEDADES EN EL DESARROLLO #

###### 25/01/2019 :: SUBLC ######

1. El core para ATtiny se ha cambiado al proporcionado por [*SpenceKonde en GitHub*](https://github.com/SpenceKonde/ATTinyCore) por la sencillez de la instalación y la correspondencia de versiones con el Arduino IDE.

2. Se ha creado un programa provisional para el gateway para la recogida de datos debido a los problemas de programación del ATtiny84 (se cree que es por diferencias en las frecuencias de reloj usadas entre éste y el arduino duemilanove utilizado para su programación actuando como ISP):
	* La recogida de datos se hace correctamente.
	* Para el almacenamiento de la información recogida se quiere emplear una Raspberry Pi conectada por el puerto serie al arduino y a un lápiz USB. Este último paso esta dando problemas que se esperan solucionar en los próximos días.

###### 20/01/2019 :: SUBLC ######

1. Se ha modificado el core obtenido para ATtiny desde [*Google Code Archive*](https://code.google.com/archive/p/arduino-tiny/downloads/arduino-tiny-0150-0020.zip) por diversos problemas de compilación:
	* La ruta del IDE de Arduino estaba mal en el archivo *platform.txt* -> Cambiada manualmente en el archivo *platform.local.txt* provisionalmente.
	* En el archivo *boards.txt* solo se ha obtenido el core **ATiny84 de 14** pines con un reloj de **8 MHz interno**. Si por cualquier casualidad se necesitara otro core hay que obtenerlo de *Prospective Boards.txt*.