
from src.ImageCapture.ImageCaptureInterface import AbstractImageCaptureClass as Parent
import src.Util as util
#python3.6 import matplotlib.image as mpimg
import cv2

class ImageCaptureFromFileClass(Parent):

    def __init__(self, name=util.getImageName()):
        self.name = name

    def loadImage(self):
        Parent.image = self.captureImageFromFile(self.name)
        return Parent.image

    def captureImageFromFile(self, filename):
        #python3.6 return mpimg.imread(filename)
        return cv2.imread(filename)
