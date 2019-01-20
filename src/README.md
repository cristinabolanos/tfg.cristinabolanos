# ENTORNO DE DESARROLLO EMPLEADO #

SO: Windows 10
IDE: [Arduino 1.8.8](https://www.arduino.cc/en/Main/Software)

# NOVEDADES EN EL DESARROLLO #

###### 20/01/2019 :: SUBLC ######
* Se ha modificado el core obtenido para ATtiny desde [*Google Code Archive*](https://code.google.com/archive/p/arduino-tiny/downloads/arduino-tiny-0150-0020.zip) por diversos problemas de compilación:
	- La ruta del IDE de Arduino estaba mal en el archivo *platform.txt* -> Cambiada manualmente en el archivo *platform.local.txt* provisionalmente.
	- En el archivo *boards.txt* solo se ha obtenido el core **ATiny84 de 14** pines con un reloj de **8 MHz interno**. Si por cualquier casualidad se necesitara otro core hay que obtenerlo de *Prospective Boards.txt*.