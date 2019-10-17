"""
    OthelloZero: main
    Author: Caleb Spradlin
    Date: 27/09/19
    This file contains the main driver for the OthelloZero system, intiializes a board, and a game to run the board
"""

from OthelloGame import OthelloGame as Game
from OthelloLogic import Board
from OthelloIO import get_char_col, split_string

if __name__ == "__main__":
    currentPlayer = 0
    ME = 1
    OPP = -1
    bd = Board()
    g = Game()
    color = g.initColor()
    #g.display(bd)
    print("Valid moves: ", g.get_valid_np_moves(bd, color))
    #g.get_canonical_form(bd, color)
    #print(g.get_np_board(bd))
    #g.get_score(bd, color)
    if color == -1:
        currentPlayer = ME
    else:
        currentPlayer = OPP

    while g.isNotOver is not False:
        if currentPlayer == ME:
            move = g.makeMove(bd, color)
            g.get_score(bd, color)
            if move is not None:
                g.executeMove(bd, color, move)
                currentPlayer = -1*currentPlayer #switch players  
        else:
            move = g.getMove(bd, -color)
            if move is not None:
                g.executeMove(bd, -color, move)
                currentPlayer = -1*currentPlayer #switch players  
        #g.display(bd)
        g.get_canonical_form(bd, currentPlayer)
        g.countNum(bd)
        #currentPlayer = -1*currentPlayer #switch players     
    print("C (Game over)")
    g.countNum(bd)
