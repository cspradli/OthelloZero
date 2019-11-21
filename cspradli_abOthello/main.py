"""
    OthelloZero: main
    Author: Caleb Spradlin
    Date: 25/10/19
    This file contains the main driver for the OthelloZero system, intiializes a board, and a game to run the board
"""
import argparse, copy, signal, sys, timeit, imp
from OthelloGame import OthelloGame as Game
from OthelloLogic import Board
from OthelloIO import get_char_col, split_string
from alphabeta import alphabeta
if __name__ == "__main__":

    ab = alphabeta()
    currentPlayer = 0
    ME = 1
    OPP = -1
    bd = Board()
    g = Game()
    color = g.initColor()
    g.display(bd)
    game_time = 300.0
    time = {-1: game_time, 1: game_time}

    if color == -1:
        currentPlayer = ME
    else:
        currentPlayer = OPP

    while g.isNotOver is not False:
        if currentPlayer == ME:
            start_time = timeit.default_timer()
            move = g.makeMove(bd, color, ab, time)
            end_time = timeit.default_timer()
            time[color] -= round(end_time - start_time, 1)
            g.get_score(bd, color)
            if move is not None:
                g.executeMove(bd, color, move)
                currentPlayer = -1*currentPlayer #switch players  
                #g.display(bd)
        else:
            start_time = timeit.default_timer()
            move = g.makeMove(bd, -color, ab, time)
            end_time  = timeit.default_timer()
            time[-color] -= round(end_time - start_time, 1)
            g.get_score(bd, -color)

            #move = g.input_move(bd, -color)
            if move is not None:
                g.executeMove(bd, -color, move)
                currentPlayer = -1*currentPlayer #switch players  
                #g.display(bd)
        g.display(bd)
        g.countNum(bd)
        input('Enter to continue')
    print("C (Game over)")
    g.countNum(bd)
