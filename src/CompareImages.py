
# encoding: utf-8

import Util as util
import Files as files
import TextInterface as txtIf

def getLoadedYml(recognizer = files.getReco()):
    recognizer.read(files.getFileName(files.ymlFile, files.recognizerFolderPath))

def compareAll(gray):

    recognizer = files.getReco()

    try:
        getLoadedYml(recognizer)
    except:
        txtIf.printError(txtIf.ERRORS.NETWORKNOTTRAINED)
        return -1, 0

    faces = util.getFacesMultiScale(gray)

    if len(faces) < 1:
        txtIf.printError(txtIf.ERRORS.IMAGENOFACES)
        #print("ERROR: Cannot compare: no faces detected.")
        return -1, 0

    # Asumiendo sólo 1 cara por imágen
    x, y, w, h = faces[0]

    id, conf = recognizer.predict(gray[y:y + h, x:x + w])

    conf = 100-conf

    percentage = float("{0:.2f}".format(conf))
    return id, percentage

def compare(img, path=files.facesDatasetPath):

    label = None   # NSF: No Such File

    txtIf.printMessage(txtIf.MESSAGES.COMPARINGIMAGES)

    gray = util.imageToGrayscale(img)

    import CompareImages as imgCompare
    id, p = imgCompare.compareAll(gray)

    if id > -1:
        imgsOr = files.filesOnDir()
        label = imgsOr[id].split(".")[0]

    print("Information about comparison: id= " + str(id) + "   ---   label= " + str(label) + "   ---   coincidence= " + str(p))

    if label is not None:   # NSF
        imgRet = files.loadImage(files.getFileName("face_" + label + files.extensionJPG, folder=path))
    else:
        imgRet = files.loadImage(files.getFileName())

    return imgRet, p, label