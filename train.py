from collections import deque
from MCTS import MCTS
import numpy as np
import time, os, sys
from random import shuffle
from config import config

class train():
    def __init__(self, game, nnet, board):
        self.game = game
        self.nnet = nnet
        self.board = board
        self.onet = self.nnet.__class__(self.game)
        self.mcts = MCTS(self.game, self.nnet)
        self.history = []
        self.skipfirst = False

    def execute_ep(self):
        trainExamples = []
        board = self.board
        self.curPlayer = 1
        ep_step = 0

        while True:
            ep_step += 1
            canonical_board = self.game.get_canonical_form(board, self.curPlayer)
            tempVal = int(ep_step< config.temp_thresh)
            pi = self.mcts.get_probability(canonical_board, temp=tempVal)
            action = np.random.choice(len(pi), p=pi)
            board, self.curPlayer = self.game.get_next_state(board, self.curPlayer, action)

            r = self.game.isNotOver(board, self.curPlayer)

    def learn(self):
        for i in range(1, config.num_iterations+1):
            print('C -- ITER: ' + str(i) + '-- C')
            if not self.skipfirst or i > 1:
                iter_examples = deque([], maxlen=config.max_len_queue)
                
                for eps in range(config.num_episodes):
                    self.mcts = MCTS(self.game, self.nnet)
                    iter_examples += self.execute_ep

                self.history.append(iter_examples)

            if len(self.history) > config.num_iterations :
                print("C len(trainhistory)", len(self.history), "=> remove oldest from history")
                self.history.pop(0)

            self.save_examples(i-1)
            trainExamples = []
            for e in self.history:
                trainExamples.extend(e)
            shuffle(trainExamples)

            self.nnet.save_mod(filename = 'tmp.pth.tar')
            self.onet.load_mod(filename = 'tmp.pth.tar')
            ocmts = MCTS(self.game, self.onet)
            self.nnet.train(trainExamples)
            nmcts = MCTS(self.game, self.nnet)
            
