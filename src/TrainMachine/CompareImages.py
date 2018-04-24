
### https://medium.com/@ageitgey/machine-learning-is-fun-part-4-modern-face-recognition-with-deep-learning-c3cffc121d78
import cv2, os

class CompareImagesClass(object):

    image2 = None
    percentage = 0

    def __init__(self, image, xml, reco, gray):
        self.image1 = image
        self.xml = xml
        self.reco = reco
        self.gray = gray

    def compareSingle(self, image):
        # Do things
        # self.setPercentage(...)
        pass

    def compareAll(self):
        # for Image i in database:
        #   p = compareSingle(i)
        #   if p > self.getPercentage:
        #       self.setPercentage(p)
        #       self.setImageCompared(i)

        fname = "./TrainMachine/recognizer/trainedData.yml"
        face_cascade = self.xml
        recognizer = self.reco
        try:
            recognizer.read(fname)
        except:
            print("Red no entrenada. Ejecute de nuevo tras entrenar la red.")
            return -1
        gray = self.gray
        #faces = face_cascade.detectMultiScale(gray, 1.2, 5)
        faces = face_cascade.detectMultiScale(gray)

        if len(faces) < 1:
            print("No se han detectado caras...")
            return -1
        '''
        for (x, y, w, h) in faces:
            cv2.rectangle(self.image1, (x, y), (x + w, y + h), (0, 255, 0), 3)
            # print("waiting...........")
            # cv2.waitKey(0)
            ids, conf = recognizer.predict(gray[y:y + h, x:x + w])
        '''

        # Asumiendo sólo 1 cara
        x, y, w, h = faces[0]
        #cv2.rectangle(self.image1, (x, y), (x + w, y + h), (0, 255, 0), 3)

        id, conf = recognizer.predict(gray[y:y + h, x:x + w])

        #conf = 100 - conf

        self.percentage = float("{0:.2f}".format(conf))
        #self.percentage = conf
        print("id= " + str(id) + " coinc= " + str(conf))
        return id

    def compareAll2(self):
        path = "./TrainMachine/recognizerPerImage/"
        face_cascade = self.xml
        #recognizer = self.reco
        gray = self.gray
        maxConf = 0
        maxID = None
        for i in os.listdir(path):
            recognizer = self.reco
            fname = path + i
            print(fname)
            #'./ TrainMachine / recognizerPerImage / trainedData_' + label + '.yml'
            recognizer.read(fname)

            faces = face_cascade.detectMultiScale(gray)

            if len(faces) < 1:
                print("No se han detectado caras...")
                return -1

            x, y, w, h = faces[0]

            id, conf = recognizer.predict(gray[y:y + h, x:x + w])
            print("id: " + str(id) + " ;conf: " + str(conf))
            if conf > maxConf:
                maxConf = conf
                maxID = id
            self.percentage = float("{0:.2f}".format(maxConf))

        return maxID


    def getPercentage(self):
        return self.percentage

    def setPercentage(self, p):
        self.percentage = p

    def getImageCompared(self):
        return self.image2

    def setImageCompared(self, i):
        self.image2 = i