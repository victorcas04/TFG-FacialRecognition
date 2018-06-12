
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

def askNewImage():
    txtIf.printMessage(txtIf.MESSAGES.ASKADDIMAGES)
    c = txtIf.getScan()
    captured = False

    if c.__eq__("Y") or c.__eq__("y"):
        import Camera as camera
        captured = camera.captureImage()[0]

    if captured:
        return train()
    else:
        return askTrain()

def train():
    import Trainer
    import time
    tic = time.time()
    trained, numImages = Trainer.train()
    toc = time.time()

    if numImages >= 2:
        txtIf.printMessage(txtIf.MESSAGES.TRAINTIME, numImages, round(toc - tic, 2))

    if not trained:
        txtIf.printError(txtIf.ERRORS.CANNOTTRAINNETWORK)
    return trained

def askTrain():
    trained = False

    txtIf.printMessage(txtIf.MESSAGES.ASKTRAINNETWORK)
    c = txtIf.getScan()

    if c.__eq__("Y") or c.__eq__("y"):
        txtIf.printMessage(txtIf.MESSAGES.TRAININGNETWROK)

        trained = train()

    txtIf.printMessage(txtIf.MESSAGES.YMLUSED, files.ymlFile, trained)
    txtIf.printMessage(txtIf.MESSAGES.LOADINGFILE, files.xmlFolderPath + files.delimiter + files.xmlFile)
    files.getLoadedXml()
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
        txtIf.printError(txtIf.ERRORS.IMAGETOOMANYFACES)
    else:
        txtIf.printError(txtIf.ERRORS.IMAGENOFACES)
    return cutted, crop_img
