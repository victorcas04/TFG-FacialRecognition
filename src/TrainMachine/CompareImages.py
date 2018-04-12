
### https://medium.com/@ageitgey/machine-learning-is-fun-part-4-modern-face-recognition-with-deep-learning-c3cffc121d78
import cv2

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
        recognizer.read(fname)
        gray = self.gray
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        if len(faces) == 0:
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
        cv2.rectangle(self.image1, (x, y), (x + w, y + h), (0, 255, 0), 3)
        ids, conf = recognizer.predict(gray[y:y + h, x:x + w])
        self.percentage = float("{0:.2f}".format(conf))
        #self.percentage = conf
        print("id= " + str(ids) + " coinc= " + str(conf))
        return ids

    def getPercentage(self):
        return self.percentage

    def setPercentage(self, p):
        self.percentage = p

    def getImageCompared(self):
        return self.image2

    def setImageCompared(self, i):
        self.image2 = i