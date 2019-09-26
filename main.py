from OthelloGame import OthelloGame as Game
from OthelloLogic import Board
from OthelloIO import get_char_col, translateX

if __name__ == "__main__":
    currentPlayer = 0
    ME = 1
    OPP = -1
    bd = Board()
    g = Game()
    color = g.initColor()
    print(get_char_col('b'))
    """if color == -1:
        currentPlayer = ME
    else:
        currentPlayer = OPP

    while (g.isOver == False):
        if currentPlayer == ME:
            move = g.makeMove(bd, color)
            g.executeMove(bd, color, move)
        else:
            move = g.getMove(bd, -color)
            g.executeMove(bd, -color, move)
        g.display(bd)
        g.countNum(bd)
        currentPlayer = -1*currentPlayer #switch players     
    g.countNum(bd)"""
