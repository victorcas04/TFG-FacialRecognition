
import tkinter as tk
from PIL import Image
from PIL import ImageTk
import cv2

class GUIClass(object):

    window = None
    panelL = None
    panelR = None
    panelB = None

    def __init__(self):
        self.window = self.createWindow()

    def createWindow(self):
        windowObject = tk.Tk()
        windowObject.title("Image Detection")
        return windowObject

    def panelTest(self, image=None, label="Default Label", side="left"):

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
            panel.pack(side=side, padx=10, pady=30)
        else:
            panel.configure(text=label)
            panel.configure(image=img)
            panel.image = img

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

