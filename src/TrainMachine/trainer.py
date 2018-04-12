
### http://www.python36.com/face-recognition-using-opencv-part-2/

import os
import cv2
import numpy as np
from PIL import Image

def train():
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    path = "dataset"
    if not os.path.exists('./TrainMachine/recognizer'):
        os.makedirs('./TrainMachine/recognizer')

    def getImagesWithID(path):

        imagePaths = [os.path.join(path,f) for f in os.listdir(path)]
        faces = []
        IDs = []
        for imagePath in imagePaths:
            faceImg = Image.open(imagePath).convert('L')
            faceNp = np.array(faceImg,'uint8')
            id = os.path.split(imagePath)[-1].split('.')[0]
            #print("Foto con id: " + str(id))
            ID = int(id)
            faces.append(faceNp)
            IDs.append(ID)
            #cv2.imshow("training",faceNp)
            #cv2.waitKey(0)
        return np.array(IDs), faces



    Ids, faces = getImagesWithID(path)
    recognizer.train(faces,Ids)
    recognizer.write('./TrainMachine/recognizer/trainedData.yml')
    cv2.destroyAllWindows()