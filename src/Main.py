from src.ImageCaptureFromFile import ImageCaptureFromFileClass as iFFClass
from src.TestingTensorflow import TestClass as tstClass

dirPath = "..\sources\\"
name1 = dirPath+"FOTO_DNI_1.jpg"
name2 = dirPath+"FOTO_DNI_2.jpg"
default = dirPath+"default.png"

def firstSteps(run=True):

    if run.__ne__(True):
        return

    tst = tstClass()

    if False:
        tst.testConstants()
        tst.testVariables1()
        tst.testVariables2()
        tst.testVariables3()
        tst.testVariables4()

    if False:
        tst.testImages1()
        tst.testImages2()
    tst.testImages3()
        #tst.testImages4()


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
