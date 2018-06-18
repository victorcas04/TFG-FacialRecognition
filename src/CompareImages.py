
# encoding: utf-8

import Util as util
import Files as files
import TextInterface as txtIf

def getLoadedYml():
    reco = files.getReco()
    reco.read(files.getFileName(files.ymlFile, files.recognizerFolderPath))
    return reco

def compareSingle(img):
    gray = util.imageToGrayscale(img)

    x = 0; y = 0; w = gray.shape[1]; h = gray.shape[0]

    try:
        recognizer = getLoadedYml()
        id, conf = recognizer.predict(gray[y:y + h, x:x + w])
    except:
        txtIf.printError(txtIf.ERRORS.NETWORK_NOT_TRAINED)
        id = -1; conf = 100;

    conf = 100 - float(conf)
    percentage = float("{0:.2f}".format(conf))
    return id, percentage

def compare(img, path=files.facesDatasetPath):

    label = None   # NSF: No Such File
    imgRet = None
    txtIf.printMessage(txtIf.MESSAGES.COMPARING_IMAGES)

    id, p = compareSingle(img)

    if id > -1:
        if p <= 0:
            p = 0
        else:
            p = float("{0:.2f}".format(p)) if p <= 100 else 100
        imgsOr = files.filesOnDir()
        label = imgsOr[id].split(".")[0]
        print("Information about comparison: id= " + str(id) + "   ---   label= " + str(label) + "   ---   coincidence= " + str(p))
        imgRet = files.loadImage(files.getFileName("face_" + label + files.extensionJPG, folder=path))

    return imgRet, p, label