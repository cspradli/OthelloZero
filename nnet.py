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
            