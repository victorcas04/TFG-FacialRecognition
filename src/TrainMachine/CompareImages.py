
# encoding: utf-8

### https://medium.com/@ageitgey/machine-learning-is-fun-part-4-modern-face-recognition-with-deep-learning-c3cffc121d78

class CompareImagesClass(object):

    delimiter = '\\'
    #fromExecutable='..'+delimiter
    fromExecutable = ""

    recognizerPath = fromExecutable+'TrainMachine'+delimiter+'recognizer'
    recognizerFile = 'trainedData.yml'

    def __init__(self, xml, reco):
        self.xml = xml
        self.reco = reco

    def compareAll(self, gray):

        fname = self.recognizerPath + self.delimiter + self.recognizerFile
        face_cascade = self.xml
        recognizer = self.reco

        try:
            recognizer.read(fname)
        except:
            print("Red no entrenada. Ejecute de nuevo tras entrenar la red.")
            return -1, 0

        faces = face_cascade.detectMultiScale(gray)

        if len(faces) < 1:
            print("No se han detectado caras...")
            return -1, 0

        # Asumiendo sólo 1 cara por imágen
        x, y, w, h = faces[0]

        id, conf = recognizer.predict(gray[y:y + h, x:x + w])

        conf = 100-conf

        percentage = float("{0:.2f}".format(conf))
        return id, percentage
