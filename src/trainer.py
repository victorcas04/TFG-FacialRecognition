
# encoding: utf-8

import os
import numpy as np
from PIL import Image
import Util as util

delimiter = util.delimiter
recognizerPath = util.recognizerFolderPath
recognizerFile = util.ymlFile
dictFile = util.recognizerDict
pathImages = util.facesDatasetPath

def train():

    trained = False
    recognizer = util.getReco()

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

    if not os.path.exists(pathImages):
        os.makedirs(pathImages)
    util.createCutFacesFromDatabase()

    ID_labels, faces = getImagesWithID(pathImages)

    if len(ID_labels) >= 2:
        recognizer.train(faces, np.fromiter(ID_labels.keys(), dtype=int))
        recognizer.write(recognizerPath + delimiter + recognizerFile)

        with open(recognizerPath + delimiter + dictFile, 'w') as f:
            for k in ID_labels.keys():
                s = str(k) + " " + ID_labels.get(k) + "\n"
                f.write(s)

        trained = True
    else:
        print("Two (2) or more samples are needed to train the network.")

    return trained