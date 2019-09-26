from OthelloGame import OthelloGame as Game
from OthelloLogic import Board

if __name__ == "__main__":
    bd = Board()
    g = Game()
    g.display(bd)
    g.makeMoves(bd, 1)
    g.display(bd)
    g.makeMoves(bd, -1)
    g.display(bd)
    g.countNum(bd)