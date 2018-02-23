from src.ImageCaptureFromFile import ImageCaptureFromFileClass as iFFClass


class MainClass(object):

    name1 = "..\sources\FOTO_DNI_1.jpg"
    name2 = "..\sources\FOTO_DNI_2.jpg"
    default = "..\sources\default.png"

    def loadI(name=default):

        iFF = iFFClass(name)
        iFF.captureImageFromFile()
        print("Image loaded successfully")
        return iFF

    if __name__ == "__main__":

        iFF1 = loadI()
        iFF2 = loadI()
