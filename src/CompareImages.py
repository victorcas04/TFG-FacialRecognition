
# encoding: utf-8

'''
@author: victorcas
'''

import Util as util
import Files as files
import TextInterface as txtIf

def getLoadedYml():

    '''
    Method that loads the yml file (where the result of the training is).
    :return: reco: Recognizer
        Trained network loaded by the recognizer.
    '''

    reco = files.getReco()
    reco.read(files.getFileName(files.ymlFile, files.recognizerFolderPath))
    return reco


def compareSingle(img):

    '''
    Method that compares a single image.
    :param img: Image
        Image to compare.
    :return: id :Integer
        Id of the result image from network, -1 if the network isn't trained.
    :return: percentage: float
        Accuracy of the comparison for that person.
    '''

    gray = util.imageToGrayscale(img)

    '''
    Set the part of the image that is gonna be compared (in our case the whole image because only the face 
        is passed).
    '''
    x = 0; y = 0; w = gray.shape[1]; h = gray.shape[0]

    try:
        '''
        Load the recognizer and predict the result image.
        '''
        recognizer = getLoadedYml()
        id, conf = recognizer.predict(gray[y:y + h, x:x + w])
    except:
        '''
        If we cannot load the recognizer or the data from the network, it means the network isn't trained.
        '''
        txtIf.printError(txtIf.ERRORS.NETWORK_NOT_TRAINED)
        id = -1; conf = 100;

    '''
    The 'conf' parameter really means the % of the image that is different.
    If we want to get the real % of coincidence, we must do this operation.
    '''
    conf = 100 - float(conf)
    percentage = float("{0:.2f}".format(conf))

    return id, percentage


def compare(img, path=files.facesDatasetPath):

    '''
    Calls method that compares the image, and get more information about it to return the whole pack.
    :param img: Image
        Image to be compared.
    :param path: String
        Path to the folder where the images to be displayed are (only the faces ones).
    :return: imgRet: Image
        Image result of the comparison or None if there was no result.
    :return: p: float
        Percentage of coincidence.
    :return: label: String
        Name of the image from database or None if the comparison wasn't successful.
    '''

    label = None
    imgRet = None
    txtIf.printMessage(txtIf.MESSAGES.COMPARING_IMAGES)

    '''
    Compare the image given.
    If we want to compare multiple images at once, just call 'compareSingle' that many times.
    '''
    id, p = compareSingle(img)

    '''
    If the comparison was successful...
    '''
    if id > -1:

        '''
        ...if the comparison got a negative result (possible, don't forget is a prediction and can fail some times) 
            just set the percentage to 0.
        '''
        if p <= 0:
            p = 0
        else:
            p = float("{0:.2f}".format(p)) if p <= 100 else 100

        '''
        Check if folder exists, if not create it.
        '''
        files.checkFolderExists(files.datasetPath)

        '''
        Get all files from that folder.
        '''
        imgsOr = files.filesOnDir()

        '''
        Get the name of the image with given id.
        '''
        label = imgsOr[id].split(".")[0]
        print("Information about comparison: id= " + str(id) + "   ---   label= " + str(label) + "   ---   coincidence= " + str(p))

        '''
        Load the image with the name got previously.
        '''
        imgRet = files.loadImage(files.getFileName("face_" + label + files.extensionJPG, folder=path))

    return imgRet, p, label