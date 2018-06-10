
# encoding: utf-8

import Util as util
import cv2

def getLoadedYml(recognizer = util.getReco()):
    recognizer.read(util.getFileName(util.ymlFile,util. recognizerFolderPath))

def compareAll(gray):

    face_cascade = util.getLoadedXml()
    recognizer = util.getReco()

    try:
        getLoadedYml(recognizer)
    except:
        print("The network isn't trained. Execute again after train the network.")
        return -1, 0

    #faces = face_cascade.detectMultiScale(gray)
    faces = util.getFacesMultiScale(gray, face_cascade)

    if len(faces) < 1:
        print("No faces detected...")
        return -1, 0

    # Asumiendo sólo 1 cara por imágen
    x, y, w, h = faces[0]

    id, conf = recognizer.predict(gray[y:y + h, x:x + w])

    conf = 100-conf

    percentage = float("{0:.2f}".format(conf))
    return id, percentage
