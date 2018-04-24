
import tkinter as tk
from tkinter import filedialog as fd
from tkinter import ttk
from PIL import Image
from PIL import ImageTk
import cv2

class GUIClass(object):

    panelL = None
    panelR = None

    def __init__(self):
        self.window = self.createWindow()

    def fixedSize(self, hDisplay, wDisplay):
        self.window.resizable(width=False, height=False)
        self.window.minsize(width=wDisplay, height=hDisplay)
        #self.window.maxsize(width=666, height=666)
        self.window.maxsize(width=wDisplay, height=hDisplay)

    def createWindow(self):
        windowObject = tk.Tk()
        windowObject.title("Image Detection - Default Title")
        return windowObject

    def setTitle(self, nF, p):
        self.nameFile = nF
        self.percentage = p
        if nF is not None:
            self.title = str(p) + " % coincidencia con imágen " + str(nF)
        else:
            self.title = "No se han encontrado coincidencias en la base de datos."
        self.window.title(self.title)

    def createPanel(self, image=None, label="Default Label", side="left", displaySize=None):

        imgRecolor = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        imgFromArray = Image.fromarray(imgRecolor)
        img = ImageTk.PhotoImage(imgFromArray)

        if side.__eq__("left"):
            panel = self.panelL
        else:
            panel = self.panelR

        if panel is None:
            panel = tk.Label(self.window, compound=tk.BOTTOM, image=img, text=label)
            panel.image = img
            panel.pack(side=side, padx=10)
        else:
            panel.configure(text=label)
            panel.configure(image=img)
            panel.image = img

        return panel

        #panel = tk.Label(self.window, compound=tk.CENTER, text=label, image=image)
        #panel.image = image
        #panel.pack(side=side)

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

        myFrame = tk.Frame(self.window, bd=1, relief="sunken")
        myFrame.pack(fill=tk.Y, pady=display[0]/10)
        myFrame.rowconfigure(0, weight=10)
        myFrame.rowconfigure(1, weight=1)

        #self.panelL = self.createPanel(photoFromCamera, "Original Image", "left", display)
        #self.panelR = self.createPanel(photoFromDatabase, "Founded Image", "right", display)
        #self.addPercentageBar(display, p)

        imgRecolor = cv2.cvtColor(photoFromCamera, cv2.COLOR_BGR2RGB)
        imgFromArray = Image.fromarray(imgRecolor)
        img = ImageTk.PhotoImage(imgFromArray)
        myLabel1 = tk.Label(myFrame, compound=tk.BOTTOM, image=img, text="Original Image")
        myLabel1.grid(row=0, sticky=tk.W, padx=(0, display[1]/2))
        myLabel1.image = img
        #myLabel1.pack(side="left", padx=10)

        imgRecolor2 = cv2.cvtColor(photoFromDatabase, cv2.COLOR_BGR2RGB)
        imgFromArray2 = Image.fromarray(imgRecolor2)
        img2 = ImageTk.PhotoImage(imgFromArray2)
        myLabel2 = tk.Label(myFrame, compound=tk.BOTTOM, image=img2, text="Founded Image")
        myLabel2.grid(row=0, sticky=tk.E, padx=(display[1]/2, 0))
        myLabel2.image = img2
        #myLabel2.pack(side="right", padx=10)

        s = ttk.Style()
        s.theme_use("default")
        t = 30
        s.configure("TProgressbar", thickness=t)
        progress = ttk.Progressbar(myFrame, orient="horizontal", length=display[1] / 2, mode="determinate", style="TProgressbar")
        progress.grid(row=1, sticky=tk.N, pady=(display[0]/10, 0))
        #progress.pack(side=tk.BOTTOM, pady=(0, display[0] / 10))
        progress["value"] = p
        progress["maximum"] = 100
        p = tk.Label(myFrame, text=self.title)
        p.grid(row=1, sticky=tk.S, pady=(0, t + display[0]/100))
        #p.pack(side=tk.BOTTOM)

    '''
    def addLabel(self, label="Default Label", side="left"):

        if side.__eq__("left"):
            panel = self.panelL
        else:
            panel = self.panelR

        if panel is None:
            panel = tk.Label(compound=tk.CENTER, text=label, image=None)
            panel.pack(side=side)
    '''
    '''
    def addImage(self, image, side="left"):

        imgRecolor = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        imgFromArray = Image.fromarray(imgRecolor)
        img = ImageTk.PhotoImage(imgFromArray)

        if side.__eq__("left"):
            panel = self.panelL
        else:
            panel = self.panelR

        if panel is None:
            panel = self.addLabel(side=side)
            panel.image = img
            panel.pack(side=side, padx=10, pady=10)
        else:
            panel.configure(image=img)
            panel.image = img

    '''
    def displayWindow(self):
        # Using mainloop() to show image
        self.window.mainloop()

    def selectFile(self):

        afw = tk.Toplevel(self.window)

        #z = fd.askopenfilename()
        afw.filename = fd.askopenfilename(initialdir="/", title="Select file",
                                                     filetypes=(("jpeg files", "*.jpg"), ("png files", "*.png*"), ("all files", "*.*")))
        print ("Archivo leído: " + str(afw.filename))
        z = afw.filename
        afw.destroy()
        return z

