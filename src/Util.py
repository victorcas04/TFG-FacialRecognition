
#python3.6 import matplotlib.image as mpimg
#python3.6 import matplotlib.pyplot as plt
import numpy as np
import decimal, math
import cv2

maxImagesPerRow = 4

def getPath():
    return "..\sources\\"

def getImageName(default="default.png"):
    return getPath() + default

def saveImage(image, path=getImageName("savedDefault.png")):
    print("\nSaving image to: " + str(path) + "\n")
    #python3.6 mpimg.imsave(path, image)
    cv2.imwrite(path, image);

def imageSize(image):
    ### This prints size of the image
    print("\nSize of image: " + str(image.shape) + "\n")

def displayImages(images=None, titles=None):

    if len(images)>0:
        ### Python rounds numbers to the closest even number, so if we have 2.5, it rounded to 2 instead of 3
        ### So we have to convert it to decimal and specify round_half_up to round it correctly
        #rows = math.ceil(len(images)/maxImagesPerRow)
        #imagesPerRow = decimal.Decimal(len(images) / rows).quantize(decimal.Decimal('1'), rounding='ROUND_HALF_UP')

        #print("n_img_row = " + str(imagesPerRow))
        #print("n_rows = " + str(rows))
        #print("n_img = " + str(len(images)))
        #print("n_tit = " + str(len(titles)))
        '''
        c = 0
        for i in images:
            c+=1
            cv2.imshow('frame'+str(c), i)
        cv2.waitKey(0)
        '''

        '''
        img1 = images[0]
        resImg = img1
        h, w, d = img1.shape
        for i in images[1:]:
            resImg = np.hstack((resImg,
                                (cv2.resize(i, (w, h)) if (i is not None)
                                 else cv2.resize(loadDefaultImage(), (w, h)))))
            ###resImg = np.hstack((resImg, i))
            ###np.concatenate((img1, i), axis=1)

        resTit = '-'.join(titles)

        cv2.imshow(resTit, resImg)
        cv2.waitKey(0)
        '''
        c = 0
        for i in images:
            cv2.imshow((titles[c] if (c < len(titles)) else ("Default Title " + str(c))), i)
            cv2.waitKey(0)
            c+=1

        '''python3.6
        window = plt.figure()
        for c, i in enumerate(images):
            subplot = window.add_subplot(rows, imagesPerRow, c + 1)
            try:
                plt.imshow(i)
            except:     ### Si existe al menos una imágen que cargar y el resto no existen, se cargan imágenes por defecto
                plt.imshow(loadDefaultImage())
            try:
                subplot.set_title(titles[c])
            except:
                subplot.set_title("Default Title")
        window.set_size_inches(np.array(window.get_size_inches()) * int(len(images) / 2))
        plt.show()
    '''
    else:               ### Si no hay ninguna imágen no se abre ninguna ventana
        print("No hay imágenes para cargar")


def loadDefaultImage():
    print("Cargando imágen por defecto...")
    #python3.6 return mpimg.imread(getImageName())
    return cv2.imread(getImageName())
