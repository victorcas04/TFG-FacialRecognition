
#python3.6 import matplotlib.image as mpimg
#python3.6 import matplotlib.pyplot as plt
import numpy as np
import decimal, math
import cv2
import wx
import src.ImageCapture.ImageCaptureFromCamera as imgCamera
import src.ImageCapture.ImageCaptureFromFile as imgFile

maxImagesPerRow = 4
thresholdNeighborhoodBlockSize = 45
constantSubstractedFromWeight = 13

def getDisplaySize():
    app = wx.App(False)
    w, h = wx.GetDisplaySize()
    #print("Anchura de Patalla: " + str(w) + "\nAltura de Pantalla: " + str(h))
    return h, w

def getFolderPath(folderName="sources"):
    return "..\\" + folderName + "\\"

def getFileName(defaultFile="default.png", folder=getFolderPath()):
    return folder + defaultFile

def saveImage(image, path=getFileName("savedDefault.png")):
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

def displaySameImageMultipleEffects(images, titles):
    img1 = images[0]
    resImg = img1
    h, w, d = img1.shape
    for i in images[1:]:

        try:
            h2, w2, d2 = i.shape
        except:
            i = cv2.cvtColor(i, cv2.COLOR_GRAY2BGR)

        resImg = np.hstack((resImg, i))

    resTit = '-'.join(titles)

    cv2.imshow(resTit, resImg)
    cv2.waitKey(0)

def resizeImage(image):

    h = image.shape[0]
    w = image.shape[1]
    hd = getDisplaySize()[0]
    wd = getDisplaySize()[1]

    if h <= hd and w <= wd:
        imageResizedString = "Original Size: " + str(image.shape) + " - Under Limits"
        return image, imageResizedString

    if h > hd:
        hh = hd
        ww = w / (h/hd)
        imageResized = cv2.resize(image, (int(ww), int(hh)))
        imageResizedString = "Over Limits - Height" + "\n" + "Original Size: " + str(image.shape) + " - New Size: " + str(imageResized.shape)
        return imageResized, imageResizedString

    if w > wd:
        ww = wd
        hh = h / (w / wd)
        imageResized = cv2.resize(image, (int(ww), int(hh)))
        imageResizedString = "Over Limits - Width" + "\n" + "Original Size: " + str(image.shape) + " - New Size: " + str(imageResized.shape)
        return imageResized, imageResizedString

    imageResized = image

    #cv2.namedWindow('image', cv2.WINDOW_NORMAL)
    #cv2.resizeWindow('image', getDisplaySize()[0], getDisplaySize()[1])

    return imageResized

def loadDefaultImage():
    print("Cargando imágen por defecto...")
    #python3.6 return mpimg.imread(getImageName())
    return cv2.imread(getFileName())

def thresholdImageIllumination(image, blockSize=thresholdNeighborhoodBlockSize, cleanSize=constantSubstractedFromWeight):
    return cv2.adaptiveThreshold(image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, blockSize, cleanSize)
    cv2.adaptiveThreshold()

def loadfileImageGray(imageName):
    iF = imgFile.ImageCaptureFromFileClass(imageName)
    imgFF = iF.loadGrayImage()
    return imgFF

def loadFileImage(imageName):
    iF = imgFile.ImageCaptureFromFileClass(imageName)
    imgFF = iF.loadImage()
    return imgFF

def loadCameraImage():
    iC = imgCamera.ImageCaptureFromCameraClass()
    imgFC = iC.loadImage()
    return imgFC

def imageToGrayscale(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
