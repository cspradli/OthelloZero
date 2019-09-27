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
    g.display(bd)
    #move = g.getMove(bd, color)
    #g.executeMove(bd, -color, move)
    #g.display(bd)
    if color == -1:
        currentPlayer = ME
    else:
        currentPlayer = OPP

    while g.isNotOver is not False:
        if currentPlayer == ME:
            move = g.makeMove(bd, color)
            if move is not None:
                g.executeMove(bd, color, move)
        else:
            move = g.getMove(bd, -color)
            if move is not None:
                g.executeMove(bd, -color, move)
        g.display(bd)
        g.countNum(bd)
        currentPlayer = -1*currentPlayer #switch players     
    print("C (Game over)")
    g.countNum(bd)
