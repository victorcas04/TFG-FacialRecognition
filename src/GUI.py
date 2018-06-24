
# encoding: utf-8

'''
@author: victorcas
'''

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

    '''
    GUI Class in which we create the main window of the interface, add visual information, etc.
    '''

    class COLORS(Enum):

        '''
        COLORS Class necessary to make and use properly the enumeration type.
        Change the String values to change colors of interface.
        '''

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

    '''
    Need an instance variable cause this is gonna be a singleton (only a window can be displayed at a time).
    '''
    __instance = None

    '''
    Some general personalization of the interface.
    '''
    textFont = "Helvetica"
    textSize = 22
    textSizeProgressBar = 18

    def displayWindow(self):

        '''
        Makes main window to show up
        '''

        self.window.mainloop()


    def selectFile(self):

        '''
        Creates a window (not the main one) that allows us to select an image in our system.
        :return: nFile: String
            Full path of the image in our system.
        '''

        txtIf.printMessage(txtIf.MESSAGES.SELECT_IMAGE)
        askFileWindow = tk.Tk()
        askFileWindow.title("Select an image...")
        askFileWindow.filename = fd.askopenfilename(initialdir="/", title="Select file",
                                          filetypes=(
                                          ("jpeg files", '*'+files.extensionJPG),
                                          ("png files", '*'+files.extensionPNG),
                                          ("all files", "*.*")))
        nFile = askFileWindow.filename
        askFileWindow.destroy()
        return nFile


    def loadImageByGUI(self):

        '''
        Loads an image selected with the interface or a default one if the image doesn't match the requirements.
        :return: imageToReturn: Image
            Image loaded by interface selection.
        '''

        imageToReturn = self.selectFile()
        if (imageToReturn.endswith(files.extensionJPG) or imageToReturn.endswith(files.extensionPNG)):
            '''
            The image must have 'jpg' or 'png' extension to be loaded...
            (this is done to avoid the user to load any kind of file, more available extensions can be added)
            '''
            imageToReturn = files.loadImage(imageToReturn)
        else:
            '''
            ...otherwise load a default one.
            '''
            txtIf.printError(txtIf.ERRORS.FILE_WRONG_FORMAT)
            imageToReturn = files.loadImage()

        return imageToReturn


    def getInfo(self, param):

        '''
        Loads only part of the information stored about an image.
        :param param: String
            Parameter that will be loaded from the information stored in our instance (name, age, birth_place or job).
        :return: information: String
            Information loaded.
        '''

        return self.info[param]


    def checkColor(self, p):

        '''
        Changes the color of the bar depending on the percentage.
        :param p: float
            Percentage of coincidence of image (from 'CompareImages').
        :return: colorprogressbar: String
            Color in RGB that will be loaded.
        '''

        '''
        New colors can sections can be added, but the colors must be in the COLORS class defined above.
        '''
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

        '''
        Get size of our main screen (in order to make interface window variable).
        :return: height: Integer
            Screen height.
        :return: width: Integer
            Screen width.
        '''

        return (self.window.winfo_screenheight(), self.window.winfo_screenwidth())


    def resizeFaceImage(self, image, aspect_ratio=2):

        '''
        Resize an image to fit the interface size.
        :param image: Image
            Image to be resized.
        :param aspect_ratio: Float
            Aspect ratio that the new image will have (bigger aspect-ration means smaller image and viceversa).
        :return: newImage: Image
            Image resized.
        '''

        h, w = self.getDisplaySize()
        prop = h / image.shape[1]
        newSize = (int((prop * image.shape[1]) / aspect_ratio), int((prop * image.shape[0]) / aspect_ratio))
        newImage = cv2.resize(image, (newSize[0], newSize[1]))
        return newImage


    def transformImageToGUI(self, img):

        '''
        Standard image type is not compatible with tKinter, so this method transform it to correct type.
        :param img: Image
            Original image loaded with OpenCV.
        :return: image: ImageTk
            Image transformed to a tKinter compatible type.
        '''

        imgRecolor = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        imgFromArray = Image.fromarray(imgRecolor)
        return ImageTk.PhotoImage(imgFromArray)


    def __init__(self):

        '''
        Constructor of GUI Class (not accesible by other classes, so call 'getInstance()' instead).
        :raise Exception
            Not public callable.
        '''

        if GUIClass.__instance != None:
            raise Exception("This is a Singleton class. "
                            "Access it through getInstance()")
        else:
            GUIClass.__instance = self


    @staticmethod
    def getInstance():

        '''
        Singleton getInstance() method.
        :return: __instance: GUIClass
            Instance of GUI Class.
        '''

        if GUIClass.__instance == None:
            GUIClass()
        return GUIClass.__instance


    def createMainWindow(self, title=None, realTime=False):

        '''
        Creates empty main window, but needs to add images and information with other methods.
        :param title: String
            Title of the window, if none is provided, a default one is used.
        :param realTime: boolean
            Parameter to know if the interface must be updated over time (recognition in real time) or not.
        :return: windowObject: WindowTk
            Main window object used in the rest of the class.
        '''

        windowObject = tk.Tk()
        self.title = title if title is not None else "GUI - Default title"
        windowObject.title(self.title)
        self.window = windowObject
        self.window.config(bg=self.COLORS.BACKGROUNDGENERAL.value)
        self.realTime = realTime

        return windowObject


    def fixedSize(self):

        '''
        Set the interface size to fit in the screen (90% of full width and height).
        Disables the manual resize of the window to avoid consistency problems with visual elements.
        '''

        hDisplay, wDisplay = self.getDisplaySize()
        self.width = wDisplay-wDisplay//10
        self.height = hDisplay-hDisplay//10
        self.window.resizable(width=False, height=False)
        self.window.minsize(width=self.width, height=self.height)
        self.window.maxsize(width=self.width, height=self.height)


    def createPopUpInfo(self):

        '''
        Creates the 'pop-up' window that displays more information about the person idetified.
        '''

        '''
        Create and configure window. Like the main one, this cannot be resized either. 
        '''
        popup = tk.Toplevel(self.window)
        popup.resizable(width=False, height=False)
        popup.config(bg=self.COLORS.POPUPINFO.value, bd=6, relief="groove")

        '''
        With this line, we avoid main window to be operational, so the user cannot create multiple pop-up windows.
        '''
        popup.grab_set()

        popup.rowconfigure(0, weight=1)
        popup.rowconfigure(1, weight=1)
        popup.rowconfigure(2, weight=1)
        popup.rowconfigure(3, weight=1)
        popup.rowconfigure(4, weight=1)

        '''
        Set the information that's gonna be displayed.
        '''
        popup.wm_title("More information about image " + str(self.namePhoto) + files.extensionJPG)
        nameL = tk.Label(popup, text="Name: \t\t" + self.getInfo("name"), font=(self.textFont, self.textSize), bg=self.COLORS.POPUPINFO.value)
        ageL = tk.Label(popup, text="Age: \t\t" + self.getInfo("age"), font=(self.textFont, self.textSize), bg=self.COLORS.POPUPINFO.value)
        bpL = tk.Label(popup, text="Birthplace: \t" + self.getInfo("birth_place"), font=(self.textFont, self.textSize), bg=self.COLORS.POPUPINFO.value)
        jobL = tk.Label(popup, text="Occupation: \t" + self.getInfo("job"), font=(self.textFont, self.textSize), bg=self.COLORS.POPUPINFO.value)

        '''
        Creates a button to close this pop-up window and continue to the main one.
        '''
        backButton = tk.Button(popup, text="Back", command=popup.destroy)
        backButton.config(font=(self.textFont, self.textSizeProgressBar), bg=self.COLORS.BUTTON.value, bd=6, relief="raised")

        nameL.grid(row=0, sticky="w")
        ageL.grid(row=1, sticky="w")
        bpL.grid(row=2, sticky="w")
        jobL.grid(row=3, sticky="w")
        backButton.grid(row=4, pady=(0, 30))

        '''
        Displays the pop-up.
        '''
        popup.mainloop()


    def createTop_BottomPanel(self):

        '''
        Creates main panel, which contains all the elements from the interface.
        '''

        myFrame = tk.Frame(self.window)
        myFrame.config(bg=self.COLORS.BACKGROUNDGENERAL.value)
        myFrame.pack(fill=tk.Y, pady=self.height/30)

        '''
        First we configure labels where the images are gonna be displayed.
        '''
        myFrame.rowconfigure(0, weight=4)

        '''
        Left image (captured).
        '''
        self.myLabelC = tk.Label(myFrame, compound=tk.BOTTOM, text="Original image")
        self.myLabelC.config(font=(self.textFont, self.textSize), bg=self.COLORS.BACKGROUNDIMAGES.value, bd=8,
                        relief="ridge")

        '''
        Right image (from database).
        '''
        self.myLabelD = tk.Label(myFrame, compound=tk.BOTTOM, text=files.loadInfo()["name"])
        self.myLabelD.grid(row=0, column=1, sticky=tk.E)
        self.myLabelD.config(font=(self.textFont, self.textSize), bg=self.COLORS.BACKGROUNDIMAGES.value, bd=8,
                        relief="ridge")

        '''
        The distribution changes if we are in real-time mode or not.
        '''
        if self.realTime:
            '''
            If we are in real time, the left image will be centered (cause we have not the 
                'More information...' button in the middle)
            '''
            self.myLabelC.grid(row=0, column=0)

            '''
            Set the positions inside the panel of the coincidence bar.
            '''
            idxTextBar = 1
            idxProgressBar = 2

        else:
            '''
            If we are not in real time, the image captured will be indented to the left.
            '''
            self.myLabelC.grid(row=0, column=0, sticky=tk.W)

            '''
            As we are not in real time, configure the label in wich the button is gonna be, and then create it 
                and assign the method that creates the pop-up ('command=self.createPopUpInfo').
            '''
            myFrame.rowconfigure(1, weight=2)
            buttonInfoLabel = tk.Button(myFrame, text="More information...", command=self.createPopUpInfo)
            buttonInfoLabel.config(font=(self.textFont, self.textSizeProgressBar), bg=self.COLORS.BUTTON.value, bd=6,
                                   relief="raised")
            buttonInfoLabel.grid(row=1, columnspan=2, pady=(self.height / 30, 0))

            '''
            Set the positions inside the panel of the coincidence bar.
            '''
            idxTextBar = 2
            idxProgressBar = 3

        '''
        Configure the labels where the coincidence bar is gonna be.
        '''
        myFrame.rowconfigure(idxTextBar, weight=1)
        myFrame.rowconfigure(idxProgressBar, weight=2)

        '''
        Information on top of the bar.
        '''
        self.pBarLabel = tk.Label(myFrame, text=self.title)
        self.pBarLabel.config(font=(self.textFont, self.textSizeProgressBar), bg=self.COLORS.BACKGROUNDGENERAL.value)
        self.pBarLabel.grid(row=idxTextBar, columnspan=2, sticky=tk.S, pady=(self.height / 30, 0))
        self.pBarLabel.config(text=self.title)

        '''
        To create a progress bar and change values dynamically, we must use 'ttk' library and create a new style.
        Available themes are: default, clam, classic, alt, winnative, vista and xpnative.
        '''
        self.s = ttk.Style()
        self.s.theme_use("classic")
        self.s.configure("TProgressbar", thickness=self.height / 10, background=self.checkColor(0), borderwidth=4,
                    relief="ridge")

        '''
        Now create the progress bar and assign the style to it.
        '''
        self.progress = ttk.Progressbar(myFrame, orient="horizontal", length=self.width - int(self.width / 10),
                                   mode="determinate", style="TProgressbar")
        self.progress.grid(row=idxProgressBar, columnspan=2, sticky=tk.S, pady=(self.height / 30, 0))
        self.progress["value"] = 0
        self.progress["maximum"] = 100


    def setTitleAndProgress(self, p=0, n=None):

        '''
        Set the text that goes above the progress bar and on the title.
        Also changes color and value of the coincidence bar according to the percentage.
        :param p: float
            Percentage of coincidence between both images.
        :param n: String
            Name of the image that is currently display on the right side of the interface (from database).
        '''

        self.namePhoto = n
        if p > 0:
            '''
            Default image name ends with jpg, but we can change that to take the name directly from database instead
                of passing it as a parameter, but this way is simpler, and it's supposed to work on a 
                controlled environment.
            '''
            self.title = str(p) + " % of coincidence with image: " + str(n) + files.extensionJPG

        else:
            '''
            In case we have 0% of coincidence (never less, because we control it in other class), 
                we display the next message.
            '''
            self.title = "No coincidences were found in the database."

        '''
        Change the title, the information and the value of the progress bar.
        '''
        self.window.title(self.title)
        self.pBarLabel.config(text=self.title)
        self.info = files.loadInfo(n)
        self.progress["value"] = p
        self.s.configure("TProgressbar", background=self.checkColor(p))
        txtIf.printMessage(txtIf.MESSAGES.DISPLAY_WITH_COINCIDENCE, str(p) + "%")


    def setImage(self, image=None, left=True, staticImage=True):

        '''
        Set a new image into the interface (in one side or another).
        :param image: Image
            Image to be displayed on the interface.
        :param left: boolean
            If True, the image is gonna be set to the left.
            If False, the image is gonna be set to the right.
        :param staticImage: boolean
            To solve a problem about resizing the same image more than once, we must change this parameter to
                False when we call this method from the real time recognition part.
        '''

        '''
        Load a default image in case none is passed.
        '''
        image = image if (image is not None) else files.loadImage()
        if staticImage:
            image = self.resizeFaceImage(image)
        img = self.transformImageToGUI(image)

        '''
        Set the image to the left panel or to the right.
        '''
        panel = self.myLabelC if left else self.myLabelD
        panel.image = img
        panel.configure(image=img)

        '''
        If the panel is the left, it already has a text by default ('Original image'), but if it is the right one, 
            we must set the title for the panel. In our case the title will be the name of the person recognized.
        '''
        if not left:
            panel.configure(text=files.loadInfo(self.namePhoto)["name"])
