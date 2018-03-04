from src.ImageCaptureFromFile import ImageCaptureFromFileClass as iFFClass
from src.Test.TestingTensorflow import TestClass as tstClass

dirPath = "..\sources\\"
name1 = dirPath+"FOTO_DNI_1.jpg"
name2 = dirPath+"FOTO_DNI_2.jpg"
default = dirPath+"default.png"

def firstSteps(run=True):

    if run.__ne__(True):
        return

    tst = tstClass()

    #
    # tst.testVariables()
    # tst.testImages()
    #

    tst.testPlaceholders()

def loadI(name=default):

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

    names = [name1, name2, default]
    loadMultipleImages(names, False)
