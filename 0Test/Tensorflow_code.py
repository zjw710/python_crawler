__author__ = 'Administrator'
#coding=utf-8
import tensorflow as tf
sess = tf.Session()
a = tf.constant(10)
b= tf.constant(12)
sess.run(a+b)