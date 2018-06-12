
# encoding: utf-8

import sys, time, math, cv2
import Util as util

delimiter = util.delimiter
maxInt = sys.maxsize

def initializeCamera(indexCamera):
    maxInt = sys.maxsize

    print("Initializing camera...")

    cap = cv2.VideoCapture(indexCamera)

    if not cap.isOpened():
        print("Camera couldn't be turned on.")
        return None

    cap.set(cv2.CAP_PROP_FPS, maxInt)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, maxInt)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, maxInt)

    # Esperamos dos segundos para que la cámara termine de inicializarse y no tomar datos basura
    time.sleep(2)
    return cap


def saveImage(image, path):
    print("\nSaving image in: " + str(path) + "...\n")
    cv2.imwrite(path, image);

def printMenuFaceInBox(fromCamera=True):

    print("\nOPTIONS:\n")
    print("Press [I] to display general information.")
    print("Press [Q] to quit.")
    if fromCamera:
        print("Press [P] to pause the camera.")
        print("Press [SPACE] to resume the camera (only if it was paused).")
        print("Press [C] to capture the actual frame and close the camera.\n")

def captureImage(indexCamera=0, captureToCompare=False):

    # Muestra informacion sobre la version de cv
    # print(cv2.getBuildInformation())

    imageToReturn = None

    cap = initializeCamera(indexCamera)
    if cap is None:
        return util.loadImage()

    print("Displaying image in real-time...")
    printMenuFaceInBox()

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
            print("\n[" + str(numFaces) + "] faces were found in the image.\nThere must be exactly one (1) person to be able to capture the image.")
            printMenuFaceInBox()

        ### Press [Q] to exit.
        if k == ord('q'):
            break

        ### Press [P] to pause camera reading.
        ### Press [SPACE] to resume camera reading.
        if k == ord('p'):
            print("CAMERA PAUSED")
            while cv2.waitKey(0) != ord(' '):
                print("CAMERA PAUSED: Press [SPACE] to resume camera reading.")

        ### Press [C] to take the actual frame and exit.
        if numFaces == 1 and k == ord('c'):
            imageToReturn = img
            break

    cap.release()
    cv2.destroyAllWindows()

    if imageToReturn is not None and captureToCompare is False:
    	iName, name, age, bPlace, job = util.askInfoNewImage()
    	util.writeInfoNewImage( '\n'+iName+util.fileDelimiter+name+util.fileDelimiter+age+util.fileDelimiter+bPlace +util.fileDelimiter+job)
    	util.saveImage(img, util.datasetPath + util.delimiter + iName + util.extensionJPG)
    	return True, None

    captured = True

    if imageToReturn is None:
    	captured = False
    	imageToReturn = util.loadImage()

    return captured, imageToReturn