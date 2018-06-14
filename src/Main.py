
# encoding: utf-8

from __future__ import division
import Util as util
import Files as files
import TextInterface as txtIf
from GUI import GUIClass as gui


if __name__ == "__main__":

    delimiter = files.delimiter
    pathDatasetFullImages = files.datasetPath
    pathDatasetFacesImages = files.facesDatasetPath

    #  [0] para la webcam integrada en el portatil
    #  [1] para la cámara externa
    # [-1] para menú
    cameraIdx = 0

    txtIf.printMessage(txtIf.MESSAGES.TITLE)
    trained = util.askNewImage()

    if(trained is True) or (len(files.filesOnDir()) >= 2):
        txtIf.printMessage(txtIf.MESSAGES.ASK_CAMERA_FILE_REALTIME)
        c = txtIf.getScan()

        guiMain = None
        realTime = False

        if c.__eq__("C") or c.__eq__("c"):
            import Camera as camera
            # Sacamos la imágen que queremos identificar desde la cámara
            photoOriginal = camera.captureImage(cameraIdx, captureToCompare=True)[1]

        elif c.__eq__("R") or c.__eq__("r"):
            import RecognizerRealTime as rrt
            rrt.compareInRealTime(cameraIdx)
            realTime = True

        else:
            # Sacamos la imágen que queremos identificar desde un archivo (en modo gráfico)
            guiMain = gui.getInstance()
            guiMain.fixedSize()
            photoOriginal = guiMain.loadImageByGUI()

        if not realTime:
            # Se hace en este órden y no antes porque da problemas con la interfaz nativa de cv
            if guiMain is None:
                guiMain = gui.getInstance()
                guiMain.fixedSize()

            cutted, pOri = util.cutFaceFromImage(photoOriginal)
            if cutted:
                import CompareImages as compareImages
                # Imágen resultado / Porcentaje comparación / Nombre imágen resultado / Información sobre la imagen
                i, p, n = compareImages.compare(photoOriginal)
                inf = files.loadInfo(n)

                guiMain.initialize(n, p, inf)

                # Si nuestra mejor coincidencia no supera el umbral especificado, mostramos una imágen por defecto con un mensaje indicándonoslo.
                # Hay imágenes que al compararlas quedna números negativos al no encontrar resultados o resultados muy malos, por eso ponemos el umbral.
                pMinComp = 0
                if p < pMinComp:
                    txtIf.printError(txtIf.ERRORS.COMPARISON_THRESHOLD, pMinComp)
                    i = files.loadImage()

                if i is not None:
                    guiMain.displayInterfaceWindow(originalPhoto=pOri, photoFromDatabase=i, percentage=p)
                else:
                    txtIf.printError(txtIf.ERRORS.NETWORK_NOT_TRAINED)
                    guiMain.displayInterfaceWindow(originalPhoto=pOri)
            else:
                guiMain.initialize()
                guiMain.displayInterfaceWindow(originalPhoto=pOri)

    else:
        txtIf.printError(txtIf.ERRORS.CANNOT_TRAIN_NETWORK)
        txtIf.printError(txtIf.ERRORS.NOT_ENOUGH_IMAGES_ON_DATABASE)
        guiMain = gui.getInstance()
        guiMain.fixedSize()
        guiMain.initialize()
        guiMain.displayInterfaceWindow()