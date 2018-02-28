

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

        sess = tf.Session()
        print(sess.run(hello))
        print(sess.run(a + b))
        sess.close()            #With: 'with tf.Session() as session' there is no need to close session like this

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
            imgToTraspose = tf.transpose(img, perm=[1, 0, 2])       #Change axes 0 and 1 of image
            session.run(model)
            imgTraspose = session.run(imgToTraspose)

        plt.imshow(imgTraspose)
        plt.show()

    def testImages3(self, filename=defaultImage):

        numImages = 2
        images = []
        titles = ["Imágen normal", "Imágen Invertida"]
        image = mpimg.imread(filename)
        imageVariable = tf.Variable(image, name='imageVariable')
        model = tf.global_variables_initializer()
        h, w, d = image.shape

        with tf.Session() as session:
            imageToInverse = tf.reverse_sequence(imageVariable, [w] * h, 1, batch_dim=0)
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
        pass

