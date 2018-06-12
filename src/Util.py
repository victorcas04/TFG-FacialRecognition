
# encoding: utf-8

from __future__ import division
import cv2, os, six

delimiter = '\\'
datasetPath = '..'+delimiter+'sources'+delimiter+'dataset'
facesDatasetPath = '..'+delimiter+'sources'+delimiter+'facesDataset'
xmlFolderPath = '..'+delimiter+'sources'+delimiter+'xml'
xmlFile = 'haarcascade_frontalface_default.xml'
recognizerFolderPath = ".." + delimiter + 'sources' + delimiter + 'recognizer'
ymlFile = 'trainedData.yml'
recognizerDict = 'dictionary_ID_labels.txt'
recognizerInfo = 'info.txt'
extensionJPG = '.jpg'
extensionPNG = '.png'
fileDelimiter = ', '

def getScan():
    return six.moves.input()

def getFileName(defaultFile="default.png", folder="..\\sources"):
    return folder + delimiter + defaultFile

def loadImage(fullName=getFileName()):
    print("Loading image " + str(fullName) + "...")
    return cv2.imread(fullName)

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

def getFacesMultiScale(gray):
    return getLoadedXml().detectMultiScale(gray, 1.2, 5, minSize=(gray.shape[0]//10, gray.shape[1]//10))

# Podríamos guardar el diccionario en una variable desde trainer.py, pero de este forma nos aseguramos tener el
#   diccionario guardado en caso de no re-entrenar la red en cada ejecución.
def loadDictIdLabels():
    d = {}
    with open(recognizerFolderPath + delimiter + recognizerDict) as f:
        for line in f:
            p = line.split()
            d[int(p[0])] = p[1]
    return d

def loadInfo(nameImage=None):
    name = " - "; age = " - "; birth_place = " - "; job = " - "
    if nameImage is not None:
        with open(recognizerFolderPath + delimiter + recognizerInfo) as f:
            for line in f:
                    # Ejemplo de lo que nos encontramos en este fichero
                    # alexandra_daddario, Alexandra Daddario, 32, Nueva York, Actriz
                    p = line.split(fileDelimiter)
                    
                    # Para quitar la primera parte del nombre (face_) y quedarnos con el resto
                    #print(p[0].split("face_",1)[1])

                    if p[0].__eq__(nameImage):
                        name = p[1]; age = p[2]; birth_place = p[3]; job = p[4]
                        break
    info = {"name": name, "age": age, "birth_place": birth_place, "job": job}
    return info

'''
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
'''
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

    print("Information about comparison: id= " + str(id) + "   ---   label= " + str(label) + "   ---   coincidence= " + str(p))

    if label is not None:   # NSF
        imgRet = loadImage(getFileName(str(dictIDlabels.get(id)) + extensionJPG, folder=path))
    else:
        imgRet = loadImage(getFileName())

    return imgRet, p, label, loadInfo(label)
    #return imgRet, p, label, loadInfo(id)

def askInfoNewImage():
    print("\nIntroduce the name of the new file (to save on database):\nIf no name is provided, \'new_image_name\' will be used.")
    nFile = getScan()
    if not nFile:
        nFile="new_image_name"
    print("\nIntroduce the name of the person who appears on that image:\nIf no name is provided, \'Default Name\' will be used.")
    name = getScan()
    if not name:
        name="Default Name"
    print("\nIntroduce the age of that person:\nIf no age is provided, \'Default Age\' will be used.")
    age = getScan()
    if not age:
        age="Default Age"
    print("\nIntroduce the city name where he/she was born:\nIf no city name is provided, \'Default City\' will be used.")
    birthplace = getScan()
    if not birthplace:
        birthplace="Default City"
    print("\nIntroduce the actual profession of that person:\nIf no occupation is provided, \'Default Job\' will be used.")
    job = getScan()
    if not job:
        job="Default Job"

    return nFile, name, age, birthplace, job

def writeInfoNewImage(stringInfo):
    with open(recognizerFolderPath + delimiter + recognizerInfo, "a") as f:
        f.write(stringInfo)

def askNewImage():
    print("If you want to add a new image to the database press [Y]")
    c = getScan()
    captured = False

    if c.__eq__("Y") or c.__eq__("y"):
        import Camera as camera
        captured = camera.captureImage()[0]

    if captured:
        return train()
    else:
        return askTrain()

def train():
    import trainer
    import time
    tic = time.time()
    trained, numImages = trainer.train()
    toc = time.time()

    if numImages >= 2:
        print("\nTraining time with " + str(numImages) + " images: " + str(round(toc-tic, 2)) + " seconds.")

    if not trained:
        print("WARNING: Network couldn't be trained.")
    return trained

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
    return trained

def cutFaceFromImage(image):

    gray = imageToGrayscale(image)
    faces = getFacesMultiScale(gray)

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