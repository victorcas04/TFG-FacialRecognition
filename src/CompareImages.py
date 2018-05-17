
# encoding: utf-8

import Util as util

def compareAll(gray):

    face_cascade = util.getLoadedXml()
    recognizer = util.getReco()

    try:
        util.getLoadedYml(recognizer)
    except:
        print("Red no entrenada. Ejecute de nuevo tras entrenar la red.")
        return -1, 0

    faces = face_cascade.detectMultiScale(gray)

    if len(faces) < 1:
        print("No se han detectado caras...")
        return -1, 0

    # Asumiendo sólo 1 cara por imágen
    x, y, w, h = faces[0]

    id, conf = recognizer.predict(gray[y:y + h, x:x + w])

    conf = 100-conf

    percentage = float("{0:.2f}".format(conf))
    return id, percentage
