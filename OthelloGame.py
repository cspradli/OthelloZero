from __future__ import print_function
from OthelloLogic import Board
from OthelloIO import get_col_char, get_char_col
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
        if inp.startswith('C'):
            return None
        elif len(inp) == 1:
            if inp == 'n':
                print("End game")
            if inp == 'B' or inp == 'W':
                #opponent passes
                self.makeMoves()
        elif len(inp) == 5:
            
            print(get_char_col(inp))

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
            print("C (", str(y) + ' |', end = ''),
            for x in range(8):
                # Get the piece to print
                piece = board.pieces[x][y]
                print("C (", x, y, ")",  end = ''),
                if piece == -1: 
                    print(" B ", end = ''),
                elif piece == 1: 
                    print(" W ", end = ''),
                else:
                    print(" . ", end = ''),
            print('| ' + str(y), ")")
        print("C (    ----------------------     )")
        print("C (    A  B  C  D  E  F  G  H     )")
