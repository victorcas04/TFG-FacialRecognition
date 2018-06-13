
# encoding: utf-8

import sys, time, math, cv2
import Util as util
import Files as files
import TextInterface as txtIf

delimiter = files.delimiter
maxInt = sys.maxsize

def initializeCamera(indexCamera):
    maxInt = sys.maxsize

    txtIf.printMessage(txtIf.MESSAGES.INITIALIZING_CAMERA)

    cap = cv2.VideoCapture(indexCamera)

    if not cap.isOpened():
        txtIf.printError(txtIf.ERRORS.CAMERA_NOT_INITIALIZED)
        return None

    cap.set(cv2.CAP_PROP_FPS, maxInt)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, maxInt)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, maxInt)

    # Esperamos dos segundos para que la cámara termine de inicializarse y no tomar datos basura
    time.sleep(2)
    return cap

def captureImage(indexCamera=0, captureToCompare=False):

    # Para mostrar informacion sobre la version de cv
    # print(cv2.getBuildInformation())

    imageToReturn = None

    cap = initializeCamera(indexCamera)
    if cap is None:
        return files.loadImage()

    txtIf.printMessage(txtIf.MESSAGES.IMAGE_IN_REALTIME)
    txtIf.printMenuFaceInBox()

    while True:
        numFaces = 0
        ret, img = cap.read()

        img = cv2.flip(img, 1)
        gray = util.imageToGrayscale(img)
        faces = util.getFacesMultiScale(gray)

        rectangleThickness = int((img.shape[0] + img.shape[1]) / (100 * 2 * math.pi))  # 20-30
        rectangleColor = (255, 0, 0)

        for (x, y, w, h) in faces:
            numFaces = numFaces + 1
            cv2.rectangle(img, (x, y), (x + w, y + h), rectangleColor, rectangleThickness)

        cv2.imshow('Real-time image', img)
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
                imageToReturn = img
                break
            else:
                txtIf.printError(txtIf.ERRORS.IMAGE_TOO_MANY_FACES, numFaces)

    cap.release()
    cv2.destroyAllWindows()

    if imageToReturn is not None and captureToCompare is False:
        #iName, name, age, bPlace, job = askInfoNewImage()
        files.doWhenNewImage(imageToReturn)
        return True, None

    captured = True
    if imageToReturn is None:
        captured = False
        imageToReturn = files.loadImage()

    return captured, imageToReturn