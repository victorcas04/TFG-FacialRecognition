
### http://www.python36.com/face-recognition-using-opencv-part-2/

import os, cv2
import numpy as np
from PIL import Image

import json

def train(path, detector=None):
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    if not os.path.exists('./TrainMachine/recognizer'):
        os.makedirs('./TrainMachine/recognizer')

    def getImagesWithID(path):

        imagePaths = [os.path.join(path,f) for f in os.listdir(path)]

        faces = []
        ID_labels = {}
        id = 0
        for imagePath in imagePaths:
            faceImg = Image.open(imagePath).convert('L')
            faceNp = np.array(faceImg,'uint8')

            #facesFromImage = detector.detectMultiScale(faceNp)

            #x, y, w, h = facesFromImage[0]
            #faces.append(faceNp[y:y + h, x:x + w])



            label = os.path.split(imagePath)[-1].split('.')[0]
            #print("Foto con id: " + str(id))
            ###ID = int(id)

            faces.append(faceNp)

            ###IDs.append(ID)
            ###labels.append(str(label))
            ID_labels[id] = label
            id+=1
            #cv2.imshow("training",faceNp)
            #cv2.waitKey(0)
        return ID_labels, faces#np.array(labels), face


    ID_labels, faces = getImagesWithID(path)

    #print("keys: " + str(np.fromiter(ID_labels.keys(), dtype=int)))
    recognizer.train(faces,np.fromiter(ID_labels.keys(), dtype=int))
    recognizer.write('./TrainMachine/recognizer/trainedData.yml')
    #recognizer.write('./TrainMachine/recognizer/trainedData.yml')
    #cv2.destroyAllWindows()

    with open('./TrainMachine/recognizer/dictionary_ID_labels.txt', 'w') as f:
        for k in ID_labels.keys():
            s = str(k) + " " + ID_labels.get(k) + "\n"
            f.write(s)


    #with open('./TrainMachine/recognizer/dictionary_ID_labels.txt', 'w') as file:
    #    file.write(json.dumps(ID_labels))


def trainDifferentYML(path, detector=None):
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    if not os.path.exists('./TrainMachine/recognizerPerImage'):
        os.makedirs('./TrainMachine/recognizerPerImage')

    def getImagesWithID(path):
        imagePaths = [os.path.join(path, f) for f in os.listdir(path)]

        faces = []
        ID_labels = {}
        id = 0
        for imagePath in imagePaths:
            faceImg = Image.open(imagePath).convert('L')
            faceNp = np.array(faceImg, 'uint8')

            label = os.path.split(imagePath)[-1].split('.')[0]

            faces.append(faceNp)

            recognizer.train([faceNp], np.array([id]))
            recognizer.write('./TrainMachine/recognizerPerImage/trainedData_' + label + '.yml')

            ID_labels[id] = label
            id += 1
        return ID_labels, faces

    ID_labels, faces = getImagesWithID(path)

    with open('./TrainMachine/recognizer/dictionary_ID_labels.txt', 'w') as f:
        for k in ID_labels.keys():
            s = str(k) + " " + ID_labels.get(k) + "\n"
            f.write(s)
