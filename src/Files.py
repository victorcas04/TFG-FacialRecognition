
# encoding: utf-8

'''
@author: victorcas
'''

import cv2, os
import TextInterface as txtIf

delimiter = '\\'
datasetPath = '..'+delimiter+'sources'+delimiter+'dataset'
facesDatasetPath = '..'+delimiter+'sources'+delimiter+'facesDataset'
xmlFolderPath = '..'+delimiter+'sources'+delimiter+'xml'
xmlFile = 'haarcascade_frontalface_default.xml'
recognizerFolderPath = ".." + delimiter + 'sources' + delimiter + 'recognizer'
ymlFile = 'trainedData.yml'
recognizerDict = 'dictionary_ID_labels.txt'
recognizerInfo = 'info.txt'
extensionJPG = '.jpg'
extensionPNG = '.png'
defaultImage = "default" + extensionPNG
defaultImagePath = '..'+delimiter+'sources'
fileDelimiter = ', '

def getFileName(defaultFile=defaultImage, folder=defaultImagePath):

    '''
    Loads the full string name for a file.
    :param defaultFile: String
        Name of the file.
    :param folder: String
        Path to get to that file.
    :return: fullName: String
        Full path (including name) to the file specified.
        If no parameters are given, the default image from default path will be taken.
    '''

    return folder + delimiter + defaultFile


def loadImage(fullName=getFileName()):

    '''
    Loads an image.
    :param fullName: String
        Full path to the image that is gonna be loaded (if no path is given, default one is loaded).
    :return: image: Image
        Image loaded with OpenCV.
    '''

    txtIf.printMessage(txtIf.MESSAGES.LOADING_FILE, fullName)
    return cv2.imread(fullName)


def getLoadedXml():

    '''
    Method that loads the xml file (where the 'haar cascade classifier' is).
    :return: cascadeClassifier: CascadeClassifier
        File loaded.
    '''

    return cv2.CascadeClassifier(getFileName(xmlFile, xmlFolderPath))


def getReco():

    '''
    Method that loads recognizer (if wanna change the type of recognizer, change this method).
    :return: recognizer: Recognizer
        LBPH recognizer.
    '''

    return cv2.face.LBPHFaceRecognizer_create()


def loadInfo(nameImage=None):

    '''
    Get information from our database about a person in an image.
    :param nameImage: String
        Name of the image to get data from.
    :return: info: Dict
        Information about that image (name, age, birth_place and job).
        If not name is given or if it is not on the database ('info.txt'), default values are returned.
    '''

    name = " - "; age = " - "; birth_place = " - "; job = " - "
    if nameImage is not None:
        with open(recognizerFolderPath + delimiter + recognizerInfo) as f:

            '''
            Go over all the lines from the file until we find the one we want.
            '''
            for line in f:
                p = line.split(fileDelimiter)

                '''
                Each line of the file will have the nex structure:
                    name_of_image, name_of_person, age_of_person, city_of_birth, job_of_person 
                '''
                if p[0].__eq__(nameImage):

                    '''
                    If the name of the image is the same from photo and from 'info.txt', load that info and exit.
                    '''
                    name = p[1];
                    age = p[2];
                    birth_place = p[3];
                    job = p[4]
                    break

    info = {"name": name, "age": age, "birth_place": birth_place, "job": job}
    return info

def filesOnDir(path=datasetPath):

    '''
    Get the path from all the files in a given folder.
    :param path: String
        Path to the folder we want to list.
    :return: paths: List<String>
        A list with strings, each one of them has the path to a file from the directory.
    '''

    return os.listdir(path)

def saveImage(image, path):

    '''
    Save an image into a folder (from path).
    :param image: Image
        Image to be saved.
    :param path: String
        Path where the image is gonna be saved.
    '''

    txtIf.printMessage(txtIf.MESSAGES.SAVING_IMAGE, path)
    cv2.imwrite(path, image);

def writeInfoNewImage(stringInfo):

    '''
    Write the information about the new image into the file specified ('recognizerInfo').
    :param stringInfo: String
        Information to be saved (add to file, not overwrite it).
    '''

    with open(recognizerFolderPath + delimiter + recognizerInfo, "a") as f:
        f.write(stringInfo)

def overwriteFile(nameImage):

    '''
    Write the whole file except for the line of the new image, which will be ignored or written again
        depending on the user.
    :param nameImage: String
        Name of te image to check if exists on the database or not.
    :return: makeChanges: boolean
        True if changes have been made, False otherwise.
    '''

    makeChanges = True

    '''
    We have to read first and write later because of concurrency problems.
    '''
    with open(recognizerFolderPath + delimiter + recognizerInfo, "r") as f:
        lines = f.readlines()
    with open(recognizerFolderPath + delimiter + recognizerInfo, "w") as f:
        for line in lines:
            '''
            For each line of the file...
            '''

            if line.split(fileDelimiter)[0] != nameImage:
                '''
                ...if it doesn't match the name of the new image, write it back.
                '''
                f.write(line)
            else:
                '''
                ...if it matches the name of the new image, ask the user if wants to override it.
                '''
                txtIf.printError(txtIf.ERRORS.IMAGE_ALREADY_ON_DATABASE, True)
                ow = txtIf.getScan()
                if (not ow.__eq__("Y") and not ow.__eq__("y")):
                    '''
                    If the user doesn't overwrite it, just wrote it back where it was and set 'makeChanges' to False,
                        to indicate that no changes were made.
                    '''
                    makeChanges = False
                    f.write(line)
    return makeChanges


def doWhenNewImage(img):

    '''
    When we take a new image to save to database, we ask the user some informacion, if everything is ok,
        the new image is saved.
    :param img: Image
        Image to be saved.
    :return: makechanges: boolean
        True if we have saved the new image successfully, False otherwise.
    '''

    '''
    First we ask the user for the image name, a name by default is used in case nothing is written.
    '''
    print(
        "\nIntroduce the name of the new file (to save on database):\nIf no name is provided, \'new_image_name\' will be used.")
    nFile = txtIf.getScan()
    if not nFile:
        nFile = "new_image_name"

    '''
    Ask the user if wants to overwrite the information (in case it already existed) or not.
    '''
    makechanges = overwriteFile(nFile)
    if makechanges:
        '''
        Ask the user for more information to be saved (name_of_person, age_of_person, city_of_birth and job_of_person).
        '''
        info = txtIf.askInfoNewImage()

        '''
        Write all this new information on the file 'info.txt'.
        '''
        writeInfoNewImage('\n' + nFile + fileDelimiter + info[0] + fileDelimiter + info[1] + fileDelimiter + info[2] + fileDelimiter + info[3])

        '''
        Save the image to the database.
        '''
        checkFolderExists()
        saveImage(img, datasetPath + delimiter + nFile+ extensionJPG)

    return makechanges

def checkFolderExists(nameF=datasetPath):

    '''
    Check if a folder exists and create it if not.
    :param nameF: String
        Full path to the folder.
    '''

    if not os.path.exists(nameF):
        txtIf.printError(txtIf.ERRORS.FOLDER_NOT_FOUND, nameF)
        os.makedirs(nameF)