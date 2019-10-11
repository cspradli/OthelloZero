## Neural network for the game
import OthelloGame
import sys
import tensorflow as tf
import numpy as np
from utils import *
from config import config

class othellonnet():

    def __init__(self, game, args):

        self.board_X, self.board_Y = game.getBoardSize()
        self.action_size = game.getActionSize()
        self.args = args


        relu = tf.nn.relu
        tanh = tf.nn.tanh
        batch_norm = tf.layers.batch_normalization
        drop = tf.layers.dropout
        dense = tf.layers.dense
        
        self.graph = tf.Graph()
        
        with self.graph.as_default():
            self.input = tf.placeholder(tf.float32, shape= [None, self.board_X, self.board_Y])
            self.dropout = tf.placeholder(tf.float32)
            self.isTraining = tf.placeholder(tf.bool, name="isTraining")

            x_image = tf.reshape(self.input, [-1, self.board_X, self.board_Y, 1])
            conv1 = relu(batch_norm(self.conv2d(x_image, config.num_channels, 'same'), axis=3, trainable=self.isTraining))
            conv2 = relu(batch_norm(self.conv2d(conv1, config.num_channels, 'same'), axis=3, training=self.isTraining))
            conv3 = relu(batch_norm(self.conv2d(conv2, config.num_channels, 'valid'), axis=3, training=self.isTraining))
            conv4 = relu(batch_norm(self.conv2d(conv3, config.num_channels, 'valid'), axis=3, training=self.isTraining))
            conv4_ft = tf.reshape(conv4, [-1, config.num_channels*(self.board_X-4)*(self.board_Y-4)])
            fc1 = drop(relu(batch_norm(dense(conv4_ft, 1024, use_bias=False), axis=1, training=self.isTraining)), rate=self.dropout)
            fc2 = drop(relu(batch_norm(dense(fc1, 512, use_bias=False), axis=1, training=self.isTraining)), rate=self.dropout)
            self.pi = dense(fc2, self.action_size)
            self.prob = tf.nn.softmax(self.pi)
            self.v = tanh(dense(fc2, 1))

            self.calc_loss()

    def conv2d(self, x, out_channels, padding):
        return tf.layers.conv2d(x, out_channels, kernel_size=[3, 3], padding=padding, use_bias=False)
    
    def calc_loss(self):
        self.target_pis = tf.placeholder(tf.float32, shape=[None, self.action_size])
        self.target_vs = tf.placeholder(tf.float32, shape=[None])