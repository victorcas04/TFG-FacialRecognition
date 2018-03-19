
from src.ImageCapture.ImageCaptureInterface import AbstractImageCaptureClass as Parent
#python3.6 import matplotlib.image as mpimg
import cv2

class ImageCaptureFromFileClass(Parent):

    def __init__(self, name):
        self.name = name

    def loadImage(self):
        Parent.image = cv2.imread(self.name)
        return Parent.image

    def loadGrayImage(self):
        Parent.image = cv2.imread(self.name, 0)
        return Parent.image
