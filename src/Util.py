
# encoding: utf-8

from __future__ import division
import cv2, os, wx

fromExecutable = True
delimiter = '\\'
datasetPath = '..'+delimiter+'sources'+delimiter+'dataset'
facesDatasetPath = '..'+delimiter+'sources'+delimiter+'facesDataset'
xmlFolderPath = '..'+delimiter+'sources'+delimiter+'xml'
xmlFile = 'haarcascade_frontalface_default.xml'
recognizerFolderPath = ".." + delimiter + 'sources' + delimiter + 'recognizer'
ymlFile = 'trainedData.yml'
recognizerDict = 'dictionary_ID_labels.txt'
recognizerInfo = 'info.txt'

def getScan():
    if fromExecutable:
        ri = raw_input()
    else:
        ri = input()
    return ri

def getDisplaySize():
    app = wx.App(False)
    w, h = wx.GetDisplaySize()
    return h, w

def getFileName(defaultFile="default.png", folder="..\\sources"):
    return folder + delimiter + defaultFile

def saveImage(image, path=getFileName("savedDefault.png")):
    print("\nSaving image in: " + str(path) + "...\n")
    cv2.imwrite(path, image);

def loadImage(fullName=getFileName()):
    print("Loading image" + str(fullName) + "...")
    return cv2.imread(fullName)

def loadImageByGUI(gui):
    return loadImage(gui.selectFile())

def imageToGrayscale(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

def imageToThreshold(image):
    imgB = cv2.medianBlur(imageToGrayscale(image), 5)
    th = cv2.adaptiveThreshold(imgB, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
    return th

def getLoadedXml():
    return cv2.CascadeClassifier(getFileName(xmlFile, xmlFolderPath))

def getReco():
    return cv2.face.LBPHFaceRecognizer_create()

def getLoadedYml(recognizer = getReco()):
    recognizer.read(getFileName(ymlFile, recognizerFolderPath))

def getFacesMultiScale(gray, faceCascade):
    return faceCascade.detectMultiScale(gray, 1.2, 5, minSize=(gray.shape[0]//10, gray.shape[1]//10))

def printMenuFaceInBox(fromCamera=True):

    print("\nOPTIONS:\n")
    print("Press [I] to display general information.")
    print("Press [Q] to quit.")
    if fromCamera:
        print("Press [P] to pause the camera.")
        print("Press [SPACE] to resume the camera (only if it was paused).")
        print("Press [C] to capture the actual frame and close the camera.\n")

def resizeFaceImage(image, aspect_ratio=2):
    h, w = getDisplaySize()
    prop = h/image.shape[1]
    newSize = (int((prop*image.shape[1])/aspect_ratio), int((prop*image.shape[0])/aspect_ratio))
    newImage = cv2.resize(image, (newSize[0], newSize[1]))
    return newImage

def displayInterfaceWindow(gui, photoFromCamera=None, photoFromDatabase=None, percentage=0.0):

    percentageString = str(percentage) + "%"
    print("\nDisplaying result with a " + percentageString + " of coincidence.\n")

    gui.createTop_BottomPanel(photoFromCamera, photoFromDatabase, percentage)
    gui.displayWindow()

# Podríamos guardar el diccionario en una variable desde trainer.py, pero de este forma nos aseguramos tener el
#   diccionario guardado en caso de no re-entrenar la red en cada ejecución.
def loadDictIdLabels():
    d = {}
    with open(recognizerFolderPath + delimiter + recognizerDict) as f:
        for line in f:
            p = line.split()
            d[int(p[0])] = p[1]
    return d

def loadInfo(id):
    i = 0
    name = " - "; age = " - "; birth_place = " - "; job = " - "
    if id > -1:
        with open(recognizerFolderPath + '\\' + recognizerInfo) as f:
            for line in f:
                if i < id:
                    i+=1
                else:
                    # Ejemplo de lo que nos encontramos en este fichero
                    # Alexandra Daddario, 32, Nueva York, Actriz
                    # IMPORTANTE: la línea cno la información debe estar en la misma posición (respecto al resto) que la imágen correspondiente
                    p = line.split(',')
                    name = p[0]; age = p[1]; birth_place = p[2]; job = p[3]
                    break
    info = {"name": name, "age": age, "birth_place": birth_place, "job": job}
    return info

def compare(img, path=facesDatasetPath):

    dictIDlabels = loadDictIdLabels()
    label = None   # NSF: No Such File

    print("\nComparing image...")

    gray = imageToGrayscale(img)

    import CompareImages as imgCompare
    id, p = imgCompare.compareAll(gray)

    if id > -1:
        imgsOr = os.listdir(datasetPath)
        label = imgsOr[id].split(".")[0]

    print("id= " + str(id) + "   ---   label= " + str(label) + "   ---   coincidence= " + str(p))

    if label is not None:   # NSF
        imgRet = loadImage(getFileName(str(dictIDlabels.get(id)) + ".jpg", folder=path))
    else:
        print("\nWARNING: No faces could be recognized.")
        imgRet = loadImage(getFileName())

    return imgRet, p, label, loadInfo(id)

def train():
    import trainer
    trained = trainer.train()

    if not trained:
        print("WARNING: Network couldn's be trained.")

    return trained

def askNewImage():
    print("If you want to add a new image to the database press [Y]")
    c = getScan()
    captured = False

    if c.__eq__("Y") or c.__eq__("y"):
        import Camera as camera
        captured = camera.captureImage()

    return captured

def askTrain():

    trained = False

    print("If you want to train the network again press [Y]")
    c = getScan()

    if c.__eq__("Y") or c.__eq__("y"):
        print("\nCreating face-focused images from original-database images...")
        print("Training network...\n")

        trained = train()

    print("\nThe file " + ymlFile + ((" just created will be used.") if trained else (" existing from before will be used.")))
    print("Loading file " + xmlFolderPath + delimiter + xmlFile + "...")
    getLoadedXml()

def cutFaceFromImage(image):

    face_cascade = getLoadedXml()
    gray = imageToGrayscale(image)
    faces = getFacesMultiScale(gray, face_cascade)

    cutted = False
    crop_img = image

    if len(faces) == 1:
        x, y, w, h = faces[0]
        crop_img = image[y:y + h, x:x + w]
        cutted = True
    elif len(faces) > 1:
        print("WARNING: Image with too many faces.")
    else:
        print("WARNING: Image with no faces.")
    return cutted, crop_img

def createCutFacesFromDatabase():
    folder = facesDatasetPath

    imagesToDelete = os.listdir(folder)
    for the_file in imagesToDelete:
        file_path = getFileName(the_file, folder)
        if os.path.isfile(file_path):
            os.remove(file_path)

    images = os.listdir(datasetPath)
    for i in images:
        cutted, cutFace = cutFaceFromImage(loadImage(getFileName(i, datasetPath)))
        if cutted is True:
            cv2.imwrite(getFileName('face_' + i, folder), cutFace)