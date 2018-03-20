

import src.Test.TestsImages as tstImages
import src.Test.TestsPlaceholders as tstPlaceholders
import src.Test.TestsVariables as tstVariables
import src.Util as util

import cv2
import numpy as np
import os, time
import sqlite3

class TestClass(object):

    orchid = util.getFileName("MarshOrchid.jpg")
    meDNI = util.getFileName("FOTO_DNI_1.jpg")
    default = util.getFileName()

    # File from: https://github.com/opencv/opencv/blob/master/data/haarcascades/
    # Repository with files for research and academic purposes
    cascadeXmlFile = "haarcascade_frontalface_default.xml"
    #cascadeXmlFile = "haarcascade_profileface.xml"

    '''
    Tutorials from https://www.tensorflow.org and https://learningtensorflow.com/
    
    '''

    def testVariables(self):
        tstVariables.testConstants()
        tstVariables.testVariables1()
        tstVariables.testVariables2()
        tstVariables.testVariables3()
        tstVariables.testVariables4()

    def testPlaceholders(self):
        tstPlaceholders.testPlaceholders1()
        tstPlaceholders.testPlaceholders2(self.default)
        tstPlaceholders.testPlaceholders3(self.default)
        tstPlaceholders.testPlaceholders4(self.default)

    def testImages(self):
        tstImages.testImages1(self.default)
        tstImages.testImages2(self.default)
        tstImages.testImages3(self.default)
        tstImages.testImages4(self.default)
        tstImages.testImages5(self.default)
        tstImages.testImages6(self.meDNI, nShots=4)
        tstImages.testThreshold(self.meDNI)

    def testActual(self, photoName):
        print("\nTest Actual\n")

        self.faceInBox(photoName)

        pass

    def faceInBox(self, photoName):

        face_cascade = cv2.CascadeClassifier(util.getFileName(self.cascadeXmlFile))

        ''' TODO CAM
        cap = cv2.VideoCapture(0)
        cap.set(cv2.CAP_PROP_FPS, 99999)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 99999)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 99999)
        time.sleep(2)
        '''

        while True:

            sampleNum = 0
            # TODO CAM
            #ret, img = cap.read()
            img = cv2.imread(photoName)

            gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
            faces = face_cascade.detectMultiScale(gray, 1.3, 5)
            for (x, y, w, h) in faces:
                sampleNum = sampleNum + 1
                cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
                # TODO CAM
                #cv2.waitKey(10)
            imageResized, imageResizedString = util.resizeImage(img)
            cv2.imshow(" - " + str(sampleNum) + " - person(s) recognized.", imageResized)

            ### Press [I] for info.
            if cv2.waitKey(0) == ord('i'):
                print(" - " + str(sampleNum) + " - person(s) recognized.")
                print(imageResizedString)

            ### Press [SCAPE] to exit.
            if cv2.waitKey(0) == 27:    #ord(' '):
                break
                #TODO CAM
        #cap.release()
        cv2.destroyAllWindows()