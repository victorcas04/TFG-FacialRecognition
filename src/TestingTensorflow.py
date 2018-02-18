
import tensorflow as tf

sess = tf.Session()

hello = tf.constant('Hello, TensorFlow!')
a = tf.constant(10)
b = tf.constant(32)

print()
print(sess.run(hello))
print(sess.run(a + b))

sess.close()