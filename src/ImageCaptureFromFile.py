
from PIL import Image
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import os

class ImageCaptureFromFileClass(object):

    name = ""

    def __init__(self, name):

        self.name = name

    def captureImageFromFile(self):

        ''' Read and open image using pillow
        img = Image.open(self.name)
        img.show()
        '''

        ### Read and open image using matplotlib
        image = mpimg.imread(self.name)
        ### This prints size of the image
        print("\nSize of image from '" + str(self.name) + "' file: " + str(image.shape) + "\n")
        plt.imshow(image)
        plt.show()

        '''
        f = open(self.name, 'r+')
        jpgdata = f.read()
        print(jpgdata)
        f.close()
        '''



