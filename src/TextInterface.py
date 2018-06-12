
# encoding: utf-8

import six
from enum import Enum

class ERRORS(Enum):
    NETWORKNOTTRAINED2 = 1
    CANNOTTRAINNETWORK = 2
    IMAGENOFACES = 3
    IMAGETOOMANYFACES = 4
    COMPARISONTHRESHOLD = 5
    NOTENOUGHIMAGESONDATABASE = 6
    CAMERANOTINITIALIZED = 7
    NETWORKNOTTRAINED = 8

class MESSAGES(Enum):
    TITLE = 1
    ASKCAMERAORFILE = 2
    SAVINGIMAGE = 4
    DISPLAYWITHCOINCIDENCE = 6
    SELECTIMAGE = 7
    ASKADDIMAGES = 8
    TRAINTIME = 9
    ASKTRAINNETWORK = 10
    LOADINGFILE = 11
    YMLUSED = 12
    TRAININGNETWORK = 13
    COMPARINGIMAGES = 14
    INITIALIZINGCAMERA = 15
    IMAGEINREALTIME = 16
    CAMERAPAUSED = 17
    CAMERAPAUSED2 = 18

def printMessage(code=None, info=None, info2=None):
    if code.name is "TITLE":
        print("\n\nTFG - Facial Recognition - Victor de Castro Hurtado\n\n")

    elif code.name is "ASKCAMERAORFILE":
        print("\nDo you want to use an image from camera [C] or from file [F]?")

    elif code.name is "SAVINGIMAGE":
        print("\nSaving image in: " + str(info) + "...")

    elif code.name is "DISPLAYWITHCOINCIDENCE":
        print("\nDisplaying result with a " + str(info) + " of coincidence.")

    elif code.name is "SELECTIMAGE":
        print("\nSelect an image...")

    elif code.name is "ASKADDIMAGES":
        print("\nIf you want to add a new image to the database press [Y]")

    elif code.name is "TRAINTIME":
        print("\nTraining time with " + str(info) + " images: " + str(info2) + " seconds.")

    elif code.name is "ASKTRAINNETWORK":
        print("\nIf you want to train the network again press [Y]")

    elif code.name is "LOADINGFILE":
        print("Loading file " + str(info) + "...")

    elif code.name is "YMLUSED":
        print("\nThe file " + str(info) + (
            (" just created will be used.") if info2 else (" existing from before will be used.")))

    elif code.name is "TRAININGNETWORK":
        print("\nCreating face-focused images from original-database images...")
        print("Training network...\n")

    elif code.name is "COMPARINGIMAGES":
        print("\nComparing images...")

    elif code.name is "INITIALIZINGCAMERA":
        print("\nInitializing camera...")

    elif code.name is "IMAGEINREALTIME":
        print("\nDisplaying image in real-time...")

    elif code.name is "CAMERAPAUSED":
        print("\nCAMERA PAUSED")

    elif code.name is "CAMERAPAUSED2":
        print("\nCAMERA PAUSED: Press [SPACE] to resume camera reading.")

    else:
        print("\nMESSAGE: Unknown message.")

def printError(code=None, info=None):
    if code.name is "NETWORKNOTTRAINED":
        print("\nERROR: Cannot compare: The network isn't trained.")

    elif code.name is "NETWORKNOTTRAINED2":
        print("\nERROR: Network is not trained, so images from \'facesDataset\' are missing. Please check.\n")

    elif code.name is "CANNOTTRAINNETWORK":
        print("\nWARNING: Network couldn't be trained.")

    elif code.name is "COMPARISONTHRESHOLD":
        print("\nWARNING: The comparison obtained less than " + str(info) + "% of coincidence. Loading default image.")

    elif code.name is "NOTENOUGHIMAGESONDATABASE":
        print("\nERROR: Two (2) or more samples are needed to train the network.")

    elif code.name is "IMAGENOFACES":
        print("\nWARNING: Image with no faces.")

    elif code.name is "IMAGETOOMANYFACES" and info is None:
        print("\nWARNING: Image with too many faces.")

    elif code.name is "IMAGETOOMANYFACES" and info is not None:
        print("\nWARNING: [" + str(
            info) + "] faces were found in the image.\nThere must be exactly one (1) person to be able to capture the image.")

    elif code.name is "CAMERANOTINITIALIZED":
        print("\nERROR: Camera couldn't be turned on.")

    else:
        print("\nERROR: Unknown error.")

def getScan():
    return six.moves.input()

def askInfoNewImage():
    print("\nIntroduce the name of the new file (to save on database):\nIf no name is provided, \'new_image_name\' will be used.")
    nFile = getScan()
    if not nFile:
        nFile="new_image_name"
    print("\nIntroduce the name of the person who appears on that image:\nIf no name is provided, \'Default Name\' will be used.")
    name = getScan()
    if not name:
        name="Default Name"
    print("\nIntroduce the age of that person:\nIf no age is provided, \'Default Age\' will be used.")
    age = getScan()
    if not age:
        age="Default Age"
    print("\nIntroduce the city name where he/she was born:\nIf no city name is provided, \'Default City\' will be used.")
    birthplace = getScan()
    if not birthplace:
        birthplace="Default City"
    print("\nIntroduce the actual profession of that person:\nIf no occupation is provided, \'Default Job\' will be used.")
    job = getScan()
    if not job:
        job="Default Job"

    return nFile, name, age, birthplace, job

def printMenuFaceInBox(fromCamera=True):

    print("\nOPTIONS:\n")
    print("Press [I] to display general information.")
    print("Press [Q] to quit.")
    if fromCamera:
        print("Press [P] to pause the camera.")
        print("Press [SPACE] to resume the camera (only if it was paused).")
        print("Press [C] to capture the actual frame and close the camera.\n")