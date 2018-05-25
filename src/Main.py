
# encoding: utf-8

from __future__ import division
import Util as util
import Camera as camera
from GUI import GUIClass as gui

delimiter = util.delimiter
pathDatasetFullImages = util.datasetPath
pathDatasetFacesImages = util.facesDatasetPath

#  [0] para la webcam integrada en el portatil
#  [1] para la cámara externa
# [-1] para menú
cameraIdx = 0

if __name__ == "__main__":

    print("\n\nTFG - Facial Recognition - Victor de Castro Hurtado\n\n")

    if util.askNewImage():
        util.train()
    else:
        util.askTrain()

    print("\nDo you want to use an image from camera [C] or from file [F]?")
    c = util.getScan()

    guiMain = None

    if c.__eq__("C") or c.__eq__("c"):
        # Sacamos la imágen que queremos identificar desde la cámara
        photoOriginal = camera.faceInBoxVideo(cameraIdx)

    else:
        # Sacamos la imágen que queremos identificar desde un archivo (en modo gráfico)
        # C:\Users\victo\Desktop\DEVELOPMENT\projects\PycharmProjects\TFG-FacialRecognition\TFG-FacialRecognition\sources\facesDataset
        guiMain = gui.getInstance()
        h, w = util.getDisplaySize()
        guiMain.fixedSize(h, w)

        photoOriginal = util.loadImageByGUI(guiMain)

    if guiMain is None:
        guiMain = gui.getInstance()
        h, w = util.getDisplaySize()
        guiMain.fixedSize(h, w)

    # Uncomment for test purposes
    # photoOriginal=util.loadImage(util.getFileName("face_cas.jpg", pathDatasetFacesImages))

    # Imágen resultado / Porcentaje comparación / Nombre imágen resultado
    i, p, n, inf = util.compare(photoOriginal)

    guiMain.initialize(n, p, inf)

    # Si nuestra mejor coincidencia no supera el umbral especificado, mostramos una imágen por defecto con un mensaje indicándonoslo.
    # Hay imágenes que al compararlas quedna números negativos al no encontrar resultados o resultados muy malos, por eso ponemos el umbral tan bajo.
    pMinComp = 0
    if p < pMinComp:
        print("\nThe comparison obtained less than " + str(pMinComp) + "% of coincidence. Loading default image.")
        i = util.loadImage()

    pOri = util.cutFaceFromImage(photoOriginal)[1]

    util.displayInterfaceWindow(guiMain, photoFromCamera=util.resizeFaceImage(pOri), photoFromDatabase=util.resizeFaceImage(i), percentage=p)
