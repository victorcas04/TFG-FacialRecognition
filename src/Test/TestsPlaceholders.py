
import tensorflow as tf
import matplotlib.image as mpimg
import matplotlib.pyplot as plt

dirPath = "..\sources\\"
nameImage = "default.png"
defaultImage = dirPath + nameImage
nameImageSave = "SlicedOrchid.png"
savePath = dirPath + nameImageSave

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

    image = mpimg.imread(filename)
    h, w, d = image.shape

    #### 2D image with 3 colours
    imagePlaceholder = tf.placeholder("uint8", [None, None, 3])
    #sliceVariable = tf.slice(imagePlaceholder, [1000, 500, 0], [2600, 2600, -1])
    sliceVariable = tf.slice(imagePlaceholder, [int(h/4), int(w/4), 0], [int(h/2), int(w/2), -1])

    with tf.Session() as session:
        sliceImage = session.run(sliceVariable, feed_dict={imagePlaceholder: image})
        print("Original image shape: " + str(image.shape))
        print("Image slice shape: " + str(sliceImage.shape))

    plt.imshow(sliceImage)
    plt.show()


def testPlaceholders3(filename=defaultImage):

    print("\nTest Placeholders 3\n")

    image = mpimg.imread(filename)
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

    plt.imshow(fullCorners)
    plt.show()

    print("\nSaving image to: " + str(savePath) + "\n")
    mpimg.imsave(savePath, fullCorners)


def testPlaceholders4(filename=defaultImage):
    print("\nTest Placeholders 4\n")
    pass
