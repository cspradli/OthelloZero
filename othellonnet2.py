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
        self.loss_pi = tf.losses.softmax_cross_entropy(self.target_pis, self.pi)
        self.loss_vi = tf.losses.mean_squared_error(self.target_vs, tf.reshape(self.v, shape[-1,]))
        self.total_loss = self.loss_pi + self.loss_vi
        update = tf.get_collection(tf.GraphKeys.UPDATE_OPS)
        with tf.control_dependencies(update):
            self.train_step = tf.train.AdamOptimizer(self.config.lr).minimize(self.total_loss)

def residual_tower():
    def __init__(self, game):
        self.board_X, self.board_Y = game.get_board_size()
        self.action_size = game.get_action_size()
        self.graph = tf.Graph()
        with self.graph.as_default():
            self.board = tf.placeholder(tf.float32, shape=[None, self.board_X, self.board_Y])
            self.drop = tf.placeholder(tf.float32)
            self.isTraining = tf.placeholder(tf.bool, name="is_training")

            x_im = tf.reshape(self.input_board, [-1, self.board_X, self.board_Y, 1])
            x_im = tf.layers.conv2d(x_im, config.num_channels, kernel_size = (3,3), strides=(1,1), name='conv', padding='same', use_bias=False)
            x_im = tf.layers.batch_normalization(x_im, axis=1, name='conv_bn', training=self.isTraining)
            x_im = tf.nn.relu(x_im)

            res_tow = self.residual_block(inputLayer = x_im, kernel_size = 3, filters=config.num_channels, stage=1, block='a')
            res_tow = self.residual_block(inputLayer = res_tow, kernel_size = 3, filters=config.num_channels, stage=1, block='b')
            res_tow = self.residual_block(inputLayer = res_tow, kernel_size = 3, filters=config.num_channels, stage=1, block='c')
            res_tow = self.residual_block(inputLayer = res_tow, kernel_size = 3, filters=config.num_channels, stage=1, block='d')
            res_tow = self.residual_block(inputLayer = res_tow, kernel_size = 3, filters=config.num_channels, stage=1, block='e')
            res_tow = self.residual_block(inputLayer = res_tow, kernel_size = 3, filters=config.num_channels, stage=1, block='f')
            res_tow = self.residual_block(inputLayer = res_tow, kernel_size = 3, filters=config.num_channels, stage=1, block='g')
            res_tow = self.residual_block(inputLayer = res_tow, kernel_size = 3, filters=config.num_channels, stage=1, block='h')
            res_tow = self.residual_block(inputLayer = res_tow, kernel_size = 3, filters=config.num_channels, stage=1, block='i')
            res_tow = self.residual_block(inputLayer = res_tow, kernel_size = 3, filters=config.num_channels, stage=1, block='j')
            res_tow = self.residual_block(inputLayer = res_tow, kernel_size = 3, filters=config.num_channels, stage=1, block='k')
            res_tow = self.residual_block(inputLayer = res_tow, kernel_size = 3, filters=config.num_channels, stage=1, block='l')
            res_tow = self.residual_block(inputLayer = res_tow, kernel_size = 3, filters=config.num_channels, stage=1, block='m')
            res_tow = self.residual_block(inputLayer = res_tow, kernel_size = 3, filters=config.num_channels, stage=1, block='n')
            res_tow = self.residual_block(inputLayer = res_tow, kernel_size = 3, filters=config.num_channels, stage=1, block='o')
            res_tow = self.residual_block(inputLayer = res_tow, kernel_size = 3, filters=config.num_channels, stage=1, block='p')
            res_tow = self.residual_block(inputLayer = res_tow, kernel_size = 3, filters=config.num_channels, stage=1, block='q')
            res_tow = self.residual_block(inputLayer = res_tow, kernel_size = 3, filters=config.num_channels, stage=1, block='r')
            res_tow = self.residual_block(inputLayer = res_tow, kernel_size = 3, filters=config.num_channels, stage=1, block='s')
            res_tow = self.residual_block(inputLayer = res_tow, kernel_size = 3, filters=config.num_channels, stage=1, block='t')
            res_tow = self.residual_block(inputLayer = res_tow, kernel_size = 3, filters=config.num_channels, stage=1, block='u')

            pol =tf.layers.conv2d(res_tow, 2, kernel_size = (1,1), strides=(1,1), name='pi', padding='same', use_bias=False)
            pol = tf.layers.batch_normalization(pol, axis=3, name='bn', training=self.isTraining)
            