from OthelloGame import OthelloGame as Game
from OthelloLogic import Board

class main():

    def getInput(self):
        inp = input()
        if inp.startswith('C'):
            return None
        elif len(inp) == 1:
            if inp == 'n'
                print("End game")
            if inp == 'B' or inp == 'W'
                #opponent passes
                self.makeMoves()

if __name__ == "__main__":
    bd = Board()
    g = Game()
    color = g.initColor()
    #Start current player as black
    if color == -1:
        currPlayer = -1
    while (not g.isOver(bd, color)):
        #unless current player needs to be white
        if color == 1:
            currPlayer = 1
        if currPlayer == -1:
            move = g.makeMove(bd, color)
            currPlayer = 1
        else:
            move = g.getMove()
            currPlayer = -1
        g.executeMove(bd, color, move)
    g.countNum(bd)
