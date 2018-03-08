
import src.Test.TestsVariables as tstVariables
import src.Test.TestsImages as tstImages
import src.Test.TestsPlaceholders as tstPlaceholders
import src.Util as util

class TestClass(object):

    orchid = "MarshOrchid.jpg"
    me = "FOTO_DNI_1.jpg"
    defaultImage = util.getImageName(orchid)

    '''
    Tutorials from https://www.tensorflow.org and https://learningtensorflow.com/
    
    '''

    def testVariables(self):
        tstVariables.testConstants()
        tstVariables.testVariables1()
        tstVariables.testVariables2()
        tstVariables.testVariables3()
        tstVariables.testVariables4()

    def testImages(self):
        tstImages.testImages1(self.defaultImage)
        tstImages.testImages2(self.defaultImage)
        tstImages.testImages3(self.defaultImage)
        tstImages.testImages4(self.defaultImage)
        tstImages.testImages5(self.defaultImage)

    def testPlaceholders(self):
        tstPlaceholders.testPlaceholders1()
        tstPlaceholders.testPlaceholders2(self.defaultImage)
        tstPlaceholders.testPlaceholders3(self.defaultImage)
        tstPlaceholders.testPlaceholders4(self.defaultImage)

    def testActual(self):
        print("\nTest Actual\n")

        images = []
        titles = []

        originalImage = util.loadImage(self.defaultImage)

        images.extend([originalImage])
        titles.extend(["Imágen Original"])

        normalizedImage = self.testNormalizeIllumination(originalImage)

        images.extend([normalizedImage, normalizedImage, normalizedImage, normalizedImage])
        titles.extend(["Imágen Normalizada"])

        util.displayImages(images, titles)

    def testNormalizeIllumination(self, imageToNormallize=defaultImage):
        print("\nTest Normalize Illumination\n")
        return imageToNormallize





