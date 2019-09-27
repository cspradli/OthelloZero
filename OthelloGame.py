"""
    OthelloZero: OthelloGame
    Author: Caleb Spradlin
    Date: 27/09/19
    This class is the driver of the board, gets and outputs to Logic class, as well as over checking and in/out operations
"""

from __future__ import print_function
from OthelloLogic import Board
from OthelloIO import get_col_char, get_char_col, split_string
import numpy as np

class OthelloGame():

    def __init__(self):
        print("C (Othello initiated)")
    
    def initColor(self):
        """ Init color based on input '| B' or '| W' must output """
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
        """ Gets all valid move given a board and player """
        validMoves = [0]*self.getActionState()
        legal_moves = board.generateMoves(player)
        if len(legal_moves) == 0:
            validMoves[-1]=1
            print("C (No valid moves)")
            return np.array(validMoves)
        return np.array(legal_moves)
    
    def getMove(self, board, color):
        """ Gets a move based on input """
        inp = input()
        iterList = iter(split_string(inp))
        for char in split_string(inp):
            if char == 'C':
                return None
            elif char == 'n':
                print("End game")
            elif char == 'B' or char == 'W':
                self.makeMove(board, color)
            elif char.isalpha() and char.islower():
                x = get_char_col(char)
            elif char.isnumeric():
                y = int(char)-1
        print("C x = ", x, " y = ", y)
        return((x,y))
       

    def makeMove(self, board, color):
        """Generates move and string to output """
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
        """ Executes move based on inputs given """
        board.executeMove(color, move)

    def isOver(self, board, color):
        """ Checks if game is over based on amount of moves each side has """
        if len(board.generateMoves(color)> 0) or len(board.generateMoves(-color)) > 0:
            return False
        else:
            return True

    def countNum(self, board):
        """Counts the number of stones each player has
         Returns both counts """
        countW = 0
        countB = 0
        for y in range(8):
            for x in range(8):
                piece = board.pieces[x][y]
                if piece == -1:
                    countB += 1
                elif piece == 1:
                    countW += 1
        print("C (White count: " + str(countW), ")")
        print("C (Black count: " + str(countB), ")")
        return countW, countB

    def display(self, board):
        """ Display the board """
        print("C (    A  B  C  D  E  F  G  H     )")
        print("C (    ----------------------     )")
        for y in range(7,-1,-1):
            # Print the row number
            print("C (", str(y+1) + ' |', end = ''),
            for x in range(8):
                # Get the piece to print
                piece = board.pieces[x][y]
                if piece == -1: 
                    print(" B ", end = ''),
                elif piece == 1: 
                    print(" W ", end = ''),
                else:
                    print(" . ", end = ''),
            print('| ' + str(y + 1), ")")
        print("C (    ----------------------     )")
        print("C (    A  B  C  D  E  F  G  H     )")
