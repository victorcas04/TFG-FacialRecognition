import sys

import src.Test.TestsImages as tstImages
import src.Test.TestsPlaceholders as tstPlaceholders
import src.Test.TestsVariables as tstVariables
import src.Util as util

import cv2
import numpy as np
import os, time
import sqlite3

class TestClass(object):

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
        tstPlaceholders.testPlaceholders2(util.getFileName())
        tstPlaceholders.testPlaceholders3(util.getFileName())
        tstPlaceholders.testPlaceholders4(util.getFileName())

    def testImages(self, photo):
        tstImages.testImages1(util.getFileName())
        tstImages.testImages2(util.getFileName())
        tstImages.testImages3(util.getFileName())
        tstImages.testImages4(util.getFileName())
        tstImages.testImages5(util.getFileName())
        tstImages.testImages6(util.getFileName(photo), nShots=4)
        tstImages.testThreshold(util.getFileName(photo))

    def testFaceLocation(self, photoName):
        util.faceInBoxImage(photoName)
        util.faceInBoxVideo()

    def testActual(self):
        print("\nTest Actual\n")



        pass
