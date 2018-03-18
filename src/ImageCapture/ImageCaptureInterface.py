
from abc import abstractmethod

class AbstractImageCaptureClass():

    def __init__(self):
        pass

    @abstractmethod
    def loadImage(self):
        pass