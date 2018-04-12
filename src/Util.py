
#python3.6 import matplotlib.image as mpimg
#python3.6 import matplotlib.pyplot as plt
import numpy as np
import decimal, math
from pathlib import Path
import cv2, wx, sys, time, math, os
import src.ImageCapture.ImageCaptureFromCamera as imgCamera
import src.ImageCapture.ImageCaptureFromFile as imgFile
#from src.GUI.GUI import GUIClass as GUI
import src.GUI.GUI as GUI
import src.TrainMachine.CompareImages as imgCompare
import src.TrainMachine.trainer as trainer
#import dlib

maxImagesPerRow = 4
thresholdNeighborhoodBlockSize = 45
constantSubstractedFromWeight = 13

def checkIfFile(name):
    return Path(name).is_file()

def getScan():
    ri = input()
    #ri = raw_input()
    return ri

def getDisplaySize():
    app = wx.App(False)
    w, h = wx.GetDisplaySize()
    #print("Anchura de Patalla: " + str(w) + "\nAltura de Pantalla: " + str(h))
    return h, w

def getXmlFolderPath(folderName="sources\\xml"):
    return "..\\" + folderName + "\\"

def getImagesFolderPath(folderName="sources\\images"):
    return "..\\" + folderName + "\\"

def getFileName(defaultFile="default.png", folder=getImagesFolderPath()):
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
        if titles is None:
            titles = []
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

    ### NOTE: in cv2.resize() we must specify new dimensions with inverse order ((w, h) instead of (h, w))

    imageResized = image
    imageResizedString = ""

    hd = getDisplaySize()[0]
    wd = getDisplaySize()[1]

    while True:
        preImageResized = imageResized
        h = imageResized.shape[0]
        w = imageResized.shape[1]

        if h <= hd and w <= wd:
            if h <= (hd/2) and w <= (wd/2):
                imageResized = cv2.resize(image, (int(2*w), int(2*h)))
                imageResizedString = imageResizedString + "\nImage Too Small" + "\n" + "Original Size: " + str(
                    preImageResized.shape) + " - New Size: " + str(imageResized.shape)
                continue

            imageResizedString = imageResizedString + "\nSize: " + str(imageResized.shape) + " - Under Limits"
            return imageResized, imageResizedString

        if h > hd:
            hh = hd
            ww = w / (h/hd)
            imageResized = cv2.resize(image, (int(ww), int(hh)))
            imageResizedString = imageResizedString + "\nOver Limits - Height" + "\n" + "Original Size: " + str(
                preImageResized.shape) + " - New Size: " + str(imageResized.shape)

        if w > wd:
            ww = wd
            hh = h / (w / wd)
            imageResized = cv2.resize(image, (int(ww), int(hh)))
            imageResizedString = imageResizedString + "\nOver Limits - Width" + "\n" + "Original Size: " + str(
                preImageResized.shape) + " - New Size: " + str(imageResized.shape)

        #cv2.namedWindow('image', cv2.WINDOW_NORMAL)
        #cv2.resizeWindow('image', getDisplaySize()[0], getDisplaySize()[1])

    return imageResized

def loadImageByName(fullName=getFileName()):
    #python3.6 return mpimg.imread(getImageName())
    return cv2.imread(fullName)

def loadImageByGUI(gui):
    return loadImageByName(gui.selectFile())

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

def getCascadeXmlFile():
    # File from: https://github.com/opencv/opencv/blob/master/data/haarcascades/
    # Repository with files for research and academic purposes
    cascadeXmlFile = "haarcascade_frontalface_default.xml"
    # cascadeXmlFile = "haarcascade_profileface.xml"
    return cascadeXmlFile

def printMenuFaceInBox(fromCamera=True):

    print("\nPress [I] for info.")
    print("Press [Q] to exit.")
    if fromCamera:
        print("Press [P] to pause camera reading.")
        print("Press [SPACE] to resume camera reading (if paused only).")
        print("Press [C] to take the actual frame and exit.\n")


def faceInBoxVideo():

    imageToReturn = None
    maxInt = sys.maxsize
    xml = getFileName(getCascadeXmlFile(), getXmlFolderPath())

    print("Loading " + xml + " file...")
    face_cascade = cv2.CascadeClassifier(xml)

    print("Inicializando cámara...")
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FPS, maxInt)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, maxInt)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, maxInt)
    time.sleep(2)

    print("Mostrando imágen en tiempo real...")

    printMenuFaceInBox()

    while True:

        sampleNum = 0
        ret, img = cap.read()
        gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        rectangleThickness = int((img.shape[0] + img.shape[1]) / (100 * 2 * math.pi))
        rectangleColor = (255, 0, 0)

        for (x, y, w, h) in faces:
            sampleNum = sampleNum + 1
            cv2.rectangle(img, (x, y), (x + w, y + h), rectangleColor, rectangleThickness)
            #cv2.waitKey(1)

        #imageResized, imageResizedString = resizeImage(img)
        #cv2.imshow(" - " + str(sampleNum) + " - person(s) recognized.", imageResized)
        cv2.imshow("Facial Location.", img)

        k = cv2.waitKey(1)
        
        ### Press [I] for info.
        if k == ord('i'):
            print("\n - " + str(sampleNum) + " - person(s) recognized.")
            printMenuFaceInBox()
            #print(imageResizedString)

        ### Press [ESCAPE] to exit.
        #if k == 27:
        #    break

        ### Press [Q] to exit.
        if k == ord('q'):
            break

        ### Press [P] to pause camera reading.
        ### Press [SPACE] to resume camera reading.
        if k == ord('p'):
            while cv2.waitKey(0) != ord(' '):
                print("Press [SPACE] to resume camera reading.")

        ### Press [C] to take the actual frame and exit.
        if k == ord('c'):
            imageToReturn = img
            break

    cap.release()
    cv2.destroyAllWindows()
    return imageToReturn

def faceInBoxImage(photoName):

    img = cv2.imread(photoName)
    xml = getFileName(getCascadeXmlFile(), getXmlFolderPath())

    print("Loading " + xml + " file...")
    face_cascade = cv2.CascadeClassifier(xml)

    print("Checking " + photoName + " size...")
    imageResizedOriginal, imageResizedOriginalString = resizeImage(img)

    rectangleThickness = int((imageResizedOriginal.shape[0] + imageResizedOriginal.shape[1]) / (100 * 2 * math.pi))
    rectangleColor = (255, 0, 0)

    print("Mostrando imágen original...")
    while True:
        cv2.imshow("Original Image", imageResizedOriginal)
        ### Press [ESCAPE] to exit.
        #if cv2.waitKey(0) == 27:  # ord(' '):
        #    break

        ### Press [Q] to exit.
        if cv2.waitKey(0) == ord('q'):
            break

    cv2.destroyAllWindows()

    sampleNum = 0
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in faces:
        sampleNum = sampleNum + 1
        cv2.rectangle(img, (x, y), (x + w, y + h), rectangleColor, rectangleThickness)
    imageResized, imageResizedString = resizeImage(img)

    print("Mostrando imágen reconocida...")

    while True:

        cv2.imshow(" - " + str(sampleNum) + " - person(s) recognized.", imageResized)

        k = cv2.waitKey(0)

        ### Press [I] for info.
        if k == ord('i'):
            print("\n - " + str(sampleNum) + " - person(s) recognized.")
            print(imageResizedString)
            printMenuFaceInBox(False)

        ### Press [ESCAPE] to exit.
        #if k == 27:  # ord(' '):
        #    break

        ### Press [Q] to exit.
        if k == ord('q'):
            break

    cv2.destroyAllWindows()

def mainMenu():
    exit = False
    while True:
        print("\n¿Desea utilizar el sistema a partir de un archivo o desde la cámara del dispositivo?")
        print(" - F - Desde archivo.\n - C - Desde cámara.\n - Q - Salir.\n")
        mainScanner = getScan()
        if mainScanner.__eq__("F") or mainScanner.__eq__("f"):
            print("\nIntroduce el nombre del fichero con extensión:\n(el fichero debe encontrarse en la carpeta sources/images):\n")
            nameScanned = getScan()
            while not checkIfFile(getFileName(nameScanned)):
                print("\nNombre de fichero inexistente.\nIntroduce un nombre válido o [Q] para salir.\n")
                nameScanned = getScan()
                if nameScanned.__eq__("Q") or nameScanned.__eq__("q"):
                    exit = True
                    break
            if not exit:
                print("")
                faceInBoxImage(getFileName(nameScanned))
                break
        elif mainScanner.__eq__("C") or mainScanner.__eq__("c"):
            print("")
            faceInBoxVideo()
            break
        elif mainScanner.__eq__("Q") or mainScanner.__eq__("q"):
            break
        else:
            print("\nComando no reconocido.")

def createInterfaceWindow():
    return GUI.GUIClass()

### Pass Image type objects, not Strings or others
def displayInterfaceWindow(gui, photoFromCamera=None, photoFromDatabase=None, percentage=0.0):

    percentageString = str(percentage) + "%"
    print("\nMostrando resultado con un " + percentageString + " de coincidencia.\n")

    # gui.addLabel("Imágen Original")
    # gui.addImage(photoFromCamera)
    # gui.addLabel("Imágen Encontrada", "right")
    # gui.addImage(photoFromDatabase, "right")
    gui.panelTest(photoFromCamera, "Original Image", "left")
    gui.panelTest(photoFromDatabase, "Founded Image", "right")
    # https://www.pyimagesearch.com/2016/05/23/opencv-with-tkinter/
    # gui.addLabel(porcentaje coincidencia)

    gui.addPercentageLabel(percentageString)
    gui.displayWindow()

def compare(img, img2=None):
    xml = cv2.CascadeClassifier(getFileName(getCascadeXmlFile(),getXmlFolderPath()))
    reco = cv2.face.LBPHFaceRecognizer_create()
    gray = imageToGrayscale(img)
    compareClass = imgCompare.CompareImagesClass(img, xml, reco, gray)
    fN = None
    if img2 is None:
        print("Comparando imágen con las de la base de datos...")
        id = compareClass.compareAll()
        if id is not -1:
            #img2 = loadImageByName(getFileName(str(id) + ".jpg", folder="..\\dataset\\"))
            fN = getFileName(str(id) + ".jpg", folder="./dataset/")
            print("\nComplete name from database= " + str(fN))
            img2 = loadImageByName(fN)
            compareClass.setImageCompared(img2)
        else:
            print("\nNo se ha podido reconocer ninguna cara...")
            img2 = img
            fN ="NoSuchFile"
    else:
        print("Comparando imágen con la imágen proporcionada...")
        compareClass.compareSingle(img2)

    p = compareClass.getPercentage()

    return img2, p, fN

def train():
    trainer.train()

def askTrain():
    print("¿Quieres entrenar la red antes? ( S / N )")
    while True:
        s = getScan()
        if s == "S":
            print("Entrenando red...")
            train()
            break
        elif s == "N":
            break
        else:
            print("No se reconoce el comando. Utiliza [S] o [N].")
