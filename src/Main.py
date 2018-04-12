from src.ImageCapture.ImageCaptureFromFile import ImageCaptureFromFileClass as iFFClass
from src.Test.TestingTensorflow import TestClass as tstClass
import src.Util as util
import src.TrainMachine.trainer as train
#import src.FaceObjectDetectorTutorial.tfrecord as rec

meDNI = "FOTO_DNI_1.jpg"
meAscensor = "FOTO_ASCENSOR.jpg"
meBorroso = "FOTO_BORROSA.jpg"
meMalaIluminacion = "FOTO_ILUMINACION.jpg"
meUbu = "FOTO_UBUVIRTUAL_ME.jpg"
CesarUbu = "FOTO_UBUVIRTUAL_CESAR.png"
grupo = "FOTO_GRUPO_1.jpg"

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

    util.askTrain()

    gui = util.createInterfaceWindow()

    photoFromCamera = util.faceInBoxVideo()
    #photoFromDatabase = util.loadImageByName(util.getFileName(meDNI))
    #photoFromDatabase = util.loadImageByGUI(gui)

    #i, p = util.compare(photoFromCamera, photoFromDatabase)
    i, p, n = util.compare(photoFromCamera)

    gui.setTitle(n, p)
    util.displayInterfaceWindow(gui, photoFromCamera=photoFromCamera, photoFromDatabase=i, percentage=p)

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