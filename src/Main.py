
# encoding: utf-8

from __future__ import division
import Util as util
import Files as files
import TextInterface as txtIf
from GUI import GUIClass as gui
import Camera as camera

if __name__ == "__main__":

    delimiter = files.delimiter
    pathDatasetFullImages = files.datasetPath
    pathDatasetFacesImages = files.facesDatasetPath

    txtIf.printMessage(txtIf.MESSAGES.TITLE)

    while True:

        askTrain = True
        while txtIf.askNewImage():
            if camera.captureImage()[0]:
                askTrain = False

        if askTrain:
            util.askTrain()
        else:
            util.train()

        if len(files.filesOnDir()) >= 2:
            txtIf.printMessage(txtIf.MESSAGES.ASK_CAMERA_FILE_REALTIME)
            c = txtIf.getScan()

            guiMain = None
            realTime = False

            if c.__eq__("C") or c.__eq__("c"):
                # Sacamos la imágen que queremos identificar desde la cámara
                photoOriginal = camera.captureImage(captureToCompare=True)[1]

            elif c.__eq__("R") or c.__eq__("r"):
                import RecognizerRealTime as rrt
                rrt.compareInRealTime()
                realTime = True

            else:
                # Sacamos la imágen que queremos identificar desde un archivo (en modo gráfico)
                txtIf.printMessage(txtIf.MESSAGES.INITIALIZING_INTERFACE)
                guiMain = gui.getInstance()
                photoOriginal = guiMain.loadImageByGUI()

            if not realTime:
                # Se hace en este órden y no antes porque da problemas con la interfaz nativa de cv
                if guiMain is None:
                    txtIf.printMessage(txtIf.MESSAGES.INITIALIZING_INTERFACE)
                    guiMain = gui.getInstance()
                guiMain.createMainWindow()
                guiMain.fixedSize()
                guiMain.createTop_BottomPanel_Final()

                cutted, pOri = util.cutFaceFromImage(photoOriginal)
                if cutted:
                    import CompareImages as compareImages
                    # Imágen resultado / Porcentaje comparación / Nombre imágen resultado / Información sobre la imagen
                    i, p, n = compareImages.compare(pOri)

                    guiMain.setTitleAndProgress(p, n)
                    guiMain.setImage(image=pOri)
                    guiMain.setImage(image=i, left=False)

                else:
                    guiMain.setTitleAndProgress()
                    guiMain.setImage(image=photoOriginal)
                    guiMain.setImage(left=False)

                guiMain.displayWindow()

        else:
            txtIf.printError(txtIf.ERRORS.NOT_ENOUGH_IMAGES_ON_DATABASE)
            txtIf.printMessage(txtIf.MESSAGES.INITIALIZING_INTERFACE)
            guiMain = gui.getInstance()
            guiMain.createMainWindow()
            guiMain.fixedSize()
            guiMain.setTitleAndProgress()
            guiMain.setImage()
            guiMain.setImage(left=False)

        if txtIf.askExitMain():
            break
