
# encoding: utf-8

from __future__ import division
import Util as util
import Camera as camera
import Files as files
import CompareImages as compareImages
import TextInterface as txtIf
from GUI import GUIClass as gui

delimiter = files.delimiter
pathDatasetFullImages = files.datasetPath
pathDatasetFacesImages = files.facesDatasetPath

#  [0] para la webcam integrada en el portatil
#  [1] para la cámara externa
# [-1] para menú
cameraIdx = 0

if __name__ == "__main__":

    txtIf.printMessage(txtIf.MESSAGES.TITLE)

    trained = util.askNewImage()

    if(trained is True) or (len(files.filesOnDir()) >= 2):
        txtIf.printMessage(txtIf.MESSAGES.ASKCAMERAORFILE)
        c = txtIf.getScan()

        guiMain = None

        if c.__eq__("C") or c.__eq__("c"):
            # Sacamos la imágen que queremos identificar desde la cámara
            photoOriginal = camera.captureImage(cameraIdx, captureToCompare=True)[1]

        else:
            # Sacamos la imágen que queremos identificar desde un archivo (en modo gráfico)
            guiMain = gui.getInstance()
            guiMain.fixedSize()
            photoOriginal = guiMain.loadImageByGUI()

        # Se hace en este órden y no antes porque da problemas con la interfaz nativa de cv
        if guiMain is None:
            guiMain = gui.getInstance()
            guiMain.fixedSize()

        pOri = util.cutFaceFromImage(photoOriginal)[1]
        # Imágen resultado / Porcentaje comparación / Nombre imágen resultado / Información sobre la imagen
        i, p, n = compareImages.compare(photoOriginal)
        inf = files.loadInfo(n)

        guiMain.initialize(n, p, inf)

        # Si nuestra mejor coincidencia no supera el umbral especificado, mostramos una imágen por defecto con un mensaje indicándonoslo.
        # Hay imágenes que al compararlas quedna números negativos al no encontrar resultados o resultados muy malos, por eso ponemos el umbral.
        pMinComp = 0
        if p < pMinComp:
            txtIf.printError(txtIf.ERRORS.COMPARISONTHRESHOLD, pMinComp)
            i = files.loadImage()

        if i is not None:
            guiMain.displayInterfaceWindow(originalPhoto=pOri, photoFromDatabase=i, percentage=p)
        else:
            txtIf.printError(txtIf.ERRORS.NETWORKNOTTRAINED)
            guiMain.displayInterfaceWindow(originalPhoto=pOri)

    else:
        txtIf.printError(txtIf.ERRORS.CANNOTTRAINNETWORK)
        txtIf.printError(txtIf.ERRORS.NOTENOUGHIMAGESONDATABASE)
        guiMain = gui.getInstance()
        guiMain.fixedSize()
        guiMain.initialize(None, 0, files.loadInfo())
        guiMain.displayInterfaceWindow()