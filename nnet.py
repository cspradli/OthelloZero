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
                    inputs = in_out
                    filters = 256
                    kernel_size = [3,3]
                    padding="same"
                    strides=1
                )

                batch_norm2 = tf.layers.batch_normalization(
                    inputs = conv2
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

        def conv2d(self, x, out_channels, padding):
            return tf.layers.conv2d(x, out_channels, kernel_size=[3,3], padding=self.padding, use_bias=False)
            