"""
    OthelloZero: OthelloGame
    Author: Caleb Spradlin
    Date: 27/09/19
    This class is the driver of the board, gets and outputs to Logic class, as well as over checking and in/out operations
"""
from OthelloLogic import Board
from OthelloIO import get_col_char, get_char_col, split_string
import random
import numpy as np
import copy

class OthelloGame():

    def __init__(self):
        print("C (Othello initiated)")
        self.current_player = -1
        self.game_time = 300.00
        self.time = {-1: self.game_time, 1: self.game_time}
    
    def get_move(self, board, engine, color, time):
        """ Get the move for the given engine and color. Check validity of the 
        move."""
        legal_moves = board.generateMoves(color)
        if not legal_moves:
            return None
        elif len(legal_moves) == 1:
            return legal_moves[0]
        else:
            move = engine.get_move(copy.deepcopy(board), color, time[color], time[-color])

            if move not in legal_moves:
                raise LookupError(color)

            return move

    def input_move(self, board, color):
        """ Gets a move based on input """
        inp = input('')
        i = 0
        for char in split_string(inp):
            if char == 'C':
                return None
            elif char == 'n':
                print("C End game")
            elif (char == 'B' and len(inp) == 1) or (char == 'W' and len(inp)==1):
                self.makeMove(board, color)
            elif char.isalpha() and char.islower():
                x = get_char_col(char)
            elif char.isnumeric():
                y = int(char)-1
            i = i + 1
        return((x,y))
       

    def makeMove(self, board, color, engine, time):
        """Generates move and string to output """
        listMoves = list()
        out = []
        outMove = []
        if color == 1:
            out.append('W')
        if color == -1:
            out.append('B')
        validMoves = board.generateMoves(color)
        if len(validMoves) <= 0:
            print(''.join(out))
            return None
        if len(validMoves) > 0:
            print("C Moves to choose")
            for move in validMoves:
                x,y = move
                print("C ", color, end=' ')
                print(get_col_char(x), end=' ')
                print(str(y + 1))
            move = self.get_move(board, engine, color, time)
            x,y = move
            out.append(' ')
            out.append(get_col_char(x))
            out.append(' ')
            out.append(str(y + 1))
            print(''.join(out))
            return move
    


    ### -------    HELPER FUNCTIONS -------   ####
    def initColor(self):
        """ Init color based on input '| B' or '| W' must output """
        inp = input('')
        if inp == 'I B':
            gameColor = -1
            print("R B")
        else:
            gameColor = 1
            print("R W")
        return gameColor

    def get_score(self, board, player):
        """ Counts difference from board class """
        print("C (Difference: ", board.countDifference(player), ")")
        return board.countDifference(player)

    def get_v_moves(board, color):
        list_move = board.generateMoves(color)
        return list_move

    def executeMove(self, board, color, move):
        """ Executes move based on inputs given """
        board.executeMove(color, move)

    def isNotOver(self, board, color):
        """ Checks if game is over based on amount of moves each side has """
        if (board.generateMoves(color) is not None) and (board.generateMoves(-color) is not None):
            # Game has not ended
            return True
        else:
            return False

    def countNum(self, board):
        """Counts the number of stones each player has
         Returns both counts """
        countW = 0
        countB = 0
        for y in range(8):
            for x in range(8):
                piece = board[x][y]
                if piece == -1:
                    countB += 1
                elif piece == 1:
                    countW += 1
        print("C (White count: " + str(countW), ")")
        print("C (Black count: " + str(countB), ")")
        return countW, countB

    def display(self, board):
        """ Display the board """
        print("C (     A  B  C  D  E  F  G  H     )")
        print("C (    ------------------------     )")
        for y in range(7,-1,-1):
            # Print the row number
            print("C (", str(y+1) + ' |', end = ''),
            for x in range(8):
                # Get the piece to print
                piece = board[x][y]
                if piece == -1: 
                    print(" B ", end = ''),
                elif piece == 1: 
                    print(" W ", end = ''),
                else:
                    print(" . ", end = ''),
            print('| ' + str(y + 1), ")")
        print("C (    ------------------------     )")
        print("C (     A  B  C  D  E  F  G  H      )")
