import os
import shutil
import time
import random
import math
import sys
from utils import *
import numpy as np
import tensorflow as tf
from othellonnet import othellonnet as onnet
from config import config

class nnet(object):

    def __init__(self, game):
        self.game = game
        self.nnet = onnet(game, args)
        self.sess = self.nnet.session

    def predict(self, board):
        state = board[np.newaxis, :, :]
        pi, v = self.sess.run({self.nnet.pi, self.nnet.v], feed_dict={self.nnet.states: state, self.nnet.isTraining = "False"})
        self.board_x, self.board_y = game.get_board_size()
        self.action_size = self.get_action_size()
        self.sess =  tf.Session(graph=self.nnet.graph)
        self.saver = None
        with tf.Session() as temp_sess:
            temp_sess.run(tf.global_variables_initializer)
        self.sess.run(tf.variables_initializer(self.nnet.graph.get_collection('variables')))

    def train(self, examples):
        for epoch in config.epochs:
            print("C Epoch ", str(epoch+1))
            data_time = AverageMeter()