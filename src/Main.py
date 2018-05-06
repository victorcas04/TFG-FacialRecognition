
import src.Util as util
from src.GUI import GUIClass as gui
import wx

pathDatasetFullImages = "../sources/dataset"
pathDatasetFacesImages = "../sources/facesDataset"

if __name__ == "__main__":

    print("\n\nTFG - Facial Recognition - Víctor de Castro Hurtado\n\n")

    # Dependiendo de las imágenes que vayamos a usar usamos un path u otro
    pathh = pathDatasetFacesImages

    util.askTrain(pathh)

    guiMain = gui.getInstance()
    app = wx.App(False)
    w, h = wx.GetDisplaySize()
    guiMain.fixedSize(h, w)

    # Sacamos la imágen que queremos identificar desde la cámara
    photoOriginal = util.faceInBoxVideo()
    # Sacamos la imágen que queremos identificar desde un archivo (en modo texto)
    #photoOriginal = util.loadImageByName(util.getFileName(meDNI))
    # Sacamos la imágen que queremos identificar desde un archivo (en modo gráfico)
    #photoOriginal = util.loadImageByGUI(guiMain)

    # Imágen resultado / Porcentaje comparación / Nombre imágen resultado
    i, p, n = util.compare(photoOriginal, path=pathh)

    guiMain.setTitle(n, p)

    # Si nuestra mejor coincidencia no supera el 50%, mostramos una imágen por defecto con un mensaje indicándonoslo.
    pMinComp = 50
    if p < pMinComp:
        print("\nLa comparación ha obtenido menos de un " + str(pMinComp) + "% de coincidencia. Cargando imágen por defecto.")
        i = util.loadImage()

    pOri = util.cutFaceFromImage(photoOriginal) if pathh.__eq__(pathDatasetFacesImages) else photoOriginal

    util.displayInterfaceWindow(guiMain, photoFromCamera=util.resizeFaceImage(pOri), photoFromDatabase=util.resizeFaceImage(i), percentage=p)
