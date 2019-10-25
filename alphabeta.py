from __future__ import absolute_import
from copy import deepcopy
import random
from OthelloLogic import Board
from OthelloGame import OthelloGame
class alphabeta(object):

    def __init__(self):
        self.INF = float('inf')
        self.WEIGHTS = [ 4, -3,  2,  2,  2,  2, -3,  4,
                        -3, -4, -1, -1, -1, -1, -4, -3,
                         2, -1,  1,  0,  0,  1, -1,  2,
                         2, -1,  0,  1,  1,  0, -1,  2,
                         2, -1,  0,  1,  1,  0, -1,  2,
                         2, -1,  1,  0,  0,  1, -1,  2,
                        -3, -4, -1, -1, -1, -1, -4, -3,
                         4, -3,  2,  2,  2,  2, -3,  4]

        self.num_node = 0
        self.dups = 0
        self.nodes = []
        self.branch_fact = [0,0,0]
        self.ply_max = 4
        self.ply_alpha = 4
        self.a_b = False

    def get_move(self, board, color, tr = None, to = None):
        if (self.a_b == False):
            score, fin_move = self.minmax(board, color, tr, to, self.ply_max)
        else:
            score, fin_move = self.alphabeta(board, color, tr, to, self.ply_alpha)
        return fin_move

    def minmax(self, board, color, tr, to, ply_alpha):
        moves = OthelloGame.get_v_moves(board, color)
        if tr < 20:
            return(0, max(moves, key=lambda move: self.greedy(board, color, move)))
        
        if not isinstance(moves, list):
            score = self.hur(board, color)
            return score, None
        return_move = moves[0]
        best_score = -self.INF

        for move in moves:
            newboard= deepcopy(board)
            newboard.executeMove(color, move)
            score = self.min_score(newboard, -color, self.ply_max-1)
            if score > best_score:
                best_score = score
                return_move = move
        
        return (best_score, return_move)
    
    def max_score(self, board, color, ply):
        moves = OthelloGame.get_v_moves(board, color)
        if ply == 0:
            return self.hur(board, color)
        bestscore = -self.INF
        for move in moves:
            newboard = deepcopy(board)
            newboard.executeMove(color, move)
            score = self.min_score(newboard, -color, ply-1)
            if score > bestscore:
                bestscore = score
        return bestscore

    def min_score(self, board, color, ply):
        moves = OthelloGame.get_v_moves(board, color)
        if ply == 0:
            return self.hur(board, color)
        bestscore = self.INF
        for move in moves:
            if move in self.nodes:
                self.dups += 1
            if move not in self.nodes:
                self.nodes.append(move)
            newboard = deepcopy(board)
            newboard.executeMove(color, move)
            score = self.max_score(board, -color, ply-1)
            if score < bestscore:
                bestscore = score
        return bestscore

    def alphabeta(self, board, color, tr, to, ply):
        moves = OthelloGame.get_v_moves(board, color)
        if not isinstance(moves, list):
            score = board.count(color)
            return score, None
        
        return_move = moves[0]
        best_score = self.INF
        if tr < 5:
            return(0, max(moves, key=lambda move: self.greedy(board, color, move)))
        for move in moves:
            newboard = deepcopy(board)
            newboard.executeMove(color, move)
            self.branch_fact[0] += 1
            score = self.min_score_alpha(newboard, -color, ply-1, -self.INF, self.INF)
            if score > best_score:
                best_score = score
                return_move = move
        return (best_score, return_move)

    def max_score_alpha(self, board, color, ply, alpha, beta):
        if ply == 0:
            return self.hur(board, color)
        best_score = -self.INF
        for move in OthelloGame.get_v_moves(board, color):
            newboard = deepcopy(board)
            newboard.executeMove(color, move)
            score = self.min_score_alpha(newboard, -color, ply-1, alpha, beta)
            if score > best_score:
                best_score = score
            if best_score >= beta:
                return best_score
            alpha = max(alpha, best_score)

        return best_score
    
    def min_score_alpha(self, board, color, ply, alpha, beta):
        if ply == 0:
            return self.hur(board, color)
        best_score = self.INF
        for move in OthelloGame.get_v_moves(board, color):
            newboard = deepcopy(board)
            newboard.executeMove(color, move)
            score = self.max_score_alpha(newboard, -color, ply-1, alpha, beta)
            if score < best_score:
                best_score = score
            if best_score <= alpha:
                return best_score
            beta = min(alpha, best_score)

        return best_score

    def hur(self, board, color):
        return 2* self.corn(color, board) + 3*self.cost(board, color)

    def corn(self, color, board):
        tot = 0
        i = 0
        while i < 64:
            if board.pieces[i//8][i%8] == color:
                tot += self.WEIGHTS[i]
            if board.pieces[i//8][i%8] == -color:
                tot -= self.WEIGHTS[i]
            i += 1
        return tot

    def greedy(self, board, color, move):
        newboard = deepcopy(board)
        newboard.executeMove(move, color)
        num_op = len(newboard.get_square(color+-1))
        num_me = len(newboard.get_square(color))
        return num_me-num_op
    
    def cost(self, board, color):
        num_op, num_me = OthelloGame.countNum(board)
        #num_op = board.countDifferences(-color)
        #num_me = board.countDifferences(color)
        return num_me-num_op