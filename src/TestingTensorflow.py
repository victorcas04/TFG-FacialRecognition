

from PIL import Image
import tensorflow as tf
import numpy as np
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import os

class TestClass(object):

    dirPath = "..\sources\\"
    defaultImage = dirPath + "MarshOrchid.jpg"

    '''
    Tutorial from https://www.tensorflow.org/install/install_windows
    '''

    def testConstants(self):

        print("\nTest Constants\n")

        hello = tf.constant('Hello, TensorFlow!')
        a = tf.constant(10)
        b = tf.constant(32)

        ### With: 'with tf.Session() as session' there is no need to use and close session like this
        sess = tf.Session()
        print(sess.run(hello))
        print(sess.run(a + b))
        sess.close()

    '''
    Tutorial from https://learningtensorflow.com/lesson2/
    '''

    def testVariables1(self):

        print("\nTest Variables 1\n")

        ### name parameter not really necessary

        x = tf.constant([35, 40, 45], name='x')
        y = tf.Variable(x + 5, name='y')
        model = tf.global_variables_initializer()

        with tf.Session() as session:
            session.run(model)
            print(session.run(y))

    '''
        Tutorial from https://learningtensorflow.com/lesson2/
    '''

    def testVariables2(self):

        print("\nTest Variables 2\n")

        data = np.random.randint(1000, size=10000)
        x = tf.constant(data, name='x')
        y = tf.Variable((5 * (x**2)) - (3*x) + 15, name = 'y')
        model = tf.global_variables_initializer()

        with tf.Session() as session:
            session.run(model)
            print(session.run(x))
            print(session.run(y))

    '''
        Tutorial from https://learningtensorflow.com/lesson2/
    '''

    def testVariables3(self):

        print("\nTest Variables 3\n")

        x = tf.Variable(0, name='x')
        model = tf.global_variables_initializer()

        with tf.Session() as session:
            session.run(model)
            for i in range(5):
                x = x + 1
                print(session.run(x))

    '''
        Tutorial from https://learningtensorflow.com/lesson2/
    '''

    def testVariables4(self):

        print("\nTest Variables 4\n")

        count = tf.Variable(0, name='count')
        average = tf.Variable(0., name='average')
        randoms = tf.Variable([0, 0, 0, 0, 0], name='randoms')
        model = tf.global_variables_initializer()

        with tf.Session() as session:
            session.run(model)
            for i in range(5):
                newRandom = np.random.randint(1000)
                randoms = randoms + tf.sparse_tensor_to_dense(tf.SparseTensor([[0, i]], [newRandom], [1, 5]))
                average = tf.multiply(average, tf.to_float(count)) + newRandom
                count = count + 1
                average = tf.divide(average, tf.to_float(count))

            print("Randoms: " + str(session.run(randoms)))
            print("Average: " + str(session.run(average)))
            print("Number of randoms: " + str(session.run(count)))

    def testImages1(self, filename=defaultImage):
        image = mpimg.imread(filename)
        print(image.shape)
        plt.imshow(image)
        plt.show()

    def testImages2(self, filename=defaultImage):
        image = mpimg.imread(filename)
        img = tf.Variable(image, name='img')
        model = tf.global_variables_initializer()

        with tf.Session() as session:
            ### Change axes 0 and 1 of image
            imgToTraspose = tf.transpose(img, perm=[1, 0, 2])
            session.run(model)
            imgTraspose = session.run(imgToTraspose)

        plt.imshow(imgTraspose)
        plt.show()

    def testImages3(self, filename=defaultImage):

        numImages = 2
        images = []
        titles = ["Original Image", "Inverse Image"]
        image = mpimg.imread(filename)
        imageVariable = tf.Variable(image, name='imageVariable')
        model = tf.global_variables_initializer()
        h, w, d = image.shape

        with tf.Session() as session:

            ### There are two ways to inverse an image
            # 1.-
            #imageToInverse = tf.reverse_sequence(imageVariable, [w] * h, 1, batch_dim=0)
            # 2.-
            imageToInverse = tf.reverse_sequence(imageVariable, np.ones((h,)) * w, 1, batch_dim=0)

            session.run(model)
            imageInverse = session.run(imageToInverse)
            imageInverseVariable = tf.Variable(imageInverse, name='imageInverseVariable')
            images.append(image)
            images.append(imageInverse)


        print("Shape normal image" + str(imageVariable.shape))
        print("Shape inverse image" + str(imageInverseVariable.shape))

        ''' Print images separately
        plt.imshow(image)
        plt.show()

        plt.imshow(imgInverse)
        plt.show()
        '''

        ### Print images together and with titles

        window = plt.figure()
        for c, i in enumerate(images):
            subplot = window.add_subplot(1, numImages, c+1)
            plt.imshow(i)
            subplot.set_title(titles[c])
        window.set_size_inches(np.array(window.get_size_inches()) * numImages)
        plt.show()

        def testImages4(self, filename=defaultImage):
            numImages = 2
            images = []
            titles = ["Original Image", "Image Rotated 180º"]
            image = mpimg.imread(filename)
            imageVariable = tf.Variable(image, name='imageVariable')
            model = tf.global_variables_initializer()

            h, w, d = image.shape

            with tf.Session() as session:
                ### There are two ways to rotate an image
                # 1.-
                # iTR = tf.reverse_sequence(imageVariable, [w] * h, 1, batch_dim=0)
                # iTR2 = tf.transpose(iTR, perm=[1, 0, 2])
                # iTR3 = tf.reverse_sequence(iTR2, [h] * w, 1, batch_dim=0)
                # imageToRotate = tf.transpose(iTR3, perm=[1, 0, 2])
                # 2.-
                imageToRotate = tf.image.rot90(imageVariable, 2)

                session.run(model)
                imageRotate = session.run(imageToRotate)
                imageRotateVariable = tf.Variable(imageRotate, name='imageRotateVariable')
                images.append(image)
                images.append(imageRotate)

            print("Shape normal image" + str(imageVariable.shape))
            print("Shape rotate image" + str(imageRotateVariable.shape))

            window = plt.figure()
            for c, i in enumerate(images):
                subplot = window.add_subplot(1, numImages, c + 1)
                plt.imshow(i)
                subplot.set_title(titles[c])
            window.set_size_inches(np.array(window.get_size_inches()) * numImages)
            plt.show()

    def testImages5(self, filename=defaultImage):
        numImages = 2
        images = []
        titles = ["Original Image", "Mirror Image"]
        image = mpimg.imread(filename)
        imageVariable = tf.Variable(image, name='imageVariable')
        model = tf.global_variables_initializer()

        h, w, d = image.shape

        with tf.Session() as session:
            imageToInverse = tf.reverse_sequence(imageVariable, [w] * h, 1, batch_dim=0)

            session.run(model)
            imageInverse = session.run(imageToInverse)

            originalImageHalf = tf.slice(imageVariable, [0, 0, 0], [h, int(w/2), d])
            inverseImageHalf = tf.slice(imageInverse, [0, int(w/2), 0], [h, int(w/2), d])

            imageToMirror = tf.concat([originalImageHalf, inverseImageHalf], 1)
            imageMirror = session.run(imageToMirror)

            imageMirrorVariable = tf.Variable(imageMirror, name='imageMirrorVariable')
            images.append(image)
            images.append(imageMirror)

        print("Shape normal image" + str(imageVariable.shape))
        print("Shape inverse image" + str(imageInverse.shape))
        print("Shape normal half image" + str(originalImageHalf.shape))
        print("Shape inverse half image" + str(inverseImageHalf.shape))
        print("Shape mirror image" + str(imageMirrorVariable.shape))

        window = plt.figure()
        for c, i in enumerate(images):
            subplot = window.add_subplot(1, numImages, c + 1)
            plt.imshow(i)
            subplot.set_title(titles[c])
        window.set_size_inches(np.array(window.get_size_inches()) * numImages)
        plt.show()