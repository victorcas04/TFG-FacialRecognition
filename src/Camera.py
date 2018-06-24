
# encoding: utf-8

'''
@author: victorcas
'''

import cv2
import Util as util
import Files as files
import TextInterface as txtIf

'''
The maximum resolution with the integrated webcam (from Sony Vaio VPCF13A4E in our case): [640 X 480]
The maximum resolution with an external camera (Logitech WEBCAM C170 in our case): [1024 X 768]

If we know the maximum resolution from our camera, edit this values.
If we don't know it, just ignore this and a default value will be taken ([640 X 480]).
'''
resH = 768
resW = 1024

'''
To choose a camera, just change the camera index below.

Use [0] to use the first external camera installed. If no external cameras are installed, 
    it will use the integrated camera.
    
Use [1] to willfully use the integrated camera while another external camera is installed.

Use [-1] to display a menu with all the cameras installed (integrated and external).
    Not recommended because of some problems while displaying the image.
'''
cameraIdx = 0


def initializeCamera():

    '''
    Method that initializes the camera with index=cameraIdx and returns it (if available, returns None otherwise).
    :return: cap: VideoCapture
        VideoCapture object with the camera initialized or None otherwise.
    '''

    txtIf.printMessage(txtIf.MESSAGES.INITIALIZING_CAMERA)

    '''
    Get the camera with given index.
    '''
    cap = cv2.VideoCapture(cameraIdx)

    '''
    If camera couldn't be open, print error message and return None.
    '''
    if not cap.isOpened():
        txtIf.printError(txtIf.ERRORS.CAMERA_NOT_INITIALIZED)
        return None

    '''
    If camera could be open, initialize parameters (FPS fixed at 60 to get better user experience).
    '''
    cap.set(cv2.CAP_PROP_FPS, int(60))
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, resH)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, resW)

    txtIf.printMessage(txtIf.MESSAGES.RESOLUTION_CAMERA, [int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)), int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))])

    '''
    Wait a few seconds to let the camera finish initializing and avoid taking trash data.
    '''
    import time
    time.sleep(2)

    return cap


def captureImage(captureToCompare=False):

    '''
    Method that captures an image to save it to the database or to compare it.
    :param captureToCompare: boolean
        If True, the image is returned to be compared.
        If False, no image is returned, but extra information is asked for to save the image in the database.
    :return: captured: boolean
        False if there was any problem, True otherwise.
    :return: imageToReturn: Image
        Image captured in case we had to return it, None otherwise.
    '''

    import math
    import numpy as np
    imageToReturn = None
    captured = False

    '''
    Get the camera initialized and continue, or return default image.
    '''
    cap = initializeCamera()
    if cap is None:
        return files.loadImage()

    '''
    Print main options to use with the camera.
    '''
    txtIf.printMessage(txtIf.MESSAGES.IMAGE_IN_REALTIME)
    txtIf.printMenuFaceInBox()

    '''
    Loop to display image in real-time, so the user knows exactly what frame is getting captured.
    '''
    while True:
        numFaces = 0

        '''
        Read actual frame.
        '''
        ret, frame = cap.read()

        '''
        Flip image to display it correctly (otherwise the right side of the image will be our left and viceversa).
        '''
        frame = cv2.flip(frame, 1)
        frameToShow = np.copy(frame)

        '''
        Need to convert image to gray so we can work with it.
        '''
        gray = util.imageToGrayscale(frameToShow)

        '''
        Get all the faces from the image (it's an array of rectangles (x, y, w, h)).
        '''
        faces = util.getFacesMultiScale(gray)

        '''
        Set parameters to personalize rectangles displayed over the faces (thickness changes automatically depending on
            the size of the image, and color is blue by default, but can be changed).
        '''
        rectangleThickness = int((frameToShow.shape[0] + frameToShow.shape[1]) / (100 * 2 * math.pi))  # 20-30
        rectangleColor = (255, 0, 0)

        '''
        Count the number of faces and set rectangles over the image.
        '''
        for (x, y, w, h) in faces:
            numFaces = numFaces + 1
            cv2.rectangle(frameToShow, (x, y), (x + w, y + h), rectangleColor, rectangleThickness)

        '''
        Display the image we are recording with rectangles on it for each face.
        '''
        cv2.imshow('Real-time image', frameToShow)
        k = cv2.waitKey(1)

        '''
        If [I] is press, some information will be displayed on text interface.
        '''
        if k == ord('i'):
            if numFaces != 1:
                txtIf.printError(txtIf.ERRORS.IMAGE_TOO_MANY_FACES, numFaces)
            txtIf.printMenuFaceInBox()

        '''
        If [Q] is press, exit loop without take any frame.
        '''
        if k == ord('q'):
            break

        '''
        If [P] is press, pause camera reading at this point.
            The camera will remain paused until we press [SPACE].
            If any other key apart from [SPACE] is press during the pause, a message will be displayed.
        '''
        if k == ord('p'):
            txtIf.printMessage(txtIf.MESSAGES.CAMERA_PAUSED)
            while cv2.waitKey(0) != ord(' '):
                txtIf.printMessage(txtIf.MESSAGES.CAMERA_PAUSED_2)

        '''
        If [C] is press, check if the number of faces on the image is one.
            If that's the case take that frame and exit loop.
            If more (or none) faces are in the image, a error message will be shown. 
        '''
        if k == ord('c'):
            if numFaces == 1:
                imageToReturn = frame
                break
            else:
                txtIf.printError(txtIf.ERRORS.IMAGE_TOO_MANY_FACES, numFaces)

    '''
    Close the camera and destroy the window created to display the image in real-time.
    '''
    cap.release()
    cv2.destroyAllWindows()

    '''
    If an image was taken...
    '''
    if imageToReturn is not None:
        captured = True
        if captureToCompare is False:
            '''
            ...if it was taken to save to database, ask the user for more data. If something goes wrong in
                that process, 'captured' will be false so any images are saved.
            '''
            captured = files.doWhenNewImage(imageToReturn)

    '''
    If no image was taken, and if the purpose of this was to compare it, load the default image.
    '''
    if imageToReturn is None and captureToCompare is True:
        imageToReturn = files.loadImage()

    return captured, imageToReturn