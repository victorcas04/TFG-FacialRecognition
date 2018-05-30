
# encoding: utf-8

import sys, time, math, cv2
import Util as util

delimiter = util.delimiter
folderDataset = ".."+delimiter+"sources"+delimiter+"dataset"+delimiter
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

def captureImage():
    #print("Introduce tu nombre:")
    #name = util.getScan()
    name = "zzzzz"

    cap = initializeCamera(0)

    print("Displaying image in real-time...")
    print("Press [C] to save the image.\nPress [Q] to quit without saving ant new image.")

    enBucle=True
    while enBucle:
        ret, img = cap.read()
        img = cv2.flip(img, 1)
        cv2.imshow("real_time_image", img)
        k=cv2.waitKey(1)
        if k == ord('c'):
            util.saveImage(img, folderDataset + name+".jpg")
            captured=True
            enBucle=False
        elif k == ord('q'):
            print("Exiting...")
            captured = False
            enBucle=False

    cap.release()
    cv2.destroyAllWindows()
    return captured


def faceInBoxVideo(indexCamera=-1):

    # Muestra informacion sobre la version de cv
    # print(cv2.getBuildInformation())

    imageToReturn = None

    face_cascade = util.getLoadedXml()

    cap = initializeCamera(indexCamera)
    if cap is None:
        return util.loadImage()

    print("Displaying image in real-time...")

    util.printMenuFaceInBox()

    while True:
        numFaces = 0
        ret, img = cap.read()

        img = cv2.flip(img, 1)
        gray = util.imageToGrayscale(img)
        faces = util.getFacesMultiScale(gray, face_cascade)

        rectangleThickness = int((img.shape[0] + img.shape[1]) / (100 * 2 * math.pi))  # 20-30
        rectangleColor = (255, 0, 0)

        for (x, y, w, h) in faces:
            numFaces = numFaces + 1
            cv2.rectangle(img, (x, y), (x + w, y + h), rectangleColor, rectangleThickness)

        cv2.imshow('Real-time image', img)
        k = cv2.waitKey(1)

        ### Press [I] for info.
        if k == ord('i'):
            print("\n[" + str(numFaces) + "] faces were found in the image.")
            util.printMenuFaceInBox()

        ### Press [Q] to exit.
        if k == ord('q'):
            imageToReturn = util.loadImage()
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
    return imageToReturn