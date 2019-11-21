## Neural network for the game
import OthelloGame
import tensorflow as tf
import numpy as np
from utils import *
import os
import shutil
import time
import random
import math
import sys
from config import config
from tensorflow.python.util import deprecation
deprecation._PRINT_DEPRECATION_WARNINGS = False
tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.ERROR)
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

class othellonnet():

    def __init__(self, game):

        self.board_X, self.board_Y = (8, 8)
        self.action_size = (8*8)+1
        self.graph = tf.Graph()
        
        with self.graph.as_default():
            
            self.inputBoard = tf.placeholder(tf.float32, shape=[None, self.board_X, self.board_Y])
            self.dropout = tf.placeholder(tf.float32)
            self.isTraining = tf.placeholder(tf.bool, name="is_training")

            #Layer to be taken as input by the model
            input_layer = tf.reshape(self.inputBoard, -1, [self.board_X, self.board_Y, 1])

            #Initial convolutional bloack
            convolution1 = tf.layers.conv2d(
                inputs = input_layer,
                filters = 256,
                kernel_size = [3, 3],
                padding= "same",
                strides= 1
            )

            batch_norm1 = tf.layers.batch_normalization(
                input = conv1,
                training=self.isTraining)
            relu1 = tf.nn.relu(batch_norm1)
            in_out = relu1

            for i in range(config.resnet_blocks):
                #residual block towers
                conv2 = tf.layers.conv2d(
                    inputs = in_out,
                    filters = 256,
                    kernel_size = [3,3],
                    padding="same",
                    strides=1
                )

                batch_norm2 = tf.layers.batch_normalization(
                    inputs = conv2,
                    training=self.isTraining)
                relu2 = tf.nn.relu(batch_norm2)
                
                conv3 = tf.layers.conv2d(
                    inputs = relu2,
                    filters = 256,
                    kernel_size = [3,3],
                    padding="same",
                    strides=1)
                batch_norm3 = tf.layers.batch_normalization(
                    inputs = conv3,
                    trainable=self.isTraining)
                
                resnet_skip = tf.add(batch_norm3, in_out)
                resnet_in_out = tf.nn.relu(resnet_skip)

        cnn4 = tf.layers.conv2d(
            inputs = resnet_in_out,
            filters= 2,
            kernel_size = [1,1],
            padding="same",
            strides=1)
        batch_norm4 = tf.layers.batch_normalization(
            inputs = cnn4,
            training= self.isTraining)

        relu4 = tf.nn.relu(batch_norm4)
        relu4_flat = tf.reshape(relu4, [-1, self.board_X * self.board_Y * 2])
        
        log = tf.layers.dense(inputs=relu4_flat, units = self.action_size)
        self.pi = tf.nn.softmax(log)

        cnn5 = tf.layers.conv2d(
            inputs = resnet_in_out,
            filters = 1,
            kernel_size = [1,1],
            padding="same",
            strides=1)

        batch_norm5 = tf.layers.batch_normalization(
            inputs = cnn5,
            training= self.isTraining)

        relu5 = tf.nn.relu(batch_norm5)
        relu5_flat = tf.reshape(relu5,[-1, self.action_size])
        dense1 = tf.layers.dense(
            inputs = relu5_flat,
            units = 256)
        relu6 = tf.nn.relu(dense1)
        dense2 = tf.layers.dense(
            inputs = relu6,
            units = 1)


        self.v = tf.nn.tanh(dense2)
        self.train_pis = tf.placeholder(tf.float32, shape=[None, self.action_size])
        self.train_vs = tf.placeholder(tf.float32, shape=[None])
        self.loss_pi = tf.losses.softmax_cross_entropy(self.train_pis, self.train_loss)
        self.loss_v =  tf.losses.mean_squared_error(self.train_vs, tf.reshape(self.v, shape=[-1, ]))
        self.tot_loss = self.loss_v + self.loss_pi

        optimizer = tf.train.MomentumOptimizer(
            learning_rate = config.learning_rate,
            momentum = config.momentum,
            use_nesterov = False)

        self.train_op = optimizer.minimize(self.tot_loss)
        self.saver = tf.train.Saver()
        self.session = tf.Session()
        self.session.run(tf.global_variables_initializer)

class nnet_wrap(object):
    def __init__(self, game):
        self.game = game
        self.net = othellonnet(self.game)
        self.sess = self.net.session

    def predict(self, board):
        board = board[np.newaxis, :, :]
        pi, v = self.sess.run([self.net.pi, self.net.v], feed_dict={self.net.inputBoard: board, self.net.isTraining: False})
        return pi[0], v[0][0]
    
    def train(self, data):
        print("C training network")

        for epoch in range(config.epochs):
            print("C Epoch ", epoch+1)
            example_num = len(data)
            for i in range(0, example_num, config.batch_size):
                board, pis, vs = map(list, zip(*data[i:i + config.batch_size]))
                feed = {self.net.inputBoard: board,
                        self.net.train_pis: pis,
                        self.net.train_vs: vs, 
                        self.net.isTraining: True}
                self.sess.run(self.net.train_op, feed_dict=feed)

                if config.record_loss:
                    if not os.path.exists(config.models_direc):
                        os.mkdir(config.models_direc)
                    file_path = config.models_direc + config.loss_file

                    with open(file_path, 'a') as loss_file:
                        loss_file.write('%f|%f\n' % (pi_loss, v_loss))
        print("\n")

    def save_mod(self, file="current_model"):
        if not os.path.exists(config.models_direc):
            os.mkdir(config.models_direc)

        file_path = config.models_direc + file
        print("C saving model: ", file, "at", file_path)
        self.net.saver.save(self.sess, file_path)

    def load_mod(self, file="current_model"):
        print("Loading model: ", file, "from", config.models_direc)
        self.net.saver.restore(self.sess, file)