
import tkinter as tk
from tkinter import ttk
from PIL import Image
from PIL import ImageTk
import cv2
from tkinter import filedialog as fd

class GUIClass(object):

    __instance = None
    textFont = "Helvetica"
    textSize = 22
    textSizeProgressBar = 18

    @staticmethod
    def getInstance():
        if GUIClass.__instance == None:
            GUIClass()
        return GUIClass.__instance

    def __init__(self):
        if GUIClass.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            GUIClass.__instance = self
            self.window = self.createWindow()

    def fixedSize(self, hDisplay, wDisplay):
        self.width = wDisplay-int(wDisplay/10)
        self.height = hDisplay-int(hDisplay/10)
        self.window.resizable(width=False, height=False)
        self.window.minsize(width=self.width, height=self.height)
        self.window.maxsize(width=self.width, height=self.height)

    def createWindow(self):
        windowObject = tk.Tk()
        windowObject.title("Image Detection - Default Title")
        return windowObject

    def getInfo(self, param):
        return self.info[param]

    def initialize(self, namePhoto, p, inf):
        self.percentage = p
        self.namePhoto = namePhoto
        self.info = inf
        if namePhoto is not None:
            self.title = str(p) + " % de coincidencia con " + str(namePhoto)
        else:
            self.title = "No se han encontrado coincidencias en la base de datos."
        self.window.title(self.title)

    def addPercentageLabel(self, percentage="0%"):

        percentageText = "Imágenes con un " + percentage + " de coincidencia"

        panel = self.panelB
        if panel is None:
            panel = tk.Label(self.window, text=percentageText)
            panel.pack(side=tk.BOTTOM)
        else:
            panel.configure(text=percentageText)

    def createPopUpInfo(self):

        popup = tk.Toplevel(self.window)
        popup.resizable(width=False, height=False)

        popup.rowconfigure(0, weight=1); popup.rowconfigure(1, weight=1); popup.rowconfigure(2, weight=1); popup.rowconfigure(3, weight=1); popup.rowconfigure(4, weight=1)

        popup.wm_title("Más información acerca de " + str(self.namePhoto))
        nameL = tk.Label(popup, text="Nombre: " + self.getInfo("name"), font=(self.textFont, self.textSize))
        ageL = tk.Label(popup, text="Edad: " + self.getInfo("age"), font=(self.textFont, self.textSize))
        bpL = tk.Label(popup, text="Lugar de nacimiento: " + self.getInfo("birth_place"), font=(self.textFont, self.textSize))
        jobL = tk.Label(popup, text="Ocupación: " + self.getInfo("job"), font=(self.textFont, self.textSize))

        backButton = tk.Button(popup, text="Atras", command=popup.destroy)
        backButton.config(font=(self.textFont, self.textSizeProgressBar))

        nameL.grid(row=0); ageL.grid(row=1); bpL.grid(row=2); jobL.grid(row=3); backButton.grid(row=4, pady=(0, 30))

        popup.mainloop()

    def createTop_BottomPanel(self, photoFromCamera, photoFromDatabase, p):

        myFrame = tk.Frame(self.window)     # bd=1, , relief="sunken"
        myFrame.pack(fill=tk.Y, pady=self.height/30)
        myFrame.rowconfigure(0, weight=4)
        myFrame.rowconfigure(1, weight=2)
        myFrame.rowconfigure(2, weight=1)
        myFrame.rowconfigure(3, weight=2)

        imgCRecolor = cv2.cvtColor(photoFromCamera, cv2.COLOR_BGR2RGB)
        imgCFromArray = Image.fromarray(imgCRecolor)
        imgC = ImageTk.PhotoImage(imgCFromArray)

        myLabelC = tk.Label(myFrame, compound=tk.BOTTOM, image=imgC, text="Camera Image")
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

        buttonInfoLabel = tk.Button(myFrame, text="Más Información...", command=self.createPopUpInfo)
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

        print("Selecciona una imágen.")

        afw = tk.Toplevel(self.window)
        afw.filename = fd.askopenfilename(initialdir="/", title="Select file",
                                          filetypes=(
                                          ("jpeg files", "*.jpg"), ("png files", "*.png*"), ("all files", "*.*")))
        z = afw.filename
        afw.destroy()
        return z