
import Util as util
from GUI import GUIClass as gui
import wx

pathDatasetFullImages = "../sources/dataset"
pathDatasetFacesImages = "../sources/facesDataset"
imageByCamera = True
#  [0] para la webcam integrada en el portatil
#  [1] para la cámara externa
# [-1] para menú
camera = 1

if __name__ == "__main__":

    print("\n\nTFG - Facial Recognition - Víctor de Castro Hurtado\n\n")

    # Dependiendo de las imágenes que vayamos a usar usamos un path u otro
    pathh = pathDatasetFacesImages

    util.askTrain(pathh)

    guiMain = gui.getInstance()
    app = wx.App(False)
    w, h = wx.GetDisplaySize()
    guiMain.fixedSize(h, w)

    if imageByCamera:
        # Sacamos la imágen que queremos identificar desde la cámara
        photoOriginal = util.faceInBoxVideo(camera)
    else:
        # Sacamos la imágen que queremos identificar desde un archivo (en modo gráfico)
        # C:\Users\victo\Desktop\DEVELOPMENT\projects\PycharmProjects\TFG-FacialRecognition\TFG-FacialRecognition\sources\facesDataset
        photoOriginal = util.loadImageByGUI(guiMain)

    # Imágen resultado / Porcentaje comparación / Nombre imágen resultado
    i, p, n = util.compare(photoOriginal, path=pathh)

    guiMain.setTitle(n, p)

    # Si nuestra mejor coincidencia no supera el umbral especificado, mostramos una imágen por defecto con un mensaje indicándonoslo.
    # Hay imágenes que al compararlas quedna números negativos al no encontrar resultados o resultados muy malos, por eso ponemos el umbral tan bajo.
    pMinComp = 0
    if p < pMinComp:
        print("\nLa comparación ha obtenido menos de un " + str(pMinComp) + "% de coincidencia. Cargando imágen por defecto.")
        i = util.loadImage()

    pOri = util.cutFaceFromImage(photoOriginal)[1] if pathh.__eq__(pathDatasetFacesImages) else photoOriginal

    util.displayInterfaceWindow(guiMain, photoFromCamera=util.resizeFaceImage(pOri), photoFromDatabase=util.resizeFaceImage(i), percentage=p)
