from src.ImageCapture.ImageCaptureFromFile import ImageCaptureFromFileClass as iFFClass
from src.Test.TestingTensorflow import TestClass as tstClass
import src.Util as util
import src.TrainMachine.trainer as train
#import src.FaceObjectDetectorTutorial.tfrecord as rec
import cv2

meDNI = "FOTO_DNI_1.jpg"
meAscensor = "FOTO_ASCENSOR.jpg"
meBorroso = "FOTO_BORROSA.jpg"
meMalaIluminacion = "FOTO_ILUMINACION.jpg"
meUbu = "FOTO_UBUVIRTUAL_ME.jpg"
CesarUbu = "FOTO_UBUVIRTUAL_CESAR.png"
grupo = "FOTO_GRUPO_1.jpg"

pathDatasetFullImages = "dataset"
pathDatasetFacesImages = "facesDataset"

def firstSteps(run=True):
    if run.__ne__(True):
        return
    tst = tstClass()
    #
    # tst.testVariables()
    # tst.testImages(meDNI)
    # tst.testPlaceholders()
    # tst.testFaceLocation(util.getFileName(meDNI))
    #
    tst.testActual()

def loadI(name=util.getFileName()):

    iFF = iFFClass(name)
    iFF.captureImageFromFile()

    print("Image loaded successfully from '" + str(name) + "'file")

    return iFF


def loadMultipleImages(names, run=True):

    images = []
    if run.__ne__(True):
        return None

    print("\n\tLoading Images...\n")

    for n in names:
        images.append(loadI(n))

    return images

if __name__ == "__main__":

    print("\n\nTFG - Facial Recognition - Víctor de Castro Hurtado\n\n")

    firstSteps(False)

    #util.createCutFacesFromDatabase()
    pathh = pathDatasetFacesImages

    #util.askTrain(pathh)
    util.train(pathh)

    #util.recognizeRealTime()

    #print("Exit")
    #util.getScan()

    gui = util.createInterfaceWindow()
    #h, w = util.getDisplaySize()
    gui.fixedSize(900, 1600)

    photoOriginal = util.faceInBoxVideo()
    #photoOriginal = util.loadImageByName(util.getFileName(meDNI))
    #photoOriginal = util.loadImageByGUI(gui)

    #i, p = util.compare(photoFromCamera, photoFromDatabase, pathDatasetFullImages)

    i, p, n, id = util.compare(photoOriginal, path=pathh)
    if False:
        n = "./facesDataset/face_cas.jpg"
        i = util.loadImageByName(n)
        p = 71.38
        id = 1


    ### util.createCutFacesFromDatabase()
    #util.displayImages([util.cutFaceFromImage(photoOriginal), util.cutFaceFromImage(i)], ["original_face", "database_face"])

    if p < 60:
        i = util.loadFileImage(util.getFileName())

    gui.setTitle(n, p)

    '''
    print("\n¿Desea mostrar el resultado a partir de las imágenes originales o exclusivamente las caras detectadas?")
    print(" - C - Imágen Recortada.\n - O - Imágen Original.\n")
    s = util.getScan()
    '''
    if pathh.__eq__(pathDatasetFacesImages):#s.__eq__("C") or s.__eq__("c"):
        #util.displayInterfaceWindow(gui, photoFromCamera=util.cutFaceFromImage(photoOriginal), photoFromDatabase=util.cutFaceFromImage(i), percentage=p)
        pOri = util.cutFaceFromImage(photoOriginal)
        pDet = util.cutFaceFromImage(i)
    else:
        #util.displayInterfaceWindow(gui, photoFromCamera=photoOriginal, photoFromDatabase=i, percentage=p)
        name = "dataset\\" + util.loadDictIdLabels().get(id) + ".jpg"
        i = util.loadImageByName(name)
        pOri = photoOriginal
        pDet = i
        #util.displayInterfaceWindow(gui, photoFromCamera=photoOriginal, photoFromDatabase=i, percentage=p)

    util.displayInterfaceWindow(gui, photoFromCamera=util.resizeFaceImage(pOri), photoFromDatabase=util.resizeFaceImage(pDet), percentage=p)

    '''
    names = [util.getFileName(meDNI), util.getFileName(meDNI)]
    images = loadMultipleImages(names, False)
    '''

    #util.mainMenu()

    '''
    if images.__ne__(None):
        for i in images:
            #rec.main(i)
            pass
    '''