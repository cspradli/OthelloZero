import numpy as np
import math
import random
from config import config
from OthelloGame import OthelloGame
EPS_DECAY = 1e-8

class MCTS():

    def __init__(self, game, nnet, args):

        self.game = game        #Game with board and functions
        self.nnet = nnet        #Neural net to use
        self.args = args        #Args (legacy to config file)

        self.qval = {}          #Stores Q value for state, action
        self.edge_visit = {}    #Stores the # o/times edge s,a was visited
        self.num_visit = {}     #Stores # o/times board s was visited
        self.policy = {}        #Stores initial policy(returned by nnet)

        self.terminal = {}      #Stores terminal state
        self.valid_moves = {}   #Stores get_valid_moves for board s

    def get_probability(self, board, temp=1):

        """ This function takes a board and runs MCTS sims starting from canonical board

            Returns: probability vector """

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

    def run_mcts(self, board):

        """ This func performs ONE interation of the MCTS, recursively called until leaf is found. NNET returns a policy vector based on the input leaf node 
            
            Returns: v=the negative val of the the current canon board """

        state = self.game.get_canonical_form(board)

        if state not in self.terminal:
            self.terminal[state] = self.game.has_ended(board, 1)
        if self.terminal[state] != 0:
            return -self.terminal[state]
        
        if state not in self.policy:
            self.policy[state], v = self.nnet.predict(board)
            valids = self.game.get_valid_moves(board, game.current_player)
            self.policy[state] = self.policy[state] * valids
            sum_policy_state = np.sum(self.policy[state])
            if sum_policy_state > 0:
                self.policy[state] /= sum_policy_state
            else:
                print("C All valid moves were masked, do workaround")
                self.policy[state] = self.policy[state] + valids
                self.policy[state] /= np.sum(self.policy[state])
            self.valid_moves = valids
            self.edge_visit = 0
            return -v
        
        valids = self.valid_moves[state]
        current_best = -float('inf')
        best_action = -1

        for a in range(self.game.get_action_size()):
            if valids[a]:
                if (s,a) in self.qval:
                    u = self.qval[(s,a)] + self.config.cpuct*self.policy[state][a]*math.sqrt(self.num_visit[state]/(1+self.edge_visit[(s,a)]))
                else:
                    u = self.config.cpuct*self.policy[state][a]*math.sqrt(self.num_visit[state] + EPS_DECAY)

                if u > current_best:
                    current_best = u
                    best_action = a
                
        a = best_action
        next_s, next_player = self.game.get_next_state(self.game.get_canonical_form(), )

                    