
# encoding: utf-8

from __future__ import division
import sys, time, cv2
import Files as files
import TextInterface as txtIf
import CompareImages as compareImages
from GUI import GUIClass as gui
import tkinter as tk
from PIL import Image, ImageTk
segBetweenFrames = .5

delimiter = files.delimiter
maxInt = sys.maxsize

def initializeCamera(indexCamera):
    maxInt = sys.maxsize

    txtIf.printMessage(txtIf.MESSAGES.INITIALIZING_CAMERA)

    cap = cv2.VideoCapture(indexCamera)

    if not cap.isOpened():
        txtIf.printError(txtIf.ERRORS.CAMERA_NOT_INITIALIZED)
        return None

    cap.set(cv2.CAP_PROP_FPS, maxInt)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, maxInt)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, maxInt)

    # Esperamos dos segundos para que la cámara termine de inicializarse y no tomar datos basura
    time.sleep(2)
    return cap

def getDisplaySize():
    return [900, 1600]

def resizeFaceImage(image, aspect_ratio=2):
    h, w = getDisplaySize()
    prop = h / image.shape[1]
    newSize = (int((prop * image.shape[1]) / aspect_ratio), int((prop * image.shape[0]) / aspect_ratio))
    newImage = cv2.resize(image, (newSize[0], newSize[1]))
    return newImage

def checkColor(p):
    if (p < 35):
        return gui.COLORS.PROGRESSBAD.value
    elif (p < 75) and (p >= 35):
        return gui.COLORS.PROGRESSNORMAL.value
    elif (p < 98) and (p >= 75):
        return gui.COLORS.PROGRESSGOOD.value
    else:
        return gui.COLORS.PROGRESSPERFECT.value

def compareInRealTime(indexCamera=0):
    window = tk.Tk()
    window.title("GUI - Default title")

    hDisplay, wDisplay = getDisplaySize()
    width = wDisplay - (wDisplay // 10)
    height = hDisplay - (hDisplay // 10)
    window.resizable(width=False, height=False)
    window.minsize(width=width, height=height)
    window.maxsize(width=width, height=height)

    p = 0
    textFont = "Helvetica"
    textSize = 22
    textSizeProgressBar = 18

    namePhoto = None
    if namePhoto is not None:
        title = str(p) + " % of coincidence with image: " + str(namePhoto) + files.extensionJPG
    else:
        title = "No coincidences were found in the database."
    window.title(title)
    window.config(bg=gui.COLORS.BACKGROUNDGENERAL.value)

    percentageString = str(p) + "%"
    txtIf.printMessage(txtIf.MESSAGES.DISPLAY_WITH_COINCIDENCE, percentageString)

    myFrame = tk.Frame(window)
    myFrame.grid(row=0, column=0)

    myFrame.config(bg=gui.COLORS.BACKGROUNDGENERAL.value)
    myFrame.pack(fill=tk.Y, pady=height / 30)
    myFrame.rowconfigure(0, weight=4)
    myFrame.rowconfigure(1, weight=2)
    myFrame.rowconfigure(2, weight=1)
    myFrame.rowconfigure(3, weight=2)

    myLabelC = tk.Label(myFrame, compound=tk.BOTTOM, text="Original image")
    myLabelC.grid(row=0, column=0, sticky=tk.W)
    myLabelC.config(font=(textFont, textSize), bg=gui.COLORS.BACKGROUNDIMAGES.value, bd=8, relief="ridge")

    myLabelD = tk.Label(myFrame, compound=tk.BOTTOM, text=files.loadInfo()["name"])
    myLabelD.grid(row=0, column=1, sticky=tk.E)
    myLabelD.config(font=(textFont, textSize), bg=gui.COLORS.BACKGROUNDIMAGES.value, bd=8, relief="ridge")

    pBarLabel = tk.Label(myFrame, text=title)
    pBarLabel.config(font=(textFont, textSizeProgressBar), bg=gui.COLORS.BACKGROUNDGENERAL.value)
    pBarLabel.grid(row=1, columnspan=2, sticky=tk.S, pady=(height / 30, 0))

    from tkinter import ttk
    s = ttk.Style()
    s.theme_use("classic")
    s.configure("TProgressbar", thickness=height / 10, background=checkColor(p), borderwidth=4, relief="ridge")

    progress = ttk.Progressbar(myFrame, orient="horizontal", length=width - int(width / 10),
                               mode="determinate", style="TProgressbar")
    progress.grid(row=2, columnspan=2, sticky=tk.S, pady=(height / 30, 0))
    progress["value"] = p
    progress["maximum"] = 100

    cap = initializeCamera(indexCamera)
    if cap is None:
        return
    import Util as util
    import math

    def show_frame():
        numFaces = 0
        _, frame = cap.read()
        frame = cv2.flip(frame, 1)
        frame = resizeFaceImage(frame)

        gray = util.imageToGrayscale(frame)
        faces = util.getFacesMultiScale(gray)

        rectangleThickness = int((frame.shape[0] + frame.shape[1]) / (100 * 2 * math.pi))  # 20-30
        rectangleColor = (255, 0, 0)

        for (x, y, w, h) in faces:
            numFaces = numFaces + 1
            cv2.rectangle(frame, (x, y), (x + w, y + h), rectangleColor, rectangleThickness)

        cv2imageC = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
        imgC = Image.fromarray(cv2imageC)
        imgtkC = ImageTk.PhotoImage(image=imgC)

        myLabelC.imgtk = imgtkC
        myLabelC.configure(image=imgtkC)

        if numFaces == 1:
            pOri = util.cutFaceFromImage(frame)[1]
            # Imágen resultado / Porcentaje comparación / Nombre imágen resultado / Información sobre la imagen
            i, p, n = compareImages.compare(pOri, rT=True)

            pMinComp = 0
            if p < pMinComp:
                txtIf.printError(txtIf.ERRORS.COMPARISON_THRESHOLD, pMinComp)
                i = files.loadImage()

            if n is not None:
                title = str(p) + " % of coincidence with image: " + str(n) + files.extensionJPG
            else:
                title = "No coincidences were found in the database."
        else:
            txtIf.printError(txtIf.ERRORS.IMAGE_TOO_MANY_FACES, numFaces)
            title = "No coincidences were found in the database."
            p = 0
            n = None
            i = files.loadImage()

        window.title(title)
        pBarLabel.config(text=title)

        cv2imageD = cv2.cvtColor(resizeFaceImage(i), cv2.COLOR_BGR2RGBA)
        imgD = Image.fromarray(cv2imageD)
        imgtkD = ImageTk.PhotoImage(image=imgD)

        myLabelD.imgtk = imgtkD
        myLabelD.configure(image=imgtkD, text=files.loadInfo(n)["name"])

        progress["value"] = p
        s.configure("TProgressbar", background=checkColor(p))

        myLabelC.after(int(segBetweenFrames * 1000), show_frame)

    show_frame()
    window.mainloop()

