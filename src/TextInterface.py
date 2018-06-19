
# encoding: utf-8

from enum import Enum

title = "TFG - Facial Recognition"
author = "Victor de Castro Hurtado"

class ERRORS(Enum):
    NETWORK_NOT_TRAINED_2 = 1
    CANNOT_TRAIN_NETWORK = 2
    IMAGE_NO_FACES = 3
    IMAGE_TOO_MANY_FACES = 4
    COMPARISON_THRESHOLD = 5
    NOT_ENOUGH_IMAGES_ON_DATABASE = 6
    CAMERA_NOT_INITIALIZED = 7
    NETWORK_NOT_TRAINED = 8
    IMAGE_ALREADY_ON_DATABASE = 9
    FUTURE_FEATURE = 10

class MESSAGES(Enum):
    TITLE = 1
    ASK_CAMERA_FILE_REALTIME = 2
    SAVING_IMAGE = 3
    DISPLAY_WITH_COINCIDENCE = 4
    SELECT_IMAGE = 5
    ASK_ADD_IMAGES = 6
    TRAIN_TIME = 7
    ASK_TRAIN_NETWORK = 8
    LOADING_FILE = 9
    YML_USED = 10
    TRAINING_NETWORK = 11
    COMPARING_IMAGES = 12
    INITIALIZING_CAMERA = 13
    IMAGE_IN_REALTIME = 14
    CAMERA_PAUSED = 15
    CAMERA_PAUSED_2 = 16
    PRESS_ANY_KEY = 17
    RESOLUTION_CAMERA = 18
    INITIALIZING_INTERFACE = 19
    ASK_EXIT_MAIN = 20

def printMessage(code=None, info=None, info2=None):
    if code.name is "TITLE":
        print("\n\n" + str(title) + " - " + str(author) + "\n\n")

    elif code.name is "ASK_CAMERA_FILE_REALTIME":
        print("\nDo you want to use an image from camera [C], from file [F] or in real-time [R]?")

    elif code.name is "SAVING_IMAGE":
        print("\nSaving image in: " + str(info) + "...")

    elif code.name is "DISPLAY_WITH_COINCIDENCE":
        print("\nDisplaying result with a " + str(info) + " of coincidence.")

    elif code.name is "SELECT_IMAGE":
        print("\nSelect an image...")

    elif code.name is "ASK_ADD_IMAGES":
        print("\nDo you want to add a new image to the database? [Y/N]")

    elif code.name is "TRAIN_TIME":
        print("\nTraining time with " + str(info) + " images: " + str(info2) + " seconds.")

    elif code.name is "ASK_TRAIN_NETWORK":
        print("\nDo you want to train the network? [Y/N]")

    elif code.name is "LOADING_FILE":
        print("Loading file " + str(info) + "...")

    elif code.name is "YML_USED":
        print("\nThe file " + str(info) + (
            (" just created will be used.") if info2 else (" existing from before will be used.")))

    elif code.name is "TRAINING_NETWORK":
        print("\nCreating face-focused images from original-database images...")
        print("Training network...\n")

    elif code.name is "COMPARING_IMAGES":
        print("\nComparing images...")

    elif code.name is "INITIALIZING_CAMERA":
        print("\nInitializing camera...")

    elif code.name is "IMAGE_IN_REALTIME":
        print("\nDisplaying image in real-time...")

    elif code.name is "CAMERA_PAUSED":
        print("\nCAMERA PAUSED")

    elif code.name is "CAMERA_PAUSED_2":
        print("\nCAMERA PAUSED: Press [SPACE] to resume camera reading.")

    elif code.name is "PRESS_ANY_KEY":
        print("\nPress any key to continue...")

    elif code.name is "RESOLUTION_CAMERA":
        print("Max. resolution of  camera used: [" + str(info[0]) + "x" + str(info[1]) + "]")

    elif code.name is "INITIALIZING_INTERFACE":
        print("\nInitializing interface...")

    elif code.name is "ASK_EXIT_MAIN":
        print("\nDo you want to exit? [Y/N]")

    else:
        print("\nMESSAGE: Unknown message.")

def printError(code=None, info=None):
    if code.name is "NETWORK_NOT_TRAINED":
        print("\nERROR: Cannot compare: The network isn't trained.")

    elif code.name is "NETWORK_NOT_TRAINED_2":
        print("\nERROR: Network is not trained, so images from \'facesDataset\' are missing. Please check.\n")

    elif code.name is "CANNOT_TRAIN_NETWORK":
        print("\nWARNING: Network couldn't be trained.")

    elif code.name is "COMPARISON_THRESHOLD":
        print("\nWARNING: The comparison obtained less than " + str(info) + "% of coincidence. Loading default image.")

    elif code.name is "NOT_ENOUGH_IMAGES_ON_DATABASE":
        print("\nERROR: Two (2) or more samples are needed to train the network.")

    elif code.name is "IMAGE_NO_FACES":
        print("\nWARNING: Image with no faces.")

    elif code.name is "IMAGE_TOO_MANY_FACES" and info is None:
        print("\nWARNING: Image with too many faces.")

    elif code.name is "IMAGE_TOO_MANY_FACES" and info is not None:
        print("\nWARNING: [" + str(
            info) + "] faces were found in the image.\nThere must be exactly one (1) person to be able to capture the image.")

    elif code.name is "CAMERA_NOT_INITIALIZED":
        print("\nERROR: Camera couldn't be turned on.")

    elif code.name is "IMAGE_ALREADY_ON_DATABASE":
        print("\nWARNING: An image with the same name already exists.")
        if info:
            print("Do you want to overwrite it? [Y/N]")

    elif code.name is "FUTURE_FEATURE":
        print("\nWARNING: Feature not implemented yet. Wait for developers to do their job.")

    else:
        print("\nERROR: Unknown error.")

def getScan():
    import six
    return six.moves.input()

def askNewImage():
    printMessage(MESSAGES.ASK_ADD_IMAGES)
    c = getScan()
    return True if c.__eq__("Y") or c.__eq__("y") else False

def askExitMain():
    printMessage(MESSAGES.ASK_EXIT_MAIN)
    c = getScan()
    return True if c.__eq__("Y") or c.__eq__("y") else False

def askInfoNewImage():

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

    return name, age, birthplace, job

def printMenuFaceInBox(fromCamera=True):

    print("\nOPTIONS:\n")
    print("Press [I] to display general information.")
    print("Press [Q] to quit.")
    if fromCamera:
        print("Press [P] to pause the camera.")
        print("Press [SPACE] to resume the camera (only if it was paused).")
        print("Press [C] to capture the actual frame and close the camera.\n")