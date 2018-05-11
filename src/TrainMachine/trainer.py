
# encoding: utf-8

### http://www.python36.com/face-recognition-using-opencv-part-2/

import os, cv2
import numpy as np
from PIL import Image

delimiter = '\\'
#fromExecutable='..'+delimiter
fromExecutable = ""

recognizerPath = fromExecutable+'TrainMachine'+delimiter+'recognizer'
recognizerFile = 'trainedData.yml'
dictFile = 'dictionary_ID_labels.txt'

def train(path):

    trained = False
    recognizer = cv2.face.LBPHFaceRecognizer_create()

    if not os.path.exists(recognizerPath):
        os.makedirs(recognizerPath)

    def getImagesWithID(path):
        imagePaths = [os.path.join(path,f) for f in os.listdir(path)]
        faces = []
        ID_labels = {}
        id = 0
        for imagePath in imagePaths:
            faceImg = Image.open(imagePath).convert('L')
            faceNp = np.array(faceImg,'uint8')
            label = os.path.split(imagePath)[-1].split('.')[0]
            faces.append(faceNp)
            ID_labels[id] = label
            id+=1
        return ID_labels, faces

    ID_labels, faces = getImagesWithID(path)

    if len(ID_labels) >= 2:
        recognizer.train(faces, np.fromiter(ID_labels.keys(), dtype=int))
        recognizer.write(recognizerPath + delimiter + recognizerFile)

        with open(recognizerPath + delimiter + dictFile, 'w') as f:
            for k in ID_labels.keys():
                s = str(k) + " " + ID_labels.get(k) + "\n"
                f.write(s)

        trained = True
    else:
        print("Se necesitan al menos dos(2) muestras para poder entrenar la red.")

    return trained

