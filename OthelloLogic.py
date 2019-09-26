import numpy as np

class Board():
    # All 8 directions for the agent to look/go
    directions = [(1,1), (1,0), (1,-1), (0,-1), (-1,-1), (-1, 0), (-1,1), (0,1)]

    def __init__(self):

        #initializes 2-D array showing the pieces
        print("(Board init properly)")
        self.pieces = [None]*8
        for i in range(8):
            self.pieces[i] = [0]*8
        
        #Set up the original pieces 2 black, 2 white
        self.pieces[3][4] = -1
        self.pieces[4][3] = -1
        self.pieces[3][3] = 1
        self.pieces[4][4] = 1

    def __getitem__(self, index):
        """Add indexing ability of board"""
        return self.pieces[index]
    
    def getEmptySquares(self):
        """ Gets a litst of empty squares in the entire board, returns that list """
        emptySquares = list()
        for y in range(8):
            for x in range(8):
                if self.pieces[x][y] == 0:
                    emptySquares.append((x,y))
        return emptySquares
        
    def generateMoves(self, color):
        """ Generates move based off of all empty quares, takes color in the form of -1,1 """
        moveList = list()
        for emptySquare in self.getEmptySquares():
            for direction in self.directions:
                direcX, direcY = direction

                #Gets all possible moves no matter legality
                possMoves = self.incrementMove(emptySquare, direction)

                for move in possMoves:
                    x,y = move
                    if self.pieces[x][y] == -color:
                        continue
                    elif self.pieces[x][y] == 0:
                        break
                    if self.pieces[x][y] == color and self.pieces[x-direcX][y-direcY] != 0 and self.pieces[x-direcX][y-direcY] != color:
                        moveList.append(emptySquare)  
        return moveList

    def makeFlips(self, color, direction, origin):
        #Gets a list of flips given color, direction, and origin
        flipList = [origin]
        flips = self.incrementMove(origin, direction)
        for x,y in flips:
            if self.pieces[x][y] == -color:
                flipList.append((x,y))
            elif (self.pieces[x][y] == 0 or (self[x][y] == color and len(flipList) == 1)):
                break
            elif self.pieces[x][y] == color and len(flipList) > 1:
                print("(",flipList,")")
                return flipList
        return []

    def executeMove(self, color, move):
        flipMoves = []
        for direction in self.directions:
            flipList = self.makeFlips(color, direction, move)
            if len(flipList) > 0:
                flipMoves = flipList
        for x,y in flipMoves:
            self.pieces[x][y] = color
    
    @staticmethod
    def incrementMove(move, direction):
        moves = list()
        x, y = move
        direcX, direcY = direction
        x += direcX
        y += direcY
        while x>=0 and x<8 and y>=0 and y<8:
            moves.append((x,y))
            x+=direcX
            y+=direcY
        return moves
