
# encoding: utf-8

from __future__ import division
import sys, cv2
import Files as files
import TextInterface as txtIf
import CompareImages as compareImages
from GUI import GUIClass as gui
import Camera as camera

segBetweenFrames = .5

def compareInRealTime():

    txtIf.printMessage(txtIf.MESSAGES.INITIALIZING_INTERFACE)

    guiMain = gui.getInstance()
    guiMain.createMainWindow("REAL-TIME RECOGNITION", realTime=True)
    guiMain.fixedSize()
    guiMain.createTop_BottomPanel_Final()

    cap = camera.initializeCamera()
    if cap is None:
        return
    import Util as util
    import math

    def show_frame():
        _, frame = cap.read()
        frame = cv2.flip(frame, 1)
        frameToShow = util.resizeFaceImage(frame, realTime=True)

        gray = util.imageToGrayscale(frameToShow)
        faces = util.getFacesMultiScale(gray)

        rectangleThickness = int((frameToShow.shape[0] + frameToShow.shape[1]) / (100 * 2 * math.pi))  # 20-30
        rectangleColor = (255, 0, 0)

        for (x, y, w, h) in faces:
            cv2.rectangle(frameToShow, (x, y), (x + w, y + h), rectangleColor, rectangleThickness)

        guiMain.setImage(image=frameToShow)

        cutted, pOri = util.cutFaceFromImage(frame)
        if cutted:
            # Imágen resultado / Porcentaje comparación / Nombre imágen resultado / Información sobre la imagen
            pOri, p, n = compareImages.compare(pOri)
            if p <= 0:
                pOri = files.loadImage()
                n = None
        else:
            p = 0;
            n = None

        guiMain.setTitleAndProgress(p, n)
        guiMain.setImage(image=pOri, left=False)

        guiMain.myLabelC.after(int(segBetweenFrames * 1000), show_frame)

    show_frame()
    guiMain.displayWindow()

