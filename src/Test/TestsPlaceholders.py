
import tensorflow as tf
#import matplotlib.pyplot as plt
from src.ImageCapture.ImageCaptureFromFile import ImageCaptureFromFileClass as imgFile
import src.Util as util
import cv2

defaultImage = util.getImageName("def")
saveSlicedPath = util.getImageName("SlicedOrchid.png")
saveGrayPath = util.getImageName("GrayOrchid.png")

def testPlaceholders1():

    print("\nTest Placeholders 1\n")

    ###We can specify number of elements of the placeholder changing None for a number
    ph = tf.placeholder(dtype=tf.int32)
    op = ph * 2

    with tf.Session() as session:
        print(session.run(op, feed_dict={ph: [1, 2, 3]}))


    ph = tf.placeholder(tf.int32, [None, 3])
    op = ph * 2

    with tf.Session() as session:
        data = [[1, 2, 3],
                  [4, 5, 6]]
        print(session.run(op, feed_dict={ph: data}))


def testPlaceholders2(filename=defaultImage):

    print("\nTest Placeholders 2\n")

    image = imgFile.loadImage(filename)
    h, w, d = image.shape

    #### 2D image with 3 colours
    imagePlaceholder = tf.placeholder("uint8", [None, None, 3])
    #sliceVariable = tf.slice(imagePlaceholder, [1000, 500, 0], [2600, 2600, -1])
    sliceVariable = tf.slice(imagePlaceholder, [int(h/4), int(w/4), 0], [int(h/2), int(w/2), -1])

    with tf.Session() as session:
        sliceImage = session.run(sliceVariable, feed_dict={imagePlaceholder: image})
        print("Original image shape: " + str(image.shape))
        print("Image slice shape: " + str(sliceImage.shape))

    #python3.6 plt.imshow(sliceImage)
    #python3.6  plt.show()
    cv2.imshow(sliceImage)
    cv2.waitKey(0)


def testPlaceholders3(filename=defaultImage):

    print("\nTest Placeholders 3\n")

    image = imgFile.loadImage(filename)
    h, w, d = image.shape

    imagePlaceholder = tf.placeholder("uint8", [h, w, d])
    upLeftCornerVariable = tf.slice(imagePlaceholder, [0, 0, 0], [int(h/2), int(w/2), -1])
    upRightCornerVariable = tf.slice(imagePlaceholder, [0, int(w/2), 0], [int(h/2), int(w/2), -1])
    downLeftCornerVariable = tf.slice(imagePlaceholder, [int(h/2), 0, 0], [int(h/2), int(w/2), -1])
    downRightCornerVariable = tf.slice(imagePlaceholder, [int(h/2), int(w/2), 0], [int(h/2), int(w/2), -1])

    with tf.Session() as session:
        upLeftCorner = session.run(upLeftCornerVariable, feed_dict={imagePlaceholder: image})
        upRightCorner = session.run(upRightCornerVariable, feed_dict={imagePlaceholder: image})
        downLeftCorner = session.run(downLeftCornerVariable, feed_dict={imagePlaceholder: image})
        downRightCorner = session.run(downRightCornerVariable, feed_dict={imagePlaceholder: image})

        upHalf = session.run(tf.concat([upRightCorner, upLeftCorner], 1))
        downHalf = session.run(tf.concat([downRightCorner, downLeftCorner], 1))
        fullCorners = session.run(tf.concat([downHalf, upHalf], 0))
        fullCornersVariable = tf.Variable(fullCorners)

    print("Original image shape: " + str(image.shape))
    print("Up left corner shape: " + str(upLeftCornerVariable.shape))
    print("Up right corner shape: " + str(upRightCornerVariable.shape))
    print("Down left corner shape: " + str(downLeftCornerVariable.shape))
    print("Down right corner shape: " + str(downRightCornerVariable.shape))
    print("Four corners together shape: " + str(fullCornersVariable.shape))

    #python3.6 plt.imshow(fullCorners)
    #python3.6 plt.show()
    cv2.imshow(fullCorners)
    cv2.waitKey(0)

    util.saveImage(fullCorners, saveSlicedPath)


def testPlaceholders4(filename=defaultImage):

    print("\nTest Placeholders 4\n")

    image = imgFile.loadImage(filename)
    h, w, d = image.shape
    images = []
    titles = []

    imageSC1 = image[:, :, 0]
    imageSC2 = image[:, :, 1]
    imageSC3 = image[:, :, 2]
    imageCC = imageSC1 + imageSC2 + imageSC3
    #imagePlaceholder = tf.placeholder(tf.uint8, [h, w, None])
    #imageGrayVariable = tf.image.rgb_to_grayscale(imagePlaceholder)

    #sum = tf.summary.image("imageSummary", image)

    with tf.Session() as session:
        #imageGray = np.asarray(session.run(imageGrayVariable, feed_dict={imagePlaceholder: image})).squeeze()
        #imageRGB = session.run(im, feed_dict={imagePlaceholder2: (image/255)})
        #imageGray2Variable = tf.image.rgb_to_grayscale(imageRGB)
        #imageGray2 = np.asarray(session.run(imageGray2Variable)).squeeze()
        pass

    images.extend((image, imageCC, imageSC1, imageSC2, imageSC3))
    titles.extend(("Original Image", "Image with Colour Change", "Image with Single Colour1", "Image with Single Colour2", "Image with Single Colour3"))

    print("Original image shape: " + str(image.shape))
    print("Color changed image shape: " + str(imageCC.shape))
    #print("Grey image shape: " + str(imageGrayVariable.shape))
    #print("Grey 2 image shape: " + str(imageGray2Variable.shape))
    print("Single colored image 1 shape: " + str(imageSC1.shape))
    print("Single colored image 2 shape: " + str(imageSC2.shape))
    print("Single colored image 3 shape: " + str(imageSC3.shape))

    util.displayImages(images, titles)

    '''
    print("\nSaving image to: " + str(saveGrayPath) + "\n")
    mpimg.imsave(saveGrayPath, imageGray)
    '''