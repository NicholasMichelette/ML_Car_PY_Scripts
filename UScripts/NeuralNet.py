import tensorflow as tf
from tensorflow import keras
import numpy as np

class car_nn:

    def __init__(self):
        with tf.device('/cpu:0'):
            model = tf.keras.models.Sequential()
            model.add(tf.keras.layers.Dense(6, input_shape=(6,))) # input layer
            model.add(tf.keras.layers.Activation('relu'))
            model.add(tf.keras.layers.Dense(6, input_shape=(6,)))
            model.add(tf.keras.layers.Activation('relu'))
            model.add(tf.keras.layers.Dense(6, input_shape=(6,)))
            model.add(tf.keras.layers.Activation('relu'))
            model.add(tf.keras.layers.Dense(3, input_shape=(6,))) # output layer
            model.add(tf.keras.layers.Activation('sigmoid'))
            model.compile(loss = 'mse', optimizer = 'adam')

            self.model = model


    def predict(self, d1, d2, d3, d4, d5, speed):
        input = np.asarray([d1, d2, d3, d4, d5, speed])
        input = np.atleast_2d(input)
        with tf.device('/cpu:0'):
            return self.model.predict(input, 1)