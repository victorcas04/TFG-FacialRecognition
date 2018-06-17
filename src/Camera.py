
# encoding: utf-8

import cv2
import Util as util
import Files as files
import TextInterface as txtIf

# max resolution with integrated webcam (sony vaio VPCF13A4E): 640 X 480
# max resolution with external camera (logitech WEBCAM C170): 1024 X 768
resH = 768
resW = 1024

#  [0] para la webcam integrada en el portatil o una externa en caso de haber
#  [1] para la webcam integrada en el portatil en caso de que haya una externa conectada
# [-1] para menú (no recomendado)
cameraIdx = 0

def initializeCamera():

    txtIf.printMessage(txtIf.MESSAGES.INITIALIZING_CAMERA)

    cap = cv2.VideoCapture(cameraIdx)

    if not cap.isOpened():
        txtIf.printError(txtIf.ERRORS.CAMERA_NOT_INITIALIZED)
        return None

    cap.set(cv2.CAP_PROP_FPS, int(60))
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, resH)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, resW)

    txtIf.printMessage(txtIf.MESSAGES.RESOLUTION_CAMERA, [int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)), int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))])
     
    # Esperamos dos segundos para que la cámara termine de inicializarse y no tomar datos basura
    import time
    time.sleep(2)
    return cap

def captureImage(captureToCompare=False):
    import math
    import numpy as np
    # Para mostrar informacion sobre la version de cv
    # print(cv2.getBuildInformation())

    imageToReturn = None
    captured = False

    cap = initializeCamera()
    if cap is None:
        return files.loadImage()

    txtIf.printMessage(txtIf.MESSAGES.IMAGE_IN_REALTIME)
    txtIf.printMenuFaceInBox()

    while True:
        numFaces = 0
        ret, frame = cap.read()
        frame = cv2.flip(frame, 1)
        frameToShow = np.copy(frame)

        gray = util.imageToGrayscale(frameToShow)
        faces = util.getFacesMultiScale(gray)

        rectangleThickness = int((frameToShow.shape[0] + frameToShow.shape[1]) / (100 * 2 * math.pi))  # 20-30
        rectangleColor = (255, 0, 0)

        for (x, y, w, h) in faces:
            numFaces = numFaces + 1
            cv2.rectangle(frameToShow, (x, y), (x + w, y + h), rectangleColor, rectangleThickness)

        cv2.imshow('Real-time image', frameToShow)
        k = cv2.waitKey(1)

        ### Press [I] for info.
        if k == ord('i'):
            if numFaces != 1:
                txtIf.printError(txtIf.ERRORS.IMAGE_TOO_MANY_FACES, numFaces)
            txtIf.printMenuFaceInBox()

        ### Press [Q] to exit.
        if k == ord('q'):
            break

        ### Press [P] to pause camera reading.
        ### Press [SPACE] to resume camera reading.
        if k == ord('p'):
            txtIf.printMessage(txtIf.MESSAGES.CAMERA_PAUSED)
            while cv2.waitKey(0) != ord(' '):
                txtIf.printMessage(txtIf.MESSAGES.CAMERA_PAUSED_2)

        ### Press [C] to take the actual frame and exit if there is only 1 person.
        if k == ord('c'):
            if numFaces == 1:
                imageToReturn = frame
                break
            else:
                txtIf.printError(txtIf.ERRORS.IMAGE_TOO_MANY_FACES, numFaces)

    cap.release()
    cv2.destroyAllWindows()

    if imageToReturn is not None:
        captured = True
        if captureToCompare is False:
            captured = files.doWhenNewImage(imageToReturn)

    if imageToReturn is None and captureToCompare is True:
        imageToReturn = files.loadImage()

    return captured, imageToReturn