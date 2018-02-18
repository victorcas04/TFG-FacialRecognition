
import tensorflow as tf

hello = tf.constant('Hello, TensorFlow!')
sess = tf.Session()
sess.run(hello)
###tf.Print()
print(str(hello))

a = tf.constant(10)
b = tf.constant(32)
sess.run(a + b)

sess.close()