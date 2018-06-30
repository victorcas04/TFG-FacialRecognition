
# encoding: utf-8

'''
@author: victorcas
'''

from __future__ import division
import cv2
import Files as files
import TextInterface as txtIf
import CompareImages as compareImages
from GUI import GUIClass as gui
import Camera as camera

'''
The speed at which the interface is updated.
With a powerful pc can be put down to 0.1, less than that value is not recommended because interface isn't 
    updated in time and sometimes there are trash data. 
'''
segBetweenFrames = 0.5

def compareInRealTime():

    '''
    Compare an image, taken in real time with the database.
    Works as the 'CompareImages' worked with a single image, but updating the image and the data associated.
    '''

    txtIf.printMessage(txtIf.MESSAGES.INITIALIZING_INTERFACE)

    '''
    Initialize interface.
    '''
    guiMain = gui.getInstance()
    guiMain.createMainWindow("REAL-TIME RECOGNITION", realTime=True)
    guiMain.fixedSize()
    guiMain.createTop_BottomPanel()

    '''
    Initialize camera. If cannot be open, cancel the process and exit to main menu.
    '''
    cap = camera.initializeCamera()
    if cap is None:
        return
    import Util as util
    import math

    '''
    Method that takes the actual frame from the camera and updates the interface.
    '''
    def show_frame():
        ret, frame = cap.read()
        frame = cv2.flip(frame, 1)

        if frame is not None:
            '''
            Resize the image to show because it needs to be bigger than in other cases to avoid empty spaces on interface.
            '''
            frameToShow = guiMain.resizeFaceImage(frame, aspect_ratio=1.5)

            '''
            The same process as in 'Camera.captureImage()': obtain all faces on image and put a rectangle over them.
            '''
            gray = util.imageToGrayscale(frameToShow)
            faces = util.getFacesMultiScale(gray)
            rectangleThickness = int((frameToShow.shape[0] + frameToShow.shape[1]) / (100 * 2 * math.pi))  # 20-30
            rectangleColor = (255, 0, 0)
            for (x, y, w, h) in faces:
                cv2.rectangle(frameToShow, (x, y), (x + w, y + h), rectangleColor, rectangleThickness)

            '''
            Set the image in real time to the left side of the interface.
            '''
            guiMain.setImage(image=frameToShow, staticImage=False)

            '''
            Try to cut the face from the image.
            '''
            cutted, pOri = util.cutFaceFromImage(frame)

            if cutted:
                '''
                If we could cut the face, compare it.
                pOri = result image from the comparison
                p = percentage of the comparison
                n = name of the image on the database
                '''
                pOri, p, n = compareImages.compare(pOri)

                if p <= 0:
                    '''
                    If the percentage obtained is less or equals to 0, it means there were no results on the database, 
                        so load a default image.
                    '''
                    pOri = files.loadImage()
                    n = None
            else:
                '''
                If we couldn't cut the face (too many or not at all), set default values.
                '''
                p = 0;
                n = None

            '''
            Set information on the interface.
            '''
            guiMain.setTitleAndProgress(p, n)

            '''
            Set the image obtained as the result to the right side of the interface.
            '''
            guiMain.setImage(image=pOri, left=False)

            '''
            Execute this method again every 0.5 seconds (value passed to 'after()' is in milliseconds).
            '''
            guiMain.myLabelC.after(int(segBetweenFrames * 1000), show_frame)
        else:
            txtIf.printError(txtIf.ERRORS.CAMERA_DISCONNECTED)
            guiMain.window.destroy()

    show_frame()

    '''
    Display main window in real time, and when we close it, the camera is closed.
    '''
    guiMain.displayWindow()
    cap.release()
