
import tkinter as tk
from tkinter import ttk
from PIL import Image
from PIL import ImageTk
import cv2
from tkinter import filedialog as fd

class GUIClass(object):

    __instance = None

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
        self.window.resizable(width=False, height=False)
        self.window.minsize(width=wDisplay, height=hDisplay)
        self.window.maxsize(width=wDisplay, height=hDisplay)

    def createWindow(self):
        windowObject = tk.Tk()
        windowObject.title("Image Detection - Default Title")
        return windowObject

    def setTitle(self, name, p):
        self.percentage = p
        if name is not None:
            self.title = str(p) + " % de coincidencia con " + str(name)
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


    def addPercentageBar(self, displaySize, p):

        self.progress = ttk.Progressbar(self.window, orient="horizontal", length=displaySize[1]/2, mode="determinate")
        self.progress.pack(side=tk.BOTTOM, pady=(0, displaySize[0]/10))
        self.progress["value"] = p
        self.progress["maximum"] = 100
        p = tk.Label(self.window, text=self.title)
        p.pack(side=tk.BOTTOM)


    def createTop_BottomPanel(self, photoFromCamera, photoFromDatabase, display, p):

        t = display[0]/30

        myFrame = tk.Frame(self.window)     # bd=1, , relief="sunken"
        myFrame.pack(fill=tk.Y, pady=t)
        myFrame.rowconfigure(0, weight=10)
        myFrame.rowconfigure(1, weight=1)

        imgCRecolor = cv2.cvtColor(photoFromCamera, cv2.COLOR_BGR2RGB)
        imgCFromArray = Image.fromarray(imgCRecolor)
        imgC = ImageTk.PhotoImage(imgCFromArray)
        myLabelC = tk.Label(myFrame, compound=tk.BOTTOM, image=imgC, text="Camera Image")
        myLabelC.grid(row=0, sticky=tk.W, padx=(0, display[1]))
        myLabelC.image = imgC
        myLabelC.config(font=("Times New Roman", 22))

        imgDRecolor = cv2.cvtColor(photoFromDatabase, cv2.COLOR_BGR2RGB)
        imgDFromArray = Image.fromarray(imgDRecolor)
        imgD = ImageTk.PhotoImage(imgDFromArray)
        myLabelD = tk.Label(myFrame, compound=tk.BOTTOM, image=imgD, text="Database Image")
        myLabelD.grid(row=0, sticky=tk.E, padx=(display[1], 0))
        myLabelD.image = imgD
        myLabelD.config(font=("Times New Roman", 22))

        s = ttk.Style()
        s.theme_use("default")
        s.configure("TProgressbar", thickness=t)
        progress = ttk.Progressbar(myFrame, orient="horizontal", length=display[1], mode="determinate", style="TProgressbar")
        progress.grid(row=1, sticky=tk.N, pady=(display[0]/10, 0))
        progress["value"] = p
        progress["maximum"] = 100
        p = tk.Label(myFrame, text=self.title)
        p.config(font=("Times New Roman", 18))
        p.grid(row=1, sticky=tk.S, pady=(0, t + display[0]/100))


    def displayWindow(self):
        # Using mainloop() to show image
        self.window.mainloop()


    def selectFile(self):
        afw = tk.Toplevel(self.window)

        afw.filename = fd.askopenfilename(initialdir="/", title="Select file",
                                          filetypes=(
                                          ("jpeg files", "*.jpg"), ("png files", "*.png*"), ("all files", "*.*")))

        z = afw.filename
        afw.destroy()
        print("Archivo leído: " + str(z))
        return z