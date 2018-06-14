
# encoding: utf-8

import Util as util
import Files as files
import TextInterface as txtIf

def getLoadedYml():
    reco = files.getReco()
    reco.read(files.getFileName(files.ymlFile, files.recognizerFolderPath))
    return reco

def compareSingle(gray, rT=False):
    try:
        recognizer = getLoadedYml()
    except:
        txtIf.printError(txtIf.ERRORS.NETWORK_NOT_TRAINED)
        return -1, 0

    faces = util.getFacesMultiScale(gray)

    if not rT:
        if len(faces) < 1:
            txtIf.printError(txtIf.ERRORS.IMAGE_NO_FACES)
            return -1, 0

        # Asumiendo sólo 1 cara por imágen
        x, y, w, h = faces[0]
    else:
        x = 0; y = 0; w = gray.shape[1]; h = gray.shape[0]

    id, conf = recognizer.predict(gray[y:y + h, x:x + w])

    conf = 100 - float(conf)
    percentage = float("{0:.2f}".format(conf))
    return id, percentage

def compare(img, path=files.facesDatasetPath, rT=False):

    label = None   # NSF: No Such File
    txtIf.printMessage(txtIf.MESSAGES.COMPARING_IMAGES)
    gray = util.imageToGrayscale(img)

    id, p = compareSingle(gray, rT)

    if id > -1:
        imgsOr = files.filesOnDir()
        label = imgsOr[id].split(".")[0]

    print("Information about comparison: id= " + str(id) + "   ---   label= " + str(label) + "   ---   coincidence= " + str(p))

    if label is not None:   # NSF
        imgRet = files.loadImage(files.getFileName("face_" + label + files.extensionJPG, folder=path))
    else:
        imgRet = files.loadImage(files.getFileName())

    return imgRet, p, label