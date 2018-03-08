
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import numpy as np
import decimal, math

maxImagesPerRow = 4

def getPath():
    return "..\sources\\"

def getImageName(default="default.png"):
    return getPath() + default

def loadImage(filename=getImageName()):
    return mpimg.imread(filename)

def saveImage(image, path=getImageName("savedDefault.png")):
    print("\nSaving image to: " + str(path) + "\n")
    mpimg.imsave(path, image)

def displayImages(images, titles=None):

    if images != None:
        ### Python rounds numbers to the closest even number, so if we have 2.5, it rounded to 2 instead of 3
        ### So we have to convert it to decimal and specify round_half_up to round it correctly
        rows = math.ceil(len(images)/maxImagesPerRow)
        imagesPerRow = decimal.Decimal(len(images) / rows).quantize(decimal.Decimal('1'), rounding='ROUND_HALF_UP')

        #print("n_img_row = " + str(imagesPerRow))
        #print("n_rows = " + str(rows))
        #print("n_img = " + str(len(images)))
        #print("n_tit = " + str(len(titles)))

        window = plt.figure()
        for c, i in enumerate(images):
            subplot = window.add_subplot(rows, imagesPerRow, c + 1)
            plt.imshow(i)
            try:
                subplot.set_title(titles[c])
            except:
                subplot.set_title("Sin Título")
        window.set_size_inches(np.array(window.get_size_inches()) * int(len(images) / 2))
        plt.show()
    else:
        print("No hay imágenes para cargar")

