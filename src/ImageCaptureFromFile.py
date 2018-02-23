
from PIL import Image

class ImageCaptureFromFileClass(object):

    name = ""

    def __init__(self, name):

        self.name = name

    def captureImageFromFile(self):

        img = Image.open(self.name)
        img.show()
        return

        f = open(self.name, 'r+')
        jpgdata = f.read()
        print("2")
        print(jpgdata)
        f.close()
        

