from __future__ import print_function
from OthelloLogic import Board
from OthelloIO import get_col_char
import numpy as np

class OthelloGame():

    def __init__(self):
        print("(Othello initiated)")
    
    def initColor(self):
        inp = input()
        if inp == '| B':
            gameColor = -1
            print("R B")
        else:
            gameColor = 1
            print("R W")
        return gameColor

    def getActionState(self):
        return ((8*8)+1)
    
    def getValidMoves(self, board, player):
        validMoves = [0]*self.getActionState()
        legal_moves = board.generateMoves(player)
        if len(legal_moves) == 0:
            validMoves[-1]=1
            print("(No valid moves)")
            return np.array(validMoves)
        return legal_moves
        
    def makeMove(self, board, color):
        out = []
        if color == 1:
            out.append('W ')
        if color == -1:
            out.append('B ')
        validMoves = board.generateMoves(color)
        if len(validMoves) < 0:
            print(''.join(out))
            return None
        if len(validMoves) > 0:
            move = validMoves.pop()
            x,y = move
            out.append(get_col_char(x))
            out.append(' ')
            out.append(str(y + 1))
            print(''.join(out))
            return move

    def executeMove(self, board, color, move):
        board.executeMove(color, move)

    def isOver(self, board, color):
        if len(board.generateMoves(color)> 0) or len(board.generateMoves(-color)) > 0:
            return False
        else:
            return True

    def countNum(self, board):
        # Counts the number of stones each player has
        # Returns both counts
        countW = 0
        countB = 0
        for y in range(8):
            for x in range(8):
                piece = board.pieces[x][y]
                if piece == -1:
                    countB += 1
                elif piece == 1:
                    countW += 1
        print("(White count: " + str(countW), ")")
        print("(Black count: " + str(countB), ")")
        return countW, countB

    def display(self, board):
        # Display the board #
        print("(    A  B  C  D  E  F  G  H     )")
        print("(    ----------------------     )")
        for y in range(7,-1,-1):
            # Print the row number
            print("(", str(y) + ' |', end = ''),
            for x in range(8):
                # Get the piece to print
                piece = board.pieces[x][y]
                print("(", x, y, ")",  end = ''),
                if piece == -1: 
                    print(" B ", end = ''),
                elif piece == 1: 
                    print(" W ", end = ''),
                else:
                    print(" . ", end = ''),
            print('| ' + str(y), ")")
        print("(    ----------------------     )")
        print("(    A  B  C  D  E  F  G  H     )")
