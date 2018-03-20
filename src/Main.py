from src.ImageCapture.ImageCaptureFromFile import ImageCaptureFromFileClass as iFFClass
from src.Test.TestingTensorflow import TestClass as tstClass
import src.Util as util
#import src.FaceObjectDetectorTutorial.tfrecord as rec

imageDefault = util.getFileName()
meDNI = util.getFileName("FOTO_DNI_1.jpg")
meAscensor = util.getFileName("FOTO_ASCENSOR.jpg")
meBorroso = util.getFileName("FOTO_BORROSA.jpg")
meMalaIluminacion = util.getFileName("FOTO_ILUMINACION.jpg")
grupo = util.getFileName("FOTO_GRUPO_1.jpg")

def firstSteps(run=True):
    if run.__ne__(True):
        return
    tst = tstClass()
    #
    # tst.testVariables()
    # tst.testImages()
    # tst.testPlaceholders()
    #
    tst.testActual(meDNI)

def loadI(name=imageDefault):

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
    firstSteps(True)

    names = [meDNI, meDNI]
    images = loadMultipleImages(names, False)

    if images.__ne__(None):
        for i in images:
            #rec.main(i)
            pass
