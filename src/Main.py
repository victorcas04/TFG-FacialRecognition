from src.ImageCaptureFromFile import ImageCaptureFromFileClass as iFFClass
from src.Test.TestingTensorflow import TestClass as tstClass
import src.Util as util

image1 = util.getImageName("FOTO_DNI_1.jpg")
image2 = util.getImageName("FOTO_DNI_2.jpg")
imageDefault = util.getImageName()

def firstSteps(run=True):

    if run.__ne__(True):
        return

    tst = tstClass()

    #
    # tst.testVariables()
    # tst.testImages()
    # tst.testPlaceholders()
    #

    tst.testActual()

def loadI(name=imageDefault):

    iFF = iFFClass(name)
    iFF.captureImageFromFile()

    print("Image loaded successfully from '" + str(name) + "'file")

    return iFF


def loadMultipleImages(names, run=True):

    if run.__ne__(True):
        return

    print("\n\tLoading Images...\n")

    for n in names:
        loadI(n)
        pass


if __name__ == "__main__":
    firstSteps()

    names = [image1, image2, imageDefault]
    loadMultipleImages(names, False)
