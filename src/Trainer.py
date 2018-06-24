
# encoding: utf-8

'''
@author: victorcas
'''

import os, cv2
import numpy as np
import Util as util
import Files as files
import TextInterface as txtIf

recognizerPath = files.recognizerFolderPath
pathOriginalImages = files.datasetPath
pathFacesImages = files.facesDatasetPath

def createCutFacesFromDatabase():

    '''
    Create the images to be compared from database, containing only the face.
    '''

    '''
    Before crop the images from database, remove the old ones.
    '''
    imagesToDelete = files.filesOnDir(pathFacesImages)
    for the_file in imagesToDelete:
        file_path = files.getFileName(the_file, pathFacesImages)
        if os.path.isfile(file_path):
            os.remove(file_path)

    '''
    For each image on the database...
    '''
    images = files.filesOnDir()
    for i in images:

        '''
        ...try to cut the face on each image...
        '''
        cutted, cutFace = util.cutFaceFromImage(files.loadImage(files.getFileName(i, pathOriginalImages)))

        if cutted is True:
            '''
            ...if success, save the image to default folder. Ignore this image otherwise.
            '''
            cv2.imwrite(files.getFileName('face_' + i, pathFacesImages), cutFace)


def train():

    '''
    Train the network.
    :return: trained: boolean
        True if the network was trianed successfully. False otherwise.
    :return: numImages: Integer
        The number of images from the database that were used to train the network (only the ones with the face).
    '''

    trained = False
    recognizer = files.getReco()
    files.checkFolderExists(recognizerPath)

    def getImagesWithID(path):

        '''
        Get all images with faces from database and stores their ID (necessary to train the network) that will
            be used when selecting the result image of the comparison from database.
        :param path: String
            Path to folder where the images are stored (the ones with faces only).
        :return: ID_labels: Dict
            Dictionary that stores the name of the image on different IDs.
        :return: faces: ArrayList<np.array>
            Array in which every face from images is stored.
        :return: id: Integer
            Number of IDs obtained, so it's equals to the number of images used to train the network.
        '''

        from PIL import Image
        imagePaths = [os.path.join(path,f) for f in files.filesOnDir(path)]
        faces = []
        ID_labels = {}
        id = 0
        for imagePath in imagePaths:

            '''
            Open the images as an array and store each image to our ArrayList.
            '''
            faceImg = Image.open(imagePath).convert('L')
            faceNp = np.array(faceImg,'uint8')
            faces.append(faceNp)

            '''
            Load each image name and stores it in the dictionary with a new ID.
            '''
            label = os.path.split(imagePath)[-1].split('.')[0]
            ID_labels[id] = label
            id+=1

        return ID_labels, faces, id

    '''
    If any of the folders doesn't exists, create it.
    '''
    files.checkFolderExists(pathFacesImages)
    files.checkFolderExists(pathOriginalImages)

    '''
    Create new images just with the faces from the original ones.
    '''
    createCutFacesFromDatabase()
    ID_labels, faces, numImages = getImagesWithID(pathFacesImages)

    if len(ID_labels) >= 2:
        '''
        If there was two or more images on the database, train the network.
        '''
        recognizer.train(faces, np.fromiter(ID_labels.keys(), dtype=int))

        '''
        Write the yml file with the results of the training.
        '''
        recognizer.write(recognizerPath + files.delimiter + files.ymlFile)

        '''
        We could save the dictionary into a temporal variable, to be used in this execution only, but the way it is 
            done now, we save it to a file, so don't have to train the network again on every run.
        '''
        with open(recognizerPath + files.delimiter + files.recognizerDict, 'w') as f:
            for k in ID_labels.keys():
                s = str(k) + " " + ID_labels.get(k) + "\n"
                f.write(s)
        trained = True

    else:
        '''
        If there was less than two images on the database, print an error message.
        '''
        txtIf.printError(txtIf.ERRORS.NOT_ENOUGH_IMAGES_ON_DATABASE)

    return trained, numImages
