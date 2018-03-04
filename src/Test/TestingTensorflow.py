
import src.Test.TestsVariables as tstVariables
import src.Test.TestsImages as tstImages
import src.Test.TestsPlaceholders as tstPlaceholders

class TestClass(object):

    dirPath = "..\sources\\"
    nameImage = "MarshOrchid.jpg"
    defaultImage = dirPath + nameImage

    '''
    Tutorials from https://www.tensorflow.org and 
    
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
