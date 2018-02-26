from src.ImageCaptureFromFile import ImageCaptureFromFileClass as iFFClass
from src.TestingTensorflow import TestClass as tstClass

name1 = "..\sources\FOTO_DNI_1.jpg"
name2 = "..\sources\FOTO_DNI_2.jpg"
default = "..\sources\default.png"


def firstSteps(value=False):
    if value.__eq__(False):
        return
    tst = tstClass()
    tst.testConstants()
    tst.testVariables1()
    tst.testVariables2()
    tst.testVariables3()
    tst.testVariables4()


def loadI(name=default):

    iFF = iFFClass(name)
    iFF.captureImageFromFile()

    print("Image loaded successfully from '" + str(name) + "'file")

    return iFF


def loadMultipleImages(names):

    print("\n\tLoading Images...\n")

    for n in names:
        loadI(n)
        pass


if __name__ == "__main__":
    firstSteps(True)
    names = [name1, name2, default]
    #loadMultipleImages(names)
