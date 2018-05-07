# Título:
### TFG-FacialRecognition

## Universidad de Burgos

# Autor: 
#### Víctor de Castro Hurtado

# Tutor: 
#### César Represa Pérez

# Índice:
  - Introducción
  - Instrucciones

## Descripción:

Se pretende diseñar un sistema de identificación de personas a través de un programa de reconocimiento facial con rostros previamente incluidos en una base de datos. El sistema de desarrollará en Python y utilizando técnicas de Machine Learning.

## Introducción:

Repositorio de Github donde se aloja el TFG de reconocimiento facial basado en machine-learning.

El TFG consiste en una aplicación que, dadas dos imágenes (una obtenida desde una cámara y la otra alojada localmente), sea capaz de distinguir si en ambas imágenes se encuentra la misma persona utilizando técnicas de machine-learning.

##### Python version 2.7

## Instrucciones:

##### 1-. Entrenar red.
        - Al principio nos preguntará si queremos entrenar la red o no.
        - En caso de decir que NO, se utilizarán los recursos almacenados del último entrenamiento.
        - En caso de decir que SI, se crearán las imágenes en el formato adecuado y se entrenará la red, utilizando los recursos recién creados.

##### 2.- Carga de recursos e inicialización.
        - Se cargan los recursos necesarios: trainerData.yml y haarcascade_frontalface_default.xml
        - Se inicializa la cámara y se le da el control al usuario.

##### 3.- Obtener captura.
        - Aparece directamente la imágen en tiempo-real capturada con la cámara.
        - Cuando el usuario tiene el control sobre la cámara, puede:
          - Pulsar [Q] para salir sin tomar ninguna imágen.
          - Pulsar [I] para mostrar información sobre esa imágen y el menú de la cámara.
          - Pulsar [P] para pausar la captura de imágenes. Mientras se esté en modo pausa el programa se queda en 'stand-by',
            y no se toman acciones hasta que se reanuda la ejecución.
          - Pulsar [ESPACIO] mientras está en modo pausa para reanudar la ejecución.
          - Pulsar [C] para tomar una captura y seguir ejecutando el programa.

          NOTA: no se puede tomar una captura a no ser que haya exáctamente una persona delante de la cámara.
            Se toma esta decisión para evitar problemas a la hora tanto de entrenar la red como de mostrar ocurrencias.

##### 4.- Comparar imágenes.
        - Se compara la imágen obtenida con la base de datos.
        - Se obtiene una ID, una ETIQUETA (nombre de la imágen) y un PORCENTAGE de coincidencia entre ambas imágenes (la mayor coincidencia de la base de datos).
        - Se carga la imágen con la etiqueta del apartado anterior.

##### 5.- Mostrar resultado.
        - Se muestra una ventana emergente con ambas imágenes, la obtenida de la captura y la de máxima coincidencia de la base de datos.
        - Se muestra además el porcentage de coincidencia que hayan tenido, y una barra de progreso que indica dicho porcentage.
        - Se muestra también el nombre de la imágen de la base de datos y la ruta completa hasta ella.

        NOTA: las imágenes se recortan para mostrar sólo el rostro, de esta manera se evitan los tamaños de imágenes excesivamente grandes/pequeños.