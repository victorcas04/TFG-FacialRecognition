
from src.ImageCapture.ImageCaptureInterface import AbstractImageCaptureClass as Parent

#from PIL import Image
#import os
import cv2
import time
import sys

class ImageCaptureFromCameraClass(Parent):

    def __init__(self):
        pass

    def loadMultipleImages(self, numberOfShots):
        images = self.captureImageFromCamera(numberOfShots)
        return images

    def loadImage(self):
        Parent.image = self.captureImageFromCamera()[0]
        return Parent.image

    def captureImageFromCamera(self, numberOfShots = 1):

        images = []

        '''
        cam = cv2.Camera()
        cv2.time.sleep(0.1)  # If you don't wait, the image will be dark
        img = cam.getImage()
        cam.stop()
        '''

        ### Max image size possible
        maxInt = sys.maxsize

        print("Starting Camera. Please Wait...")

        cam = cv2.VideoCapture(0)
        cam.set(cv2.CAP_PROP_FPS, maxInt)
        #cam.set(cv2.CAP_PROP_CONVERT_RGB, True)        ### By default
        cam.set(cv2.CAP_PROP_FRAME_HEIGHT, maxInt)
        cam.set(cv2.CAP_PROP_FRAME_WIDTH, maxInt)
        time.sleep(2)

        while cam.isOpened() and numberOfShots > 0:

            ret, frame = cam.read()
            cv2.imshow("To Take a Snap Press [SPACE] (" + str(numberOfShots) + " shots remaining)", frame)
            if cv2.waitKey(1) == ord(' '):        ### If space is pressed, we take a snap and exit loop
                images.append(frame)
                numberOfShots -= 1
                #break

        cam.release()
        cv2.destroyAllWindows()

        '''
        pygame.init()
        pygame.camera.init()
        cam = pygame.camera.Camera(pygame.camera.list_cameras()[0])
        cam.start()
        secondsToWait = 5
        msToWait = secondsToWait * 1000
        pygame.time.delay(msToWait)
        img = cam.get_image()
        cam.stop()
        '''

        return images
