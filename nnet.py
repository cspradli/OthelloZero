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

class othellonnet():

    def __init__(self, game, args):
        self.board_X, self.board_Y = game.getBoardSize()
        self.action_size = game.getActionSize()
        self.args = args

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
                training=self.isTraining
            )

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
                    training=self.isTraining
                )
                relu2 = tf.nn.relu(batch_norm2)
                conv3 = tf.layers.conv2d(
                    inputs = relu2,
                    filters = 256,
                    kernel_size = [3,3],
                    padding="same",
                    strides=1
                )
                batch_norm3 = tf.layers.batch_normalization(
                    inputs = conv3,
                    trainable=self.isTraining
                )
                resnet_skip = tf.add(batch_norm3, in_out)
                resnet_in_out = tf.nn.relu(resnet_skip)

        cnn4 = tf.layers.conv2d(
            inputs = resnet_in_out,
            filters= 2,
            kernel_size = [1,1],
            padding="same",
            strides=1
        )
        batch_norm4 = tf.layers.batch_normalization(
            inputs = cnn4,
            training= self.isTraining
        )
        relu4 = tf.nn.relu(batch_norm4)
        relu4_flat = tf.reshape(relu4, [-1, self.board_X * self.board_Y * 2])
        log = tf.layers.dense(inputs=relu4_flat, units = self.action_size)
        self.pi = tf.nn.softmax(log)

        cnn5 = tf.layers.conv2d(
            inputs = resnet_in_out,
            filters = 1,
            kernel_size = [1,1],
            padding="same",
            strides=1
        )

        batch_norm5 = tf.layers.batch_normalization(
            inputs = cnn5,
            training= self.isTraining
        )

        relu5 = tf.nn.relu(batch_norm5)
        relu5_flat = tf.reshape(relu5,[-1, self.action_size])
        dense1 = tf.layers.dense(
            inputs = relu5_flat,
            units = 256
        )
        relu6 = tf.nn.relu(dense1)

        dense2 = tf.layers.dense(
            inputs = relu6,
            units = 1
        )
        self.v = tf.nn.tanh(dense2)

        self.train_pis = tf.placeholder(tf.float32, shape=[None, self.action_size])
        self.train_vs = tf.placeholder(tf.float32, shape=[None])
        self.loss_pi = tf.losses.softmax_cross_entropy(self.train_pis, self.train_loss)
        self.loss_v =  tf.losses.mean_squared_error(self.train_vs, tf.reshape(self.v, shape=[-1, ]))
        self.tot_loss = self.loss_v + self.loss_pi

        optimizer = tf.train.MomentumOptimizer(
            learning_rate = config.learning_rate,
            momentum = config.momentum,
            use_nesterov = False
        )

        self.train_op = optimizer.minimize(self.tot_loss)
        self.saver = tf.train.Saver()
        self.session = tf.Session()
        self.session.run(tf.global_variables_initializer)



            