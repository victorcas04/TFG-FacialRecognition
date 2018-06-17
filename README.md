
# TFG - FacialRecognition

## Universidad de Burgos

## Autor: Víctor de Castro Hurtado

### Tutor: César Represa Pérez

# Índice:
  - Descripción inicial
  - Poniéndonos técnicos... (desarrollo)
  - ¿Qué necesitamos? (requisitos)
  - Instrucciones

## Descripción inicial

Las tecnologías avanzan continuamente, al igual que hacen las amenazas que acompañan a dichas tecnologías. Por ello, y para mantener una sociedad estable, la seguridad debe ir ligada a estos avances.

Con este proyecto se pretende abordar la temática de la seguridad en lugares públicos (como pueden ser aeropuertos o centros comerciales) desde el punto de vista del reconocimiento facial.

Para ello, se ha diseñado un prototipo de un sistema de identificación de personas a través de un programa de reconocimiento facial, desarrollado en *Python* y utilizando técnicas de *Machine-Learning*.
En dicho sistema se parte de una base de datos que contiene imágenes de personas en una lista de busca y captura. De este modo, a partir de una imagen capturada en el lugar de interés, el sistema reconocerá el rostro y lo identificará si se encuentra en la base de datos.

## Poniéndonos técnicos...

El repositorio de Github donde se encuentran los ficheros del TFG de reconocimiento facial basado en machine-learning se puede encontrar en el siguiente [enlace](https://github.com/victorcas04/TFG-FacialRecognition).

El TFG consiste en una aplicación que, dadas dos imágenes, una obtenida en el momento de ejecución, ya sea mediante fichero (accediendo a la foto que tengamos almacenada en nuestro equipo),  o mediante una captura que realicemos con nuestra cámara,  y la otra alojada localmente en una base de datos: sea capaz de distinguir si en ambas imágenes se encuentra la misma persona utilizando técnicas de machine-learning.

A la hora de comparar ambas imágenes se utiliza la extracción de características mediante el algoritmo *LBPH* y la herramiento *OpenCV*. Si la persona que se intenta identificar no estaba registrada en la base de datos, aparecerá la persona que esté registrada que más se parezca.
En caso de que no se supere un **umbral de coincidencia** con ninguna de las personas registradas, mostrará una imagen por defecto avisando de que no se ha podido obtener ningún resultado satisfactorio.
Además, esta misma imagen por defecto se mostrará si no se reconoce exactamente un sólo rostro (se toma esta decisión para ahorrarnos problemas a la hora de extraer características).

En cualquier caso, junto con la imagen que se obtenga como resultado, se mostrará una barra de progreso, que indica el porcentaje de acierto que ha obtenido al encontrar dicho resultado. Además, se muestra un botón que nos permite crear un pequeño *pop-up* con información de la persona obtenida como resultado (nombre, edad, lugar de nacimiento y profesión).

Como desarrollo adicional, se ha implementado un sistema de reconocimiento totalmente en tiempo-real, en el cual se muestra un vídeo de la cámara que esté grabando, el cual se analiza cada determinados *frames* para obtener las comparaciones automáticamente (en lugar de una comparación por ejecución como en le modo anterior).
La interfaz utilizada en este último caso es similar a la anterior, pero eliminando el botón que proporcionaba esa ventana con más información. Esto se ha hecho ya que, al poder cambiar el resultado en poco tiempo, era un elemento contra-producente.

## ¿Qué necesitamos?

Es necesario tener instalado *python* (preferiblemente en su versión 2.7, o un entorno virtual con dicha versión ya que es el entorno en el que se ha desarrollado) y diferentes librerías imprescindibles como son *cv2* (librería de OpenCV orientada a computer vision), *tKinter* (necesaria para mostrar la interfaz gráfica), *numpy* (diversas operaciones de utilidad), *Pillow* (para realizar cambios sobre imágenes).
El proyecto ha sido desarrollado y probado en *Windows 10*.

- *NOTA*: En el resto de versiones de windows no se asegura su correcto funcionamiento.
- *NOTA*: En otros sistemas operativos como *Linux* no funciona debido a las librerías exclusivas de windows y a las rutas utilizadas en los ficheros.

## Instrucciones:

Para ejecutar el programa, simplemente hay que descargarse el proyecto (podemos hacer un *clone* a una carpeta local desde *github* o simplemente descargarlo como *.zip*) y dar *doble click* sobre el fichero llamado *run.bat* que encontramos en la carpeta principal.
Esto nos abrirá una consola de comandos donde nos irán saliendo mensajes informativos sobre el progreso del programa (orientados más al uso por parte del desarrollador, aunque también pueden resultar útiles a todo tipo de usuarios), aunque la parte principal creará ventanas para mostrar la interfaz y que la información aparezca de forma más visual y entendible para el usuario medio.

Las principales fases por las que pasa nuestro programa son:

##### 1.- Añadir nuevas imágenes a la base de datos
- Nos preguntará si queremos añadir una imagen nueva a la base de datos.

- En caso de responder sí [Y], se inicializará la cámara por defecto del equipo (si tenemos una externa conectada, utilizará esa, en caso contrario usará la webcam integrada).
        
- Se pueden seguir las instrucciones del apartado *Instrucciones adicionales: Menú de utilización general de la cámara*.

- En caso de obtener una imagen (podemos elegir no hacerlo), nos pedirá introducir una serie de datos sobre la persona que deberíamos encontrar en esa imagen: nombre, edad, ciudad de nacimiento y profesión.
En caso de no querer rellenar alguno de esos campos se tomarán valores por defecto. Además, se pedirá introducir el nombre de la imagen que acabamos de obtener para almacenarla en nuestra base de datos.
Estos datos se almacenarán en un fichero local llamado *info.txt*.

- **IMPORTANTE**: Los datos de este fichero se pueden modificar manualmente, aunque conviene no hacerlo ya que, de cambiar el nombre de la imagen por error, podemos encontrarnos con datos inconsistentes y tener errores en la ejecución. En caso de hacer cambios sobre este fichero o sobre las imágenes de la base de datos de forma manual (antes de su ejecución), asegurarse de que quedan datos consistentes.
        
##### 2.- Entrenamiento de la red
- A continuación, si hemos guardado una imagen nueva en la base de datos en el apartado *1.- Añadir nuevas imágenes a la base de datos*, pasaremos directamente al punto en que se entrena la red, en caso contrario nos preguntará si queremos entrenarla o no.

- En caso de decir que NO, se utilizarán los recursos almacenados del último entrenamiento (la primera vez que se ejecute el programa, a pesar de tener un fichero por defecto, es probable que tengamos que entrenar la red debido a registros internos de la librería que utilizamos).

- En caso de decir que SI, se crearán las imágenes en el formato adecuado y se entrenará la red, utilizando los recursos recién creados.

- **IMPORTANTE**: si se añaden o eliminan imágenes manualmente, de forma previa a la ejecución del programa a la base de datos (antes del apartado *1.- Añadir nuevas imágenes a la base de datos*), entrenar la red para evitar problemas sobre identificaciones erróneas.

##### 3.- Carga de recursos e inicialización
- Se cargan los recursos necesarios: *trainerData.yml* (los datos de nuestra red entrenada en el apartado *2.- Entrenamiento de la red*) y *haarcascade_frontalface_default.xml* (fichero que nos permite identificar un rostro dentro de una imagen a partir de sus características).

- A continuación, se le pregunta al usuario cómo desea obtener la imagen que va a contrastar con la base de datos: desde fichero (apartado *4.1.- Obtener la imagen desde fichero*), desde la cámara (apartado *4.2.- Obtener la imagen mediante una captura*) o en tiempo real (apartado *4.3.-Realizar la identificación en tiempo-real*).

##### 4.1.- Obtener la imagen desde fichero
- Si se selecciona esta opción, se abrirá una pequeña interfaz en la que el usuario puede buscar la imagen que quiera en el sistema. 

- Una vez que se encuentra la imagen, basta con dar *doble click* sobre ella o seleccionarla y pulsar aceptar.

- A continuación, y si la imagen es correcta (sólo tiene un rostro en ella y ocupa al menos el 10% de la imagen), se mostrará en la interfaz explicada en el apartado
*6.- Resultados finales: Interfaz visual*.

- *NOTA*: Se puede filtrar el tipo de ficheros que se pueden ver para facilitar la búsqueda (restringido a *.png* y *.jpg*).

##### 4.2.- Obtener la imagen mediante una captura
- Al seleccionar esta opción, se inicializará la cámara por defecto (en función del modelo de la cámara, tendremos que especificar la máxima resolución posible, en caso de no conocer este dato, se puede dejar el valor por defecto *[640 X 480]*).
        
- *NOTA*: La cámara por defecto es la primera cámara externa que tengamos conectada. En caso de no tener ninguna externa, se utilizará la webcam integrada.

- *NOTA*: en caso de no poder inicializar la cámara con estos parámetros, mostrará un mensaje avisándonos y pasará al apartado *6.- Resultados finales* con una imagen por defecto.

- Con la cámara inicializada correctamente, aparecerá una ventana con la imagen en tiempo-real capturada con la cámara.

- Se pueden seguir las instrucciones del apartado *Instrucciones adicionales: Menú de utilización general de la cámara* para capturar la imagen que queremos analizar. No nos dejará tomar una imagen hasta que haya exactamente una sola persona en dicha imagen.

- *NOTA*: en caso de no querer tomar una captura (opción [Q] del menú), se pasará al apartado *6.- Resultados finales* con una imagen por defecto.

##### 4.3.- Realizar la identificación en tiempo-real
- En este apartado se inicializa la cámara por defecto como en los apartados anteriores, y se muestra directamente en la interfaz (imagen de la izquierda con el título *Original image*).

- Si queremos que nos reconozca (suponiendo que estemos en la base de datos), simplemente debemos ponernos delante de la cámara y esperar a que se actualice la interfaz (este tiempo se ha establecido de **0.5 segundos** para darle tiempo al programa a que extraiga las características del rostro y las compare con las de la red, en caso de disponer de un equipo más potente se puede reducir este tiempo).

- A continuación, se puede observar como los resultados van cambiando en la interfaz explicada en el apartado *6.- Resultados finales: Interfaz visual* en función de la persona que se coloque delante de la cámara, o incluso si cambiamos de posición o modificamos la iluminación.

- El proceso que sigue este apartado en cuanto a la obtención de resultados es similar al que se sigue en los otros dos casos (comprobar apartado *5.- Comparar imágenes y obtener resultados*), salvo que se repite y actualiza cada **0.5 segundos**.

- Para terminar de ejecutar el programa en este punto cerrar la ventana de la interfaz.

##### 5.- Comparar imágenes y obtener resultados
- Este proceso es interno y no tiene efecto en la interfaz de usuario, de manera que no afecta a estos.

- Con la imagen obtenida de los apartados 4.1, o 4.2, se analiza dicha imagen y se comparan los resultados con los obtenidos de entrenar las imágenes almacenadas en la base de datos (fichero *trainerData.yml* mencionado en el apartado *3.- Carga de recursos e inicialización*). Esta comparación se realiza mediante algunas funciones proporcionadas por la librería de *OpenCV*.

- Se obtiene una ID perteneciente a la imagen con mejor resultado de la comparación en nuestro fichero de entrenamiento y un porcentaje, que indica el éxito de dicha comparación.
Con esa ID, se carga la imagen correspondiente, el nombre que tenga dicha imagen y el porcentaje en la interfaz gráfica.

##### 6.- Resultados finales: Interfaz visual
- La interfaz consiste en una ventana con ambas imágenes: la que se quería reconocer y la de máxima coincidencia de la base de datos obtenida en el apartado *5.- Comparar imágenes y obtener resultados*.

- *NOTA*: las imágenes se recortan para mostrar sólo el rostro y se ajustan todas al mismo tamaño, de esta manera se evitan los tamaños de imágenes excesivamente grandes/pequeños.

- Se muestra además el porcentaje de coincidencia que hayan tenido la comparación, y una barra de progreso que indica dicho porcentaje junto con el nombre de la imagen de la base de datos.
Esta barra de progreso cambia de color en función del tanto por ciento que hayamos obtenido (negro < 10%, rojo < 35%, naranja < 50%, amarillo < 80%, verde < 95%, morado >= 95%).

- *NOTA*: el nombre que se muestra sobre la imagen de la derecha es el de la persona a la que corresponda dicha fotografía (extraído del fichero *info.txt*), mientras que el nombre que se muestra sobre la barra de progreso es el correspondiente al nombre del fichero de dicha foto. Se muestran ambos nombres en caso de que el usuario necesite acceder a esa foto en la base de datos manualmente.

- Además, se crea un botón *More Information...* (en los casos 4.1 y 4.2), que al pulsarle crea un pequeño *pop-up* con información sobre la imagen resultado. Esta información se puede encontrar en el fichero *info.txt* mencionado en el apartado *1.- Añadir nuevas imágenes a la base de datos*.

##### Instrucciones adicionales: Menú de utilización general de la cámara
- Cuando el usuario tiene el control sobre la cámara, puede:
   - Pulsar [Q] para salir sin tomar ninguna imagen.
   - Pulsar [I] para mostrar información sobre esa imagen y el menú de la cámara.
   - Pulsar [P] para pausar la captura de imágenes. Mientras se esté en modo pausa el programa se queda en *stand-by*, y no se toman acciones hasta que se reanuda la ejecución.
   - Pulsar [ESPACIO] mientras está en modo pausa para reanudar la ejecución.
   - Pulsar [C] para tomar una captura y seguir ejecutando el programa.

A continuación se deja una imagen de ejemplo de un resultado de ejecución obteniendo la imagen mediante fichero.

![Interfaz final recolor - Comparación mediante fichero](/Other/Images/develop/interface_final_color.png)
