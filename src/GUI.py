
# encoding: utf-8

from __future__ import division
import tkinter as tk
from tkinter import ttk
import Util as util
from PIL import Image, ImageTk
import cv2, wx
from tkinter import filedialog as fd

class GUIClass(object):

    __instance = None
    textFont = "Helvetica"
    textSize = 22
    textSizeProgressBar = 18

    def __init__(self):
        if GUIClass.__instance != None:
            raise Exception("This is a Singleton class. Access it through getInstance()")
        else:
            GUIClass.__instance = self
            self.window = self.createWindow()

    @staticmethod
    def getInstance():
        if GUIClass.__instance == None:
            GUIClass()
        return GUIClass.__instance

    def getDisplaySize(self):
        app = wx.App(False)
        w, h = wx.GetDisplaySize()
        return h, w

    def fixedSize(self):
        hDisplay, wDisplay = self.getDisplaySize()
        self.width = wDisplay-wDisplay//10
        self.height = hDisplay-hDisplay//10
        self.window.resizable(width=False, height=False)
        self.window.minsize(width=self.width, height=self.height)
        self.window.maxsize(width=self.width, height=self.height)

    def displayInterfaceWindow(self, originalPhoto=util.loadImage(), photoFromDatabase=util.loadImage(), percentage=0.0):

        def resizeFaceImage(image, aspect_ratio=2):
            h, w = self.getDisplaySize()
            prop = h / image.shape[1]
            newSize = (int((prop * image.shape[1]) / aspect_ratio), int((prop * image.shape[0]) / aspect_ratio))
            newImage = cv2.resize(image, (newSize[0], newSize[1]))
            return newImage

        percentageString = str(percentage) + "%"
        print("\nDisplaying result with a " + percentageString + " of coincidence.\n")

        self.createTop_BottomPanel(resizeFaceImage(originalPhoto), resizeFaceImage(photoFromDatabase), percentage)
        self.displayWindow()

    def createWindow(self):
        windowObject = tk.Tk()
        windowObject.title("GUI - Default title")
        return windowObject

    def getInfo(self, param):
        return self.info[param]

    def initialize(self, namePhoto, p, inf):
        self.percentage = p
        self.namePhoto = namePhoto
        self.info = inf
        if namePhoto is not None:
            self.title = str(p) + " % of coincidence with image: " + str(namePhoto) + util.extensionJPG
        else:
            self.title = "No coincidences were found in the database."
        self.window.title(self.title)

    def addPercentageLabel(self, percentage="0%"):

        percentageText = "Images with a " + percentage + " of coincidence"

        panel = self.panelB
        if panel is None:
            panel = tk.Label(self.window, text=percentageText)
            panel.pack(side=tk.BOTTOM)
        else:
            panel.configure(text=percentageText)

    def createPopUpInfo(self):

        popup = tk.Toplevel(self.window)
        popup.resizable(width=False, height=False)

        # Nos permite evitar usar la ventana principal mientras esté esta abierta
        popup.grab_set()

        popup.rowconfigure(0, weight=1)
        popup.rowconfigure(1, weight=1)
        popup.rowconfigure(2, weight=1)
        popup.rowconfigure(3, weight=1)
        popup.rowconfigure(4, weight=1)

        popup.wm_title("More information about image " + str(self.namePhoto) + util.extensionJPG)
        nameL = tk.Label(popup, text="Name: \t\t" + self.getInfo("name"), font=(self.textFont, self.textSize))
        ageL = tk.Label(popup, text="Age: \t\t" + self.getInfo("age"), font=(self.textFont, self.textSize))
        bpL = tk.Label(popup, text="Birthplace: \t" + self.getInfo("birth_place"), font=(self.textFont, self.textSize))
        jobL = tk.Label(popup, text="Occupation: \t" + self.getInfo("job"), font=(self.textFont, self.textSize))

        backButton = tk.Button(popup, text="Back", command=popup.destroy)
        backButton.config(font=(self.textFont, self.textSizeProgressBar))

        nameL.grid(row=0, sticky="w")
        ageL.grid(row=1, sticky="w")
        bpL.grid(row=2, sticky="w")
        jobL.grid(row=3, sticky="w")
        backButton.grid(row=4, pady=(0, 30))

        popup.mainloop()

    def createTop_BottomPanel(self, photoFromCamera, photoFromDatabase, p):

        myFrame = tk.Frame(self.window) 
        myFrame.pack(fill=tk.Y, pady=self.height/30)
        myFrame.rowconfigure(0, weight=4)
        myFrame.rowconfigure(1, weight=2)
        myFrame.rowconfigure(2, weight=1)
        myFrame.rowconfigure(3, weight=2)

        imgCRecolor = cv2.cvtColor(photoFromCamera, cv2.COLOR_BGR2RGB)
        imgCFromArray = Image.fromarray(imgCRecolor)
        imgC = ImageTk.PhotoImage(imgCFromArray)

        myLabelC = tk.Label(myFrame, compound=tk.BOTTOM, image=imgC, text="Original image")
        myLabelC.grid(row=0, column = 0, sticky=tk.W)
        myLabelC.image = imgC
        myLabelC.config(font=(self.textFont, self.textSize))

        imgDRecolor = cv2.cvtColor(photoFromDatabase, cv2.COLOR_BGR2RGB)
        imgDFromArray = Image.fromarray(imgDRecolor)
        imgD = ImageTk.PhotoImage(imgDFromArray)

        myLabelD = tk.Label(myFrame, compound=tk.BOTTOM, image=imgD, text=self.getInfo("name"))
        myLabelD.grid(row=0, column=1, sticky=tk.E)
        myLabelD.image = imgD
        myLabelD.config(font=(self.textFont, self.textSize))

        s = ttk.Style()
        s.theme_use("default")
        s.configure("TProgressbar", thickness=self.height/10)

        buttonInfoLabel = tk.Button(myFrame, text="More information...", command=self.createPopUpInfo)
        buttonInfoLabel.config(font=(self.textFont, self.textSizeProgressBar))
        buttonInfoLabel.grid(row=1, columnspan=2, pady=(self.height/30, 0))

        pBarLabel = tk.Label(myFrame, text=self.title)
        pBarLabel.config(font=(self.textFont, self.textSizeProgressBar))
        pBarLabel.grid(row=2, columnspan=2, sticky=tk.S, pady=(self.height/30, 0))

        progress = ttk.Progressbar(myFrame, orient="horizontal", length=self.width-int(self.width/10), mode="determinate", style="TProgressbar")
        progress.grid(row=3, columnspan=2, sticky=tk.S, pady=(self.height/30, 0))
        progress["value"] = p
        progress["maximum"] = 100

    def displayWindow(self):
        # Using mainloop() to show image
        self.window.mainloop()

    def selectFile(self):
        print("Select an image...")
        afw = tk.Toplevel(self.window)
        afw.filename = fd.askopenfilename(initialdir="/", title="Select file",
                                          filetypes=(
                                          ("jpeg files", '*'+util.extensionJPG), ("png files", '*'+util.extensionPNG), ("all files", "*.*")))
        z = afw.filename
        afw.destroy()
        return z

    def loadImageByGUI(self):
        imageToReturn = self.selectFile()
        return util.loadImage(imageToReturn) if (
                    imageToReturn.endswith(util.extensionJPG) or imageToReturn.endswith(util.extensionPNG)) \
            else util.loadImage()