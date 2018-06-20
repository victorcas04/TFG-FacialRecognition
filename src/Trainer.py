
# encoding: utf-8

import os, cv2
import numpy as np
import Util as util
import Files as files
import TextInterface as txtIf

recognizerPath = files.recognizerFolderPath
pathOriginalImages = files.datasetPath
pathFacesImages = files.facesDatasetPath

def createCutFacesFromDatabase():
    folder = files.facesDatasetPath

    imagesToDelete = files.filesOnDir(folder)
    for the_file in imagesToDelete:
        file_path = files.getFileName(the_file, folder)
        if os.path.isfile(file_path):
            os.remove(file_path)

    images = files.filesOnDir()
    for i in images:
        cutted, cutFace = util.cutFaceFromImage(files.loadImage(files.getFileName(i, pathOriginalImages)))
        if cutted is True:
            cv2.imwrite(files.getFileName('face_' + i, folder), cutFace)

def train():

    trained = False
    recognizer = files.getReco()

    files.checkFolderExists(recognizerPath)

    def getImagesWithID(path):
        from PIL import Image
        imagePaths = [os.path.join(path,f) for f in files.filesOnDir(path)]
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
        return ID_labels, faces, id

    files.checkFolderExists(pathFacesImages)
    files.checkFolderExists(pathOriginalImages)

    createCutFacesFromDatabase()

    ID_labels, faces, numImages = getImagesWithID(pathFacesImages)

    if len(ID_labels) >= 2:
        recognizer.train(faces, np.fromiter(ID_labels.keys(), dtype=int))
        # Podríamos guardar el diccionario en una variable, pero de este forma nos aseguramos tener el
        #   diccionario guardado en caso de no re-entrenar la red en cada ejecución.
        recognizer.write(recognizerPath + files.delimiter + files.ymlFile)

        with open(recognizerPath + files.delimiter + files.recognizerDict, 'w') as f:
            for k in ID_labels.keys():
                s = str(k) + " " + ID_labels.get(k) + "\n"
                f.write(s)

        trained = True
    else:
        txtIf.printError(txtIf.ERRORS.NOT_ENOUGH_IMAGES_ON_DATABASE)

    return trained, numImages
