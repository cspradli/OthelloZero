from __future__ import absolute_import
from copy import deepcopy
import random
from OthelloLogic import Board
from OthelloGame import OthelloGame

class alphabeta(object):

    def __init__(self):
        self.INF = float('inf')
        self.WEIGHTS = [4, -3, 2, 2, 2, 2, -3, 4,
               -3, -4, -1, -1, -1, -1, -4, -3,
               2, -1, 1, 0, 0, 1, -1, 2,
               2, -1, 0, 1, 1, 0, -1, 2,
               2, -1, 0, 1, 1, 0, -1, 2,
               2, -1, 1, 0, 0, 1, -1, 2,
               -3, -4, -1, -1, -1, -1, -4, -3,
               4, -3, 2, 2, 2, 2, -3, 4]

        self.num_node = 0
        self.dups = 0
        self.nodes = []
        self.branch_fact = [0,0,0]
        self.ply_max = 4
        self.ply_alpha = 4
        self.a_b = False

    def get_move(self, board, color, move_n = None, tr = None, to = None):
        if (self.a_b == False):
            score, fin_move = self.minmax(board, color, move_n, tr, to, self.ply_max)
        else:
            score, fin_move = self.alphabeta(board, color, move_n, tr, to, self.ply_alpha)
        return fin_move

    def minmax(self, board, color, move_n, tr, to, ply_alpha):
        moves = game.get_v_moves(board, color)
        if move_n > 7 and move_n < 15:
            self.ply_max = 2
        if tr < 20:
            return(0, max(moves, key=lambda move: self.greedy(board, color, move)))
        
        if not isinstance(moves, list):
            score = self.hur(board, color)
            return score, None
        return_move = moves[0]
        best_score = -self.INF

        for move in moves:
            newboard= deepcopy(board)
            newboard.execute_move(color, move)
            score = self.min_score(newboard, -color, move_n, self.ply_max-1)
            if score > best_score:
                best_score = score
                return_move = move
        
        return (best_score, return_move)
