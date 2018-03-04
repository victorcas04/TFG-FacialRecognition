
import tensorflow as tf
import numpy as np

def testConstants():

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

def testVariables1():

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

def testVariables2():

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

def testVariables3():

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

def testVariables4():

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