
import tensorflow as tf
import numpy as np
import src.Util as util
import src.ImageCapture.ImageCaptureFromCamera as imgCamera
import src.ImageCapture.ImageCaptureFromFile as imgFile
import cv2

defaultImage = util.getFileName()
savePath = util.getFileName("DualOrchid.png")

def testImages1(filename=defaultImage):

    print("\nTest Images 1\n")

    # python3.6 image = mpimg.imread(filename)
    image = cv2.imread(filename)
    print("\nShape of image '" + str(defaultImage) + "' file: " + str(image.shape) + "\n")
    #python3.6 plt.imshow(image)
    #python3.6 plt.show()
    cv2.imshow('Image', image)
    cv2.waitKey(0)

def testImages2(filename=defaultImage):

    print("\nTest Images 2\n")

    # python3.6 mpimg.imread(filename)
    image = cv2.imread(filename)
    img = tf.Variable(image, name='img')
    model = tf.global_variables_initializer()

    with tf.Session() as session:
        ### Change axes 0 and 1 of image
        imgToTraspose = tf.transpose(img, perm=[1, 0, 2])
        session.run(model)
        imgTraspose = session.run(imgToTraspose)

    #python3.6 plt.imshow(imgTraspose)
    #python3.6 plt.show()
    cv2.imshow('Image', imgTraspose)
    cv2.waitKey(0)

def testImages3(filename=defaultImage):

    print("\nTest Images 3\n")

    numImages = 2
    images = []
    titles = ["Original Image", "Inverse Image"]

    # python3.6 mpimg.imread(filename)
    image = cv2.imread(filename)
    imageVariable = tf.Variable(image, name='imageVariable')
    model = tf.global_variables_initializer()
    h, w, d = image.shape

    with tf.Session() as session:

        ### There are two ways to inverse an image
        # 1.-
        # imageToInverse = tf.reverse_sequence(imageVariable, [w] * h, 1, batch_dim=0)
        # 2.-
        imageToInverse = tf.reverse_sequence(imageVariable, np.ones((h,)) * w, 1, batch_dim=0)

        session.run(model)
        imageInverse = session.run(imageToInverse)
        imageInverseVariable = tf.Variable(imageInverse, name='imageInverseVariable')
        images.append(image)
        images.append(imageInverse)


    print("\nShape normal image" + str(imageVariable.shape))
    print("Shape inverse image" + str(imageInverseVariable.shape) + "\n")

    ''' Print images separately
    # python3.6
    plt.imshow(image)
    plt.show()
    plt.imshow(imgInverse)
    plt.show()
    '''
    '''
    #python2.7
    cv2.imshow('Image', imgTraspose)
    cv2.waitKey(0)
    '''

    ### Print images together and with titles
    '''python3.6
    window = plt.figure()
    for c, i in enumerate(images):
        subplot = window.add_subplot(1, numImages, c+ 1)
        plt.imshow(i)
        subplot.set_title(titles[c])
    window.set_size_inches(np.array(window.get_size_inches()) * numImages)
    plt.show()
    '''
    util.displayImages(images, titles)

def testImages4(filename=defaultImage):

    print("\nTest Images 4\n")

    numImages = 2
    images = []
    titles = ["Original Image", "Image Rotated 180º"]
    # python3.6 mpimg.imread(filename)
    image = cv2.imread(filename)
    imageVariable = tf.Variable(image, name='imageVariable')
    model = tf.global_variables_initializer()

    #h, w, d = image.shape

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

    print("\nShape normal image" + str(imageVariable.shape))
    print("Shape rotate image" + str(imageRotateVariable.shape) + "\n")
    '''python3.6
    window = plt.figure()
    for c, i in enumerate(images):
        subplot = window.add_subplot(1, numImages, c + 1)
        plt.imshow(i)
        subplot.set_title(titles[c])
    window.set_size_inches(np.array(window.get_size_inches()) * numImages)
    plt.show()
    '''
    util.displayImages(images, titles)

def testImages5(filename=defaultImage):

    print("\nTest Images 5\n")

    numImages = 2
    images = []
    titles = ["Original Image", "Mirror Image"]
    # python3.6 mpimg.imread(filename)
    image = cv2.imread(filename)
    imageVariable = tf.Variable(image, name='imageVariable')
    model = tf.global_variables_initializer()

    h, w, d = image.shape

    with tf.Session() as session:
        imageToInverse = tf.reverse_sequence(imageVariable, [w] * h, 1, batch_dim=0)

        session.run(model)
        imageInverse = session.run(imageToInverse)

        originalImageHalf = tf.slice(imageVariable, [0, 0, 0], [h, int(w / 2), d])
        inverseImageHalf = tf.slice(imageInverse, [0, int(w / 2), 0], [h, int(w / 2), d])

        imageToMirror = tf.concat([originalImageHalf, inverseImageHalf], 1)
        imageMirror = session.run(imageToMirror)

        imageMirrorVariable = tf.Variable(imageMirror, name='imageMirrorVariable')
        images.append(image)
        images.append(imageMirror)

    print("\nShape normal image" + str(imageVariable.shape))
    print("Shape inverse image" + str(imageInverse.shape))
    print("Shape normal half image" + str(originalImageHalf.shape))
    print("Shape inverse half image" + str(inverseImageHalf.shape))
    print("Shape mirror image" + str(imageMirrorVariable.shape) + "\n")
    '''python3.6
    window = plt.figure()
    for c, i in enumerate(images):
        subplot = window.add_subplot(1, numImages, c + 1)
        plt.imshow(i)
        subplot.set_title(titles[c])
    window.set_size_inches(np.array(window.get_size_inches()) * numImages)
    plt.show()
    '''
    util.displayImages(images, titles)
    print("\nSaving image to: " + str(savePath) + "\n")
    #python3.6 mpimg.imsave(savePath, imageMirror)
    cv2.imwrite(savePath, imageMirror);

def testImages6(me, nShots = 2):
    images = []

    iF = imgFile.ImageCaptureFromFileClass(me)
    imgFF = iF.loadImage()

    iC = imgCamera.ImageCaptureFromCameraClass()
    #imgFC = iC.loadImage()

    images.append(imgFF)
    #images.append(imgFC)

    imgFCMul = iC.loadMultipleImages(nShots)
    for i in imgFCMul:
        images.append(i)

    util.displayImages(images, ["Image from File"])#, "Image from Camera"])

def testThreshold(image=defaultImage):
    image = util.loadFileImage(image)
    imageGray = util.imageToGrayscale(image)
    imagenIllumination = util.thresholdImageIllumination(imageGray)
    util.displaySameImageMultipleEffects([image, imageGray, imagenIllumination], ['Original', 'Gray', 'Threshold'])

def testAdjustBrightness(imageToAdjust=defaultImage):
    print("\nTest Adjust Brightness\n")

    images = []
    titles = []

    h, w, d = imageToAdjust.shape
    ph = tf.placeholder(tf.uint8, [h, w, d])

    originalImage = imgFile.loadImage(imageToAdjust)
    images.extend([originalImage])
    titles.extend(["Imágen Original"])

    #normallizeImageOp = tf.image.per_image_standardization(ph)

    adjustImageOp = tf.image.adjust_brightness(ph, 0.25)

    with tf.Session() as session:
        imageAdjusted = session.run(adjustImageOp, feed_dict={ph: imageToAdjust})

    images.extend([imageAdjusted])
    titles.extend(["Imágen con Brillo Ajustado"])

    util.displayImages(images, titles)
