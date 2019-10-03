"""
    OthelloZero: OthelloLogic
    Author: Caleb Spradlin
    Date: 27/09/19 
    This file is the main logic file for the Othello system, given the right params, a 2-d board is set up and moves can be made/executed/etc
"""

class Board():
    # All 8 directions for the agent to look/go
    directions = [(1,1), (1,0), (1,-1), (0,-1), (-1,-1), (-1, 0), (-1,1), (0,1)]

    def __init__(self):

        #initializes 2-D array showing the pieces
        print("C (Board init properly)")
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
                directionX, directionY = direction

                #Gets all possible moves no matter legality
                possMoves = self.incrementMove(emptySquare, direction)
                for move in possMoves:
                    x,y = move
                    if self.pieces[x][y] == -color:
                        continue
                    elif self.pieces[x][y] == 0:
                        break
                    if self.pieces[x][y] == color:
                        if self.pieces[x-directionX][y-directionY] != 0:
                            if self.pieces[x-directionX][y-directionY] != color:
                                if len(self.makeFlips(color, direction, emptySquare)) > 0:
                                    moveList.append(emptySquare)
                        #moveList.append(emptySquare)  
        return moveList

    def makeFlips(self, color, direction, origin):
        #Gets a list of flips given color, direction, and origin
        flipList = list()
        flipList.append(origin)
        flips = self.incrementMove(origin, direction)
        for flip in flips:
            x,y = flip
            if self.pieces[x][y] == -color:
                flipList.append((x,y))
            elif (self.pieces[x][y] == 0 or (self[x][y] == color and len(flipList) == 1)):
                break
            elif self.pieces[x][y] == color and len(flipList) > 1:
                print("C (",flipList,")")
                return flipList
        return []

    def checkExecute(self, color, move):
        for direction in self.directions:
            dx, dy = direction
            x,y = move
            if self.pieces[x-dx][y-dy] == 0 or self.pieces[x-dx][y-dy] == color:
                print("C FALSE MOVE- pick another")
                return False
        return True

    def executeMove(self, color, move):
        flipMoves = list()
        for direction in self.directions:
            flipList = self.makeFlips(color, direction, move)
            if len(flipList) > 0:
                flipMoves.extend(flipList)
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
