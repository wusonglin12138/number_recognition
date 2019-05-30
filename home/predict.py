from PIL import Image, ImageFilter
import tensorflow as tf
import time
import cv2
# 去除加速sse的warning
import os

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'


class Predict:
    checkpoint_dir = "/home/tf/models/"
    pre_time = 0.0

    def __init__(self, img_dir):
        self.img_dir = img_dir

    def img2matrix(self):
        # 导入自己的图片地址
        # in terminal 'mogrify -format png *.jpg' convert jpg to png
        im = Image.open(self.img_dir).convert('L')
        tv = list(im.getdata())  # get pixel values
        # normalize pixels to 0 and 1. 0 is pure white, 1 is pure black.我们写的是白底黑字，标准训练的是黑底白字，需要转换
        tva = [(255 - x) * 1.0 / 255.0 for x in tv]
        return tva

    @staticmethod
    def weight_variable(shape):
        initial = tf.truncated_normal(shape, stddev=0.1)
        return tf.Variable(initial)

    @staticmethod
    def bias_variable(shape):
        initial = tf.constant(0.1, shape=shape)
        return tf.Variable(initial)

    @staticmethod
    def conv2d(x, W):
        return tf.nn.conv2d(x, W, strides=[1, 1, 1, 1], padding='SAME')

    @staticmethod
    def max_pool_2x2(x):
        return tf.nn.max_pool(x, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding='SAME')

    def predict(self):
        result = self.img2matrix()

        # 详细解释见train.py
        x = tf.placeholder(tf.float32, [None, 784])
        W = tf.Variable(tf.zeros([784, 10]))
        b = tf.Variable(tf.zeros([10]))
        W_conv1 = self.weight_variable([5, 5, 1, 32])
        b_conv1 = self.bias_variable([32])
        x_image = tf.reshape(x, [-1, 28, 28, 1])
        h_conv1 = tf.nn.relu(self.conv2d(x_image, W_conv1) + b_conv1)
        h_pool1 = self.max_pool_2x2(h_conv1)

        W_conv2 = self.weight_variable([5, 5, 32, 64])
        b_conv2 = self.bias_variable([64])
        h_conv2 = tf.nn.relu(self.conv2d(h_pool1, W_conv2) + b_conv2)
        h_pool2 = self.max_pool_2x2(h_conv2)

        W_fc1 = self.weight_variable([7 * 7 * 64, 1024])
        b_fc1 = self.bias_variable([1024])
        h_pool2_flat = tf.reshape(h_pool2, [-1, 7 * 7 * 64])
        h_fc1 = tf.nn.relu(tf.matmul(h_pool2_flat, W_fc1) + b_fc1)

        keep_prob = tf.placeholder(tf.float32)
        h_fc1_drop = tf.nn.dropout(h_fc1, keep_prob)

        W_fc2 = self.weight_variable([1024, 10])
        b_fc2 = self.bias_variable([10])

        y_conv = tf.nn.softmax(tf.matmul(h_fc1_drop, W_fc2) + b_fc2)
        init_op = tf.global_variables_initializer()

        saver = tf.train.Saver()
        with tf.Session() as sess:
            start = time.clock()
            sess.run(init_op)
            # 使用之前保存的模型参数
            saver.restore(sess, "/home/tf/models/model.ckpt")
            prediction = tf.argmax(y_conv, 1)
            predint = prediction.eval(feed_dict={x: [result], keep_prob: 1.0}, session=sess)
            result_probability = sess.run(y_conv, feed_dict={x: [result], keep_prob: 1.0})
            # 将预测结果写在predictNumber.txt文件里
            # fi_xu = open('E:/tem/predictNumber.txt', 'w')
            # fi_xu.write(str(predint[0]))
            # fi_xu.close()
            print('recognize result:')
            print(predint[0])
        end = time.clock()

        return predint, result_probability, end - start
