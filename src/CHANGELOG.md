# Changelog
Todos los cambios notables de este subproyecto serán documentados en este fichero.

El formato está basado en [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), y a su vez se adhiere al [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]
### 25/02/2019
1. El ATtiny84 se ha podido programar con una versión inicial del programa nodo satisfactoriamente gracias a los siguientes cambios:
	* Modificación del archivo $HOME/.arduino15/packages/ATtinyCore/hardware/avr/1.2.3/programers.txt en lo que corresponde a la sección del programador Arduino as ISP cambiando *arduino* por *stk500v1* en:
	```c
	arduinoasisp.protocol=stk500v1
	arduinoasisp.program.protocol=stk500v1
	```

### 12/02/2019

1. Modificación de la idea del subsistema SubI contemplada desde desde el inicio del 02/2019 de la forma:
	* Realización del desarrollo y despliegue con [Docker](https://www.docker.com/) por: uso de bajos recursos y empleo del mismo en el entorno cloud actualmente empleado (IMBCloud).
	* Puede contemplarse el uso de otras herramientas de automatización y/o pruebas y su combinación en el futuro tales como: Ansible, Chef, Vagrant, Virtualbox, etc. no es trivial por el momento.
	* Se elaborará un esquema con la estructura del subsistema en los próximos días.

### 29/01/2019

1. Se ha diseñado un programa para recolectar los datos que el Arduino envía por el puerto Serie. Se almacena en el propio dispositivo de forma provisional ya que al querer almacenarlo en un USB seguía dando problemas de formato. Se prevee dejar el sistema recogiendo datos de una planta desde hoy a las 17:00 hasta al día siguiente esperando que no haya problemas.

### 25/01/2019

1. El core para ATtiny se ha cambiado al proporcionado por [*SpenceKonde en GitHub*](https://github.com/SpenceKonde/ATTinyCore) por la sencillez de la instalación y la correspondencia de versiones con el Arduino IDE.

2. Se ha creado un programa provisional para el gateway para la recogida de datos debido a los problemas de programación del ATtiny84 (se cree que es por diferencias en las frecuencias de reloj usadas entre éste y el arduino duemilanove utilizado para su programación actuando como ISP):
	* La recogida de datos se hace correctamente.
	* Para el almacenamiento de la información recogida se quiere emplear una Raspberry Pi conectada por el puerto serie al arduino y a un lápiz USB. Este último paso esta dando problemas que se esperan solucionar en los próximos días.

### 20/01/2019

1. Se ha modificado el core obtenido para ATtiny desde [*Google Code Archive*](https://code.google.com/archive/p/arduino-tiny/downloads/arduino-tiny-0150-0020.zip) por diversos problemas de compilación:
	* La ruta del IDE de Arduino estaba mal en el archivo *platform.txt* -> Cambiada manualmente en el archivo *platform.local.txt* provisionalmente.
	* En el archivo *boards.txt* solo se ha obtenido el core **ATiny84 de 14** pines con un reloj de **8 MHz interno**. Si por cualquier casualidad se necesitara otro core hay que obtenerlo de *Prospective Boards.txt*.
