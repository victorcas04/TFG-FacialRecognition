
# encoding: utf-8

from __future__ import division
import cv2
import Files as files
import TextInterface as txtIf

def imageToGrayscale(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

def imageToThreshold(image):
    imgB = cv2.medianBlur(imageToGrayscale(image), 5)
    th = cv2.adaptiveThreshold(imgB, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
    return th

def getFacesMultiScale(gray):
    scaleFactor = 1.2
    minNeighbors = 5
    return files.getLoadedXml().detectMultiScale(gray, scaleFactor, minNeighbors, minSize=(gray.shape[0] // 10, gray.shape[1] // 10))

def train():
    txtIf.printMessage(txtIf.MESSAGES.TRAINING_NETWORK)
    import Trainer
    import time
    tic = time.time()
    trained, numImages = Trainer.train()
    toc = time.time()

    if numImages >= 2:
        txtIf.printMessage(txtIf.MESSAGES.TRAIN_TIME, numImages, round(toc - tic, 2))

    if not trained:
        txtIf.printError(txtIf.ERRORS.CANNOT_TRAIN_NETWORK)

    if trained:
        txtIf.printMessage(txtIf.MESSAGES.YML_USED, files.ymlFile, trained)
        txtIf.printMessage(txtIf.MESSAGES.LOADING_FILE, files.xmlFolderPath + files.delimiter + files.xmlFile)
        files.getLoadedXml()
    return trained

def askTrain():
    txtIf.printMessage(txtIf.MESSAGES.ASK_TRAIN_NETWORK)
    c = txtIf.getScan()
    toContinue = False

    if c.__eq__("Y") or c.__eq__("y"):
        toContinue = train()
    elif len(files.filesOnDir(files.facesDatasetPath)) >= 2:
        txtIf.printMessage(txtIf.MESSAGES.YML_USED, files.ymlFile, False)
        txtIf.printMessage(txtIf.MESSAGES.LOADING_FILE, files.xmlFolderPath + files.delimiter + files.xmlFile)
        files.getLoadedXml()
        toContinue = True
    else:
        txtIf.printError(txtIf.ERRORS.NOT_ENOUGH_IMAGES_ON_DATABASE, True)

    return toContinue

def cutFaceFromImage(image):

    gray = imageToGrayscale(image)
    faces = getFacesMultiScale(gray)
    numFaces = len(faces)
    cutted = False
    crop_img = None

    if numFaces == 1:
        x, y, w, h = faces[0]
        crop_img = image[y:y + h, x:x + w]
        cutted = True
    else:
        txtIf.printError(txtIf.ERRORS.IMAGE_TOO_MANY_FACES, numFaces)

    return cutted, crop_img
