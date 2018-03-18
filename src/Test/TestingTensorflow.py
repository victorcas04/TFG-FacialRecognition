

import src.Test.TestsImages as tstImages
import src.Test.TestsPlaceholders as tstPlaceholders
import src.Test.TestsVariables as tstVariables
import src.Util as util

class TestClass(object):

    orchid = util.getImageName("MarshOrchid.jpg")
    me = util.getImageName("FOTO_DNI_1.jpg")
    default = util.getImageName()

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
        tstImages.testImages1(self.default)
        tstImages.testImages2(self.default)
        tstImages.testImages3(self.default)
        tstImages.testImages4(self.default)
        tstImages.testImages5(self.default)
        tstImages.testImages6(self.me, nShots=4)

    def testPlaceholders(self):
        tstPlaceholders.testPlaceholders1()
        tstPlaceholders.testPlaceholders2(self.default)
        tstPlaceholders.testPlaceholders3(self.default)
        tstPlaceholders.testPlaceholders4(self.default)

    def testActual(self):
        print("\nTest Actual\n")

        pass

