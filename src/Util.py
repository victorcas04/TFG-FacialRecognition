
import cv2, wx, sys, time, math, os
import src.TrainMachine.CompareImages as imgCompare
import src.TrainMachine.trainer as trainer

datasetPath = '../sources/dataset'
facesDatasetPath = '../sources/facesDataset'
xmlFolderPath = '../sources/xml'
xmlFile = 'haarcascade_frontalface_default.xml'
recognizerFolderPath = 'TrainMachine/recognizer'
ymlFile = 'trainedData.yml'
recognizerDict = 'dictionary_ID_labels.txt'

def getScan():
    ri = input()
    return ri

def getDisplaySize():
    app = wx.App(False)
    w, h = wx.GetDisplaySize()
    return w, h

def getFileName(defaultFile="default.png", folder="../sources"):
    return folder + '/' + defaultFile

def saveImage(image, path=getFileName("savedDefault.png")):
    print("\nGuardando imágen en: " + str(path) + "\n")
    cv2.imwrite(path, image);

def loadImage(fullName=getFileName()):
    print("Cargando imágen " + str(fullName))
    return cv2.imread(fullName)

def loadImageByGUI(gui):
    return loadImage(gui.selectFile())

def imageToGrayscale(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

def getLoadedXml():
    return cv2.CascadeClassifier(getFileName(xmlFile, xmlFolderPath))

def getLoadedYml():
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    try:
        recognizer.read(getFileName(ymlFile, recognizerFolderPath))
    except:
        print("Red no entrenada. Ejecute de nuevo tras entrenar la red.")

def getFacesMultiScale(gray, faceCascade):
    return faceCascade.detectMultiScale(gray, 1.2, 5, minSize=(int(gray.shape[0]/10), int(gray.shape[1]/10)))

def printMenuFaceInBox(fromCamera=True):

    print("\nOPCIONES:\n")
    print("Pulsa [I] para información general.")
    print("Pulsa [Q] para salir.")
    if fromCamera:
        print("Pulsa [P] para pausar la cámara.")
        print("Pulsa [SPACE] para reanudar la cámara (sólo si estaba pausada).")
        print("Pulsa [C] para capturar el frame actual y cerrar la cámara.\n")


def faceInBoxVideo():

    imageToReturn = None
    maxInt = sys.maxsize

    print("Cargando fichero " + xmlFolderPath + '/' + xmlFile + "...")
    face_cascade = getLoadedXml()

    print("Inicializando cámara...")
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FPS, maxInt)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, maxInt)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, maxInt)
    # Esperamos dos segundos para que la cámara termine de inicializarse y no tomar datos basura
    time.sleep(2)

    print("Mostrando imágen en tiempo real...")

    printMenuFaceInBox()

    while True:

        numFaces = 0
        ret, img = cap.read()
        img = cv2.flip(img, 1)
        gray = imageToGrayscale(img)
        faces = getFacesMultiScale(gray, face_cascade)

        rectangleThickness = int((img.shape[0] + img.shape[1]) / (100 * 2 * math.pi))   # 20-30
        rectangleColor = (255, 0, 0)

        for (x, y, w, h) in faces:
            numFaces = numFaces + 1
            cv2.rectangle(img, (x, y), (x + w, y + h), rectangleColor, rectangleThickness)

        cv2.imshow("Imagen en tiempo real", img)
        k = cv2.waitKey(1)
        
        ### Press [I] for info.
        if k == ord('i'):
            print("\n - " + str(numFaces) + " - person(s) recognized.")
            printMenuFaceInBox()

        ### Press [Q] to exit.
        if k == ord('q'):
            break

        ### Press [P] to pause camera reading.
        ### Press [SPACE] to resume camera reading.
        if k == ord('p'):
            while cv2.waitKey(0) != ord(' '):
                print("Press [SPACE] to resume camera reading.")

        ### Press [C] to take the actual frame and exit.
        if numFaces == 1 and k == ord('c'):
            imageToReturn = img
            break

    cap.release()
    cv2.destroyAllWindows()
    return imageToReturn

def resizeFaceImage(image, aspect_ratio=2):
    h, w = getDisplaySize()
    prop = w/image.shape[1]
    newSize = (int((prop*image.shape[0])/aspect_ratio), int((prop*image.shape[1])/aspect_ratio))
    newImage = cv2.resize(image, (newSize[1], newSize[0]))
    return newImage

def displayInterfaceWindow(gui, photoFromCamera=None, photoFromDatabase=None, percentage=0.0):

    percentageString = str(percentage) + "%"
    print("\nMostrando resultado con un " + percentageString + " de coincidencia.\n")

    gui.createTop_BottomPanel(photoFromCamera, photoFromDatabase, getDisplaySize(), percentage)
    gui.displayWindow()

# Podríamos guardar el diccionario en una variable desde trainer.py, pero de este forma nos aseguramos tener el
#   diccionario guardado en caso de no re-entrenar la red en cada ejecución.
def loadDictIdLabels():
    d = {}
    with open(recognizerFolderPath + '/' + recognizerDict) as f:
        for line in f:
            (k, v) = line.split()
            d[int(k)] = v
    return d

def compare(img, path=facesDatasetPath):
    xml = getLoadedXml()
    reco = cv2.face.LBPHFaceRecognizer_create()

    compareClass = imgCompare.CompareImagesClass(xml, reco)
    dictIDlabels = loadDictIdLabels()
    label = "NSF"   # No Such File

    print("Comparando imágen con las de la base de datos...")

    gray = imageToGrayscale(img)
    id, p = compareClass.compareAll(gray)

    if id > -1:
        imgsOr = os.listdir(datasetPath)
        label = imgsOr[id].split(".")[0]
    print("id= " + str(id) + "   ---   etiqueta= " + str(label) + "   ---   coincidencia= " + str(p))

    if label is not "NSF":
        imgRet = loadImage(getFileName(str(dictIDlabels.get(id)) + ".jpg", folder=path))
    else:
        print("\nNo se ha podido reconocer ninguna cara.")
        imgRet = loadImage(getFileName())

    return imgRet, p, label

def train(path):
    return trainer.train(path)

def askTrain(path):

    trained = False

    print("¿Se han añadido nuevas imágenes o quieres reentrenar la red de nuevo? ( S / N )")
    c = getScan()

    if not c.__eq__("N") and not c.__eq__("n"):
        print("\nCreando imágenes de reconocimiento a partir de la base de datos...")
        print("Entrenando red...\n")

        createCutFacesFromDatabase()
        trained = train(path)

        if not trained:
            print("WARNING: No se ha podido entrenar la red.")

    print("\n" + ("Se utilizará el fichero " + ymlFile + " creado.") if trained else ("\nSe utilizará el fichero " + ymlFile + " existente."))

def cutFaceFromImage(image):

    face_cascade = getLoadedXml()
    gray = imageToGrayscale(image)
    faces = getFacesMultiScale(gray, face_cascade)

    crop_img = None

    if len(faces) == 1:
        x, y, w, h = faces[0]
        crop_img = image[y:y + h, x:x + w]
    elif len(faces) > 1:
        print("WARNING: Imágen con demasiados rostros.")
    else:
        print("WARNING: No se han detectado rostros.")

    return crop_img

def createCutFacesFromDatabase():

    folder = facesDatasetPath

    if not os.path.exists(folder):
        os.makedirs(folder)

    imagesToDelete = os.listdir(folder)
    for the_file in imagesToDelete:
        file_path = getFileName(the_file, folder)
        if os.path.isfile(file_path):
            os.remove(file_path)

    images = os.listdir(datasetPath)
    for i in images:
        cutFace = cutFaceFromImage(loadImage(getFileName(i, datasetPath)))
        if cutFace is not None:
            cv2.imwrite(getFileName('face_' + i, folder), cutFace)
