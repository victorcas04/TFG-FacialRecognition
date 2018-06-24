
# encoding: utf-8

from __future__ import division
import cv2
import Files as files
import TextInterface as txtIf

def imageToGrayscale(image):

    '''
    Convert an image in RGB to grayscale.
    :param image: Image
        Image to convert.
    :return: img: Image
        New image converted.
    '''
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


def imageToThreshold(image):

    '''
    Convert an image in RGB to another one in grayscale, applying a threshold filter.
    :param image: Image
        Image to convert.
    :return: th: Image
        New image converted.
    '''

    '''
    Convert image to grayscale, and then apply a filter.
    The filter can be changed, but the 'ADAPTIVE_THRESH_GAUSSIAN' was better for us.
    '''
    imgB = cv2.medianBlur(imageToGrayscale(image), 5)
    th = cv2.adaptiveThreshold(imgB, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)

    return th


def getFacesMultiScale(gray):

    '''
    Detect all faces in an image.
    We can filter what the program thinks is a face as explained below.
    :param gray: Image
        Image to detect faces from.
    :return: faces: ArrayList<rectangle>
        Arraylist with a rectangle for each face on the image. The rectangles represent:
        x = position on X-axis where the face begins
        y = position on Y-axis where the face begins
        w = width of the face
        h = height of the face
    '''

    '''
    Scale Factor represents which part of the image is analized in each iteration of the process.
    Minimum number of neighbors represents how many rectangles (at least) may take each face.
    Minimum size represents the minimum size that a face can have on the image. In our case, as we are not gonna take 
        long ranged photos, we set this parameter to ignore everything less than a 10% of the image's size.
    '''
    scaleFactor = 1.2
    minNeighbors = 5
    minSize = (gray.shape[0] // 10, gray.shape[1] // 10)

    return files.getLoadedXml().detectMultiScale(gray, scaleFactor, minNeighbors, minSize=minSize)


def train():

    '''
    Print some messages, initialize a time counter and call main Train method.
    :return: trained: boolean
        True if the network could be trained.
    '''

    txtIf.printMessage(txtIf.MESSAGES.TRAINING_NETWORK)
    import Trainer
    import time

    '''
    Count the time the training lasts for researcher purposes.
    '''
    tic = time.time()
    trained, numImages = Trainer.train()
    toc = time.time()

    if numImages >= 2:
        txtIf.printMessage(txtIf.MESSAGES.TRAIN_TIME, numImages, round(toc - tic, 2))

    if not trained:
        txtIf.printError(txtIf.ERRORS.CANNOT_TRAIN_NETWORK)

    '''
    If the network is trained, the new resources are used.
    '''
    if trained:
        txtIf.printMessage(txtIf.MESSAGES.YML_USED, files.ymlFile, trained)
        txtIf.printMessage(txtIf.MESSAGES.LOADING_FILE, files.xmlFolderPath + files.delimiter + files.xmlFile)
        files.getLoadedXml()

    return trained


def askTrain():

    '''
    Ask the user if wants to train the network or not.
    :return: toContinue: boolean
        True if we can carry on with the main program, False if cannot do that.
    '''

    txtIf.printMessage(txtIf.MESSAGES.ASK_TRAIN_NETWORK)
    c = txtIf.getScan()
    toContinue = False

    if c.__eq__("Y") or c.__eq__("y"):

        '''
        If the user wants to train the network...
        '''
        toContinue = train()

    elif len(files.filesOnDir(files.facesDatasetPath)) >= 2:

        '''
        ...if the user doesn't want to train the network and there are at least two image on the database,
            the old resources are used.
        '''
        txtIf.printMessage(txtIf.MESSAGES.YML_USED, files.ymlFile, False)
        txtIf.printMessage(txtIf.MESSAGES.LOADING_FILE, files.xmlFolderPath + files.delimiter + files.xmlFile)
        files.getLoadedXml()
        toContinue = True

    else:

        '''
        ...if the user doesn't want to train the network and there are less than two images on the database, 
            print an error message and exit this part.
        '''
        txtIf.printError(txtIf.ERRORS.NOT_ENOUGH_IMAGES_ON_DATABASE, True)

    return toContinue


def cutFaceFromImage(image):

    '''
    Cut a face from an image (only if there is exactly one).
    :param image: Image
        Image to be cut.
    :return: cutted: boolean
        True if the image could be cropped or False otherwise.
    :return: crop_img: Image
        Image only with a face.
    '''

    gray = imageToGrayscale(image)

    '''
    Get the number of faces on the image.
    '''
    faces = getFacesMultiScale(gray)
    numFaces = len(faces)
    cutted = False
    crop_img = None

    if numFaces == 1:

        '''
        If there are exactly one face on the image, cut it.
        '''
        x, y, w, h = faces[0]
        crop_img = image[y:y + h, x:x + w]
        cutted = True

    else:

        '''
        If there are more or less than one face on the image, print an error message.
        '''
        txtIf.printError(txtIf.ERRORS.IMAGE_TOO_MANY_FACES, numFaces)

    return cutted, crop_img
