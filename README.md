# Título:
### TFG-FacialRecognition

## Universidad de Burgos

# Autor: 
#### Víctor de Castro Hurtado

# Tutor: 
#### César Represa Pérez

# Índice:
  - Descripción
  - Introducción
  - Requisitos
  - Instrucciones

## Descripción:

Se pretende diseñar un sistema de identificación de personas a través de un programa de reconocimiento facial con rostros previamente incluidos en una base de datos. El sistema de desarrollará en Python y utilizando técnicas de Machine Learning.

## Introducción:

El repositorio de Github donde se encuentran los ficheros del TFG de reconocimiento facial basado en machine-learning se puede encontrar en el siguiente [enlace](https://github.com/victorcas04/TFG-FacialRecognition).

El TFG consiste en una aplicación que, dadas dos **imágenes**, una obtenida en el **momento de ejecución**, ya sea mediante **fichero** (accediendo a la foto que tengamos almacenada en nuestro equipo), o mediante una captura que realicemos con nuestra **cámara**,  y la otra alojada localmente en una **base de datos**: sea capaz de distinguir si en ambas imágenes se encuentra la misma persona utilizando técnicas de **machine-learning**.
A la hora de comparar ambas imágenes, si la persona que se pone delante de la cámara no estaba registrada en la base de datos, aparecerá **la persona** que esté registrada **que más se parezca**. En caso de que no se supere un **umbral de coincidencia** con ninguna de las personas registradas, mostrará una imágen por defecto avisando de que no se ha podido obtener ningún resultado satisfactorio.
En cualquier caso, junto con la imágen que se obtenga como resultado, se mostrará una **'barra de progreso'**, que indica el porcentage de acierto que ha obtenido al encontrar dicho resultado. Además, se muestra un botón que nos permite crear otra ventana extra con **información de la persona obtenida como resultado** (nombre, edad, lugar de nacimiento y profesión).

## Requisitos:

Es necesario tener instalado python 2.7 y diferentes librerías: cv2 (machine-learning orientado a imágenes), tKinter (interfaz), numpy (utilidad), Pillow (operaciones con imágenes).
Proyecto desarrollado y probado en Windows 10.

- NOTA: En el resto de versiones de windows no se asegura su correcto funcionamiento.
- NOTA: En otros sistemas operativos como Linux no funciona debido a las librerías exclusivas de windows y a las rutas utilizadas en los ficheros.

## Instrucciones:

Para ejecutar el programa, simplemente hay que **descargarse el proyecto** (podemos hacer un clone a una carpeta local desde github o simplemente descargarlo como .zip) y dar doble click sobre el fichero llamado **'run.bat'** que encontramos en la carpeta principal.
Esto nos abrirá una consola de comandos donde nos irán saliendo mensajes informativos sobre el progreso del programa, aunque la parte principal creará ventanas para mostrar la interfaz y que la información aparezca de forma más visual y entendible para el usuario medio.

Las principales fases por las que pasa nuestro programa son:

##### 1.- Añadir nuevas imágenes.
- Nos preguntará si queremos añadir una imágen nueva a la base de datos.
- En caso de responder [Y] (yes), se inicializará la cámara por defecto del equipo.
        
- NOTA: La cámara por defecto es la webcam en caso de tener integrada, externa en caso contrario. En caso de tener ambas cámaras instaladas, se utilizará la integrada.
        
- Podremos tomar una imágen pulsando [C] o salir sin tomar ninguna pulsando [Q].
        
##### 2.- Entrenar red.
- A continuación, si hemos guardado una imágen nueva en la base de datos en el apartado 1, pasaremos directamente al punto en que se entrena la red, en caso conrtario nos preguntará si queremos entrenarla o no.
- En caso de decir que NO, se utilizarán los recursos almacenados del último entrenamiento.
- En caso de decir que SI, se crearán las imágenes en el formato adecuado y se entrenará la red, utilizando los recursos recién creados.

- IMPORTANTE: si se añaden imágenes previas a la ejecución del programa a la base de datos (antes del punto 1), entrenar la red para evitar problemas sobre identificaciones erróneas.

##### 3.- Carga de recursos e inicialización.
- Se cargan los recursos necesarios: trainerData.yml y haarcascade_frontalface_default.xml
- A continuación, se le pregunta al usuario cómo desea obtener la imágen que va a contrastar con la base de datos: desde fichero (punto 4.1) o desde la cámara (punto 4.2).

##### 4.1.- Obtener imágen desde fichero.
- Si se selecciona esta opción, se abrirá una pequeña interfaz en la que el usuario puede buscar la imágen que quiera en el sistema. 
- Una vez que se encuentra la imágen, basta con dar doble click sobre ella o seleccionarla y pulsar aceptar.
        
- NOTA: Se puede filtrar el tipo de ficheros que se pueden ver para facilitar la búsqueda (restringido a ".png" y ".jpg").

##### 4.2.- Obtener captura.
- Al seleccionar esta opción, si hay más de una cámara instalada nos dejará elegir qué cámara utilizar. En caso contrario utilizará la cámara por defecto.
        
- NOTA: La cámara por defecto es la webcam en caso de tener integrada, externa en caso contrario.
        
- Con la cámara seleccionada se inicializan los parámetros para la captura de imágenes por defecto (fps, tamaño de la imágen, etc).

- NOTA: en caso de no poder inicializar la cámara con estos parámetros, mostrará un mensaje avisándonos y pasará a la fase 5 con una imágen por defecto.

- Con la cámara inicializada correctamente, aparecerá una ventana con la imágen en tiempo-real capturada con la cámara.
- Cuando el usuario tiene el control sobre la cámara, puede:
   - Pulsar [Q] para salir sin tomar ninguna imágen.
   - Pulsar [I] para mostrar información sobre esa imágen y el menú de la cámara.
   - Pulsar [P] para pausar la captura de imágenes. Mientras se esté en modo pausa el programa se queda en 'stand-by', y no se toman acciones hasta que se reanuda la ejecución.
   - Pulsar [ESPACIO] mientras está en modo pausa para reanudar la ejecución.
   - Pulsar [C] para tomar una captura y seguir ejecutando el programa.

- NOTA: no se puede tomar una captura a no ser que haya exáctamente una persona delante de la cámara. Se toma esta decisión para evitar problemas a la hora tanto de entrenar la red como de mostrar coincidencias con la base de datos.
- NOTA: si se pulsa [Q] se pasará a la fase 5 con una imágen por defecto.

##### 5.- Comparar imágenes.
- Con la imágen obtenida de la fase 4, se analiza dicha imágen y se comparan los resultados con los obtenidos de entrenar las imágenes almacenadas en la base de datos (fichero 'trainerData.yml' de la fase 3).
- Se obtiene una **ID**, una **ETIQUETA** (nombre de la imágen) y un **PORCENTAGE** de coincidencia entre ambas imágenes (la mayor coincidencia de la base de datos).
- Se carga la imágen de la base de datos con la **etiqueta** del apartado anterior y la información relacionada con la **id** obtenida del fichero 'info.txt'.

##### 6.- Mostrar resultado.
- Se muestra una ventana con ambas imágenes, la obtenida de la captura/fichero y la de máxima coincidencia de la base de datos.

- NOTA: las imágenes se recortan para mostrar sólo el rostro, de esta manera se evitan los tamaños de imágenes excesivamente grandes/pequeños.

- Se muestra además el porcentage de coincidencia que hayan tenido, y una barra de progreso que indica dicho porcentage junto con el nombre de la imágen de la base de datos.

- NOTA: el nombre que se muestra sobre la imágen de la derecha es el de la persona a la que corresponda dicha fotografía (extraído del fichero 'info.txt'), mientras que el nombre que se muestra sobre la barra de progreso es el correspondiente al nombre del fichero de dicha foto. Se muestran ambos nombres en caso de que el usuario necesite acceder a esa foto manualmente.

- Además, se crea un botón 'Info.', que al pulsarle crea una pequeña ventana extra con información sobre la imágen resultado. Esta información se puede editar en el fichero 'info.txt' mencionado en la fase 5.

- IMPORTANTE: si se añade una imágen a la base de datos, es necesario añadir una línea en el fichero 'info.txt' con al información de la persona que acabamos de introducir en la base de datos. Esta línea deberá ir en la posición exacta en la que se encuentre la imágen en relación al resto. Por ejemplo, si añadimos una imágen a la que nombramos 'aaa.jpg' será la primera en la base de datos, por lo que deberemos añadir una línea al principio del fichero 'info.txt'. Si añadimos una imágen que se llame 'zzz.jpg' a la base de datos será la última, por lo que necesitaremos añadir una línea al final del fichero 'info.txt'. En caso de no realizar este paso, cuando se muestren los resultados, se hará con la información de otra persona.
- NOTA: esta parte de introducir información sobre cada persona en un fichero en la posición exacta es muy tedioso y peligroso, por ello se está estudiando la posibilidad de crear una base de datos real para almacenar esta información, de manera que cada imágen tenga vinculada su información de manera automática.
