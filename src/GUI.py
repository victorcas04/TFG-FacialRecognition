
# encoding: utf-8

from __future__ import division
import tkinter as tk
from tkinter import ttk
import Files as files
import TextInterface as txtIf
from PIL import Image, ImageTk
import cv2
from tkinter import filedialog as fd
from enum import Enum

class GUIClass(object):
    class COLORS(Enum):
        BACKGROUNDIMAGES = "#00CED1"  # darkturquoise
        BACKGROUNDGENERAL = "#AFEEEE"  # paleturquoise
        BUTTON = "#00CED1"  # dark turquoise
        PROGRESSDEAD = "#000000" # black
        PROGRESSBAD = "#8B0000"  # darkred
        PROGRESSBADNORMAL = "#FF4500" # orange red
        PROGRESSNORMAL = "#CCCC00"  # dark yellow 1
        PROGRESSGOOD = "#006400"  # darkgreen
        PROGRESSPERFECT = "#FF00FF"  # magenta
        POPUPINFO = "#6FEFC4" # aqua marine

    __instance = None
    textFont = "Helvetica"
    textSize = 22
    textSizeProgressBar = 18

    def displayWindow(self):
        # Using mainloop() to show image
        self.window.mainloop()

    def selectFile(self):
        txtIf.printMessage(txtIf.MESSAGES.SELECT_IMAGE)
        askFileWindow = tk.Tk()
        askFileWindow.title("Select an image...")
        askFileWindow.filename = fd.askopenfilename(initialdir="/", title="Select file",
                                          filetypes=(
                                          ("jpeg files", '*'+files.extensionJPG), ("png files", '*'+files.extensionPNG), ("all files", "*.*")))
        nFile = askFileWindow.filename
        askFileWindow.destroy()
        return nFile

    def loadImageByGUI(self):
        imageToReturn = self.selectFile()
        if (imageToReturn.endswith(files.extensionJPG) or imageToReturn.endswith(files.extensionPNG)):
            imageToReturn = files.loadImage(imageToReturn)
        else:
            txtIf.printError(txtIf.ERRORS.FILE_WRONG_FORMAT)
            imageToReturn = files.loadImage()
        return imageToReturn

    def getInfo(self, param):
        return self.info[param]

    def checkColor(self, p):
        if (p < 10):
            colorprogressbar = self.COLORS.PROGRESSDEAD.value
        elif (p < 35) and (p >= 10):
            colorprogressbar = self.COLORS.PROGRESSBAD.value
        elif (p < 50) and (p >= 35):
            colorprogressbar = self.COLORS.PROGRESSBADNORMAL.value
        elif (p < 80) and (p >= 50):
            colorprogressbar = self.COLORS.PROGRESSNORMAL.value
        elif (p < 95) and (p >= 80):
            colorprogressbar = self.COLORS.PROGRESSGOOD.value
        else:
            colorprogressbar = self.COLORS.PROGRESSPERFECT.value
        return colorprogressbar

    def getDisplaySize(self):
        return (self.window.winfo_screenheight(), self.window.winfo_screenwidth())

    def resizeFaceImage(self, image, aspect_ratio=2):
        h, w = self.getDisplaySize()
        prop = h / image.shape[1]
        newSize = (int((prop * image.shape[1]) / aspect_ratio), int((prop * image.shape[0]) / aspect_ratio))
        newImage = cv2.resize(image, (newSize[0], newSize[1]))
        return newImage

    def transformImageToGUI(self, img):
        imgRecolor = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        imgFromArray = Image.fromarray(imgRecolor)
        return ImageTk.PhotoImage(imgFromArray)

    def __init__(self):
        if GUIClass.__instance != None:
            raise Exception("This is a Singleton class. "
                            "Access it through getInstance()")
        else:
            GUIClass.__instance = self

    @staticmethod
    def getInstance():
        if GUIClass.__instance == None:
            GUIClass()
        return GUIClass.__instance

    def createMainWindow(self, title=None, realTime=False):
        windowObject = tk.Tk()
        self.title = title if title is not None else "GUI - Default title"
        windowObject.title(self.title)
        self.window = windowObject
        self.window.config(bg=self.COLORS.BACKGROUNDGENERAL.value)
        self.realTime = realTime
        return windowObject

    def fixedSize(self):
        hDisplay, wDisplay = self.getDisplaySize()
        self.width = wDisplay-wDisplay//10
        self.height = hDisplay-hDisplay//10
        self.window.resizable(width=False, height=False)
        self.window.minsize(width=self.width, height=self.height)
        self.window.maxsize(width=self.width, height=self.height)

    def createPopUpInfo(self):

        popup = tk.Toplevel(self.window)
        popup.resizable(width=False, height=False)
        popup.config(bg=self.COLORS.POPUPINFO.value, bd=6, relief="groove")

        # Nos permite evitar usar la ventana principal mientras esté esta abierta
        popup.grab_set()

        popup.rowconfigure(0, weight=1)
        popup.rowconfigure(1, weight=1)
        popup.rowconfigure(2, weight=1)
        popup.rowconfigure(3, weight=1)
        popup.rowconfigure(4, weight=1)

        popup.wm_title("More information about image " + str(self.namePhoto) + files.extensionJPG)
        nameL = tk.Label(popup, text="Name: \t\t" + self.getInfo("name"), font=(self.textFont, self.textSize), bg=self.COLORS.POPUPINFO.value)
        ageL = tk.Label(popup, text="Age: \t\t" + self.getInfo("age"), font=(self.textFont, self.textSize), bg=self.COLORS.POPUPINFO.value)
        bpL = tk.Label(popup, text="Birthplace: \t" + self.getInfo("birth_place"), font=(self.textFont, self.textSize), bg=self.COLORS.POPUPINFO.value)
        jobL = tk.Label(popup, text="Occupation: \t" + self.getInfo("job"), font=(self.textFont, self.textSize), bg=self.COLORS.POPUPINFO.value)

        backButton = tk.Button(popup, text="Back", command=popup.destroy)
        backButton.config(font=(self.textFont, self.textSizeProgressBar), bg=self.COLORS.BUTTON.value, bd=6, relief="raised")

        nameL.grid(row=0, sticky="w")
        ageL.grid(row=1, sticky="w")
        bpL.grid(row=2, sticky="w")
        jobL.grid(row=3, sticky="w")
        backButton.grid(row=4, pady=(0, 30))

        popup.mainloop()

    def createTop_BottomPanel(self):

        myFrame = tk.Frame(self.window)
        myFrame.config(bg=self.COLORS.BACKGROUNDGENERAL.value)
        myFrame.pack(fill=tk.Y, pady=self.height/30)
        myFrame.rowconfigure(0, weight=4)

        self.myLabelC = tk.Label(myFrame, compound=tk.BOTTOM, text="Original image")
        self.myLabelC.config(font=(self.textFont, self.textSize), bg=self.COLORS.BACKGROUNDIMAGES.value, bd=8,
                        relief="ridge")

        self.myLabelD = tk.Label(myFrame, compound=tk.BOTTOM, text=files.loadInfo()["name"])
        self.myLabelD.grid(row=0, column=1, sticky=tk.E)
        self.myLabelD.config(font=(self.textFont, self.textSize), bg=self.COLORS.BACKGROUNDIMAGES.value, bd=8,
                        relief="ridge")

        if self.realTime:
            self.myLabelC.grid(row=0, column=0)
            idxTextBar = 1
            idxProgressBar = 2
        else:
            self.myLabelC.grid(row=0, column=0, sticky=tk.W)
            myFrame.rowconfigure(1, weight=2)
            buttonInfoLabel = tk.Button(myFrame, text="More information...", command=self.createPopUpInfo)
            buttonInfoLabel.config(font=(self.textFont, self.textSizeProgressBar), bg=self.COLORS.BUTTON.value, bd=6,
                                   relief="raised")
            buttonInfoLabel.grid(row=1, columnspan=2, pady=(self.height / 30, 0))

            idxTextBar = 2
            idxProgressBar = 3

        myFrame.rowconfigure(idxTextBar, weight=1)
        myFrame.rowconfigure(idxProgressBar, weight=2)

        self.pBarLabel = tk.Label(myFrame, text=self.title)
        self.pBarLabel.config(font=(self.textFont, self.textSizeProgressBar), bg=self.COLORS.BACKGROUNDGENERAL.value)
        self.pBarLabel.grid(row=idxTextBar, columnspan=2, sticky=tk.S, pady=(self.height / 30, 0))
        self.pBarLabel.config(text=self.title)

        self.s = ttk.Style()
        # print(s.theme_names()) # default, clam, classic, alt, winnative, vista, xpnative
        self.s.theme_use("classic")
        self.s.configure("TProgressbar", thickness=self.height / 10, background=self.checkColor(0), borderwidth=4,
                    relief="ridge")

        self.progress = ttk.Progressbar(myFrame, orient="horizontal", length=self.width - int(self.width / 10),
                                   mode="determinate", style="TProgressbar")
        self.progress.grid(row=idxProgressBar, columnspan=2, sticky=tk.S, pady=(self.height / 30, 0))
        self.progress["value"] = 0
        self.progress["maximum"] = 100

    def setTitleAndProgress(self, p=0, n=None):
        self.namePhoto = n
        if p > 0:
            self.title = str(p) + " % of coincidence with image: " + str(n) + files.extensionJPG
        else:
            self.title = "No coincidences were found in the database."
        self.window.title(self.title)
        self.pBarLabel.config(text=self.title)
        self.info = files.loadInfo(n)

        self.progress["value"] = p
        self.s.configure("TProgressbar", background=self.checkColor(p))

        txtIf.printMessage(txtIf.MESSAGES.DISPLAY_WITH_COINCIDENCE, str(p) + "%")

    def setImage(self, image=None, left=True, staticImage=True):
        image = image if (image is not None) else files.loadImage()
        if staticImage:
            image = self.resizeFaceImage(image)
        img = self.transformImageToGUI(image)
        panel = self.myLabelC if left else self.myLabelD
        panel.image = img
        panel.configure(image=img)
        if not left:
            panel.configure(text=files.loadInfo(self.namePhoto)["name"])
