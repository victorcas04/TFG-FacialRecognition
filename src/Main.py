
# encoding: utf-8

'''
@author: victorcas
'''

from __future__ import division
import Util as util
import TextInterface as txtIf
from GUI import GUIClass as gui
import Camera as camera

'''
Contains the main method of the program execution.
'''

if __name__ == "__main__":

    txtIf.printMessage(txtIf.MESSAGES.TITLE)

    '''
    Main loop to run the program until the user exits.
    '''

    while True:
        askTrain = True

        '''
        Ask the user if wants to add a new image to the database.
        On loop to avoid run the program for each image to add.
        '''

        while txtIf.askNewImage():
            if camera.captureImage()[0]:
                '''
                If we add one image or more, the network will be trained without asking the user. 
                '''
                askTrain = False

        if (util.askTrain() if askTrain else util.train()):
            '''
            Ask the user if wants to recognize someone from file, from a single camera shot or in real-time.
            '''
            txtIf.printMessage(txtIf.MESSAGES.ASK_CAMERA_FILE_REALTIME)
            c = txtIf.getScan()

            guiMain = None
            realTime = False

            if c.__eq__("C") or c.__eq__("c"):
                '''
                If the user press [C], take a picture from camera to compare it.
                If 'captureToCompare' is set to 'False', the photo will be taken to save on the database.
                '''
                photoOriginal = camera.captureImage(captureToCompare=True)[1]

            elif c.__eq__("X") or c.__eq__("x"):
                '''
                If the user press [X], exit this part of the program and go to the end.
                '''
                realTime = True

            elif c.__eq__("F") or c.__eq__("f"):
                '''
                If the user press [F], load an image from a file in the system.
                A new interface window is created, but is destroyed after we take a file, 
                    so no problems with multiple window objects from tKinter.
                '''
                txtIf.printMessage(txtIf.MESSAGES.INITIALIZING_INTERFACE)
                guiMain = gui.getInstance()
                photoOriginal = guiMain.loadImageByGUI()

            else:
                '''
                If we press [R] (or any other button), the real-time recognition process will begin.
                '''
                import RecognizerRealTime as rrt
                rrt.compareInRealTime()
                realTime = True

            '''
            If we have pressed [C] or [F], the next process will be done. Pass it otherwise.
            '''

            if not realTime:
                '''
                We have to initialize the main window of the interface here and not before because of some 
                    compatibility problems between tKinter and OpenCV.
                '''
                if guiMain is None:
                    txtIf.printMessage(txtIf.MESSAGES.INITIALIZING_INTERFACE)
                    guiMain = gui.getInstance()
                guiMain.createMainWindow()
                guiMain.fixedSize()
                guiMain.createTop_BottomPanel()

                '''
                Cut the image to obtain only the face.
                '''
                cutted, pOri = util.cutFaceFromImage(photoOriginal)

                if cutted:
                    '''
                    If we could cut a face, compare that face and display on the interface.
                    '''
                    import CompareImages as compareImages

                    '''
                    The return of this method gives us the image (i), a percentage (p) and the name of the image (n).
                    '''
                    i, p, n = compareImages.compare(pOri)

                    guiMain.setTitleAndProgress(p, n)
                    guiMain.setImage(image=pOri)
                    guiMain.setImage(image=i, left=False)

                else:
                    '''
                    If a face cannot be cut (too many faces or not at all), display default image.
                    '''
                    guiMain.setTitleAndProgress()
                    guiMain.setImage(image=photoOriginal)
                    guiMain.setImage(left=False)

                guiMain.displayWindow()

        '''
        Ask the user if wants to continue again with same process or to exit the application.
        '''
        if txtIf.askExitMain():
            break
