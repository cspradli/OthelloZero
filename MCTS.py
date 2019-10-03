import numpy as np
import math
import random
EPS_DECAY = 1e-8

class MCTS():

    def __init__(self, game, nnet, args):
        self.game = game
        self.nnet = nnet
        self.args = args

        self.qval = {}
        self.edge_visit = {}
        self.num_visit = {}
        self.policy = {}

        self.terminal = {}
        self.valid_moves = {}

    def get_probability(self, board, temp=1):

        for i in range(self.args.numMCTSRuns):
            self.search(board)

        state = board
        counts = [self.edge_visit[(s, a)] if (s, a) in self.edge_visit else 0 for a in range(self.game.get_action_state())]

        if temp == 0:
            good_action = np.argmax(counts)
            probability = [0]*len(counts)
            probability[good_action] = 1
            return probability
        
        counts = [x**(1./temp) for x in counts]
        probability = [x/float(sum(counts)) for x in counts]

        return probability