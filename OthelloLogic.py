import numpy as np

class Board():
    # All 8 directions for the agent to look/go
    directions = [(1,1), (1,0), (1,-1), (0,-1), (-1,-1), (-1, 0), (-1,1), (0,1)]

    def __init__(self):

        #initializes 2-D array showing the pieces
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

        print("Moves for", color, end=' ')
        print(moveList)
        return moveList

    def makeFlips(self, color, direction, origin):
        #Gets a list of flips given color, direction, and origin
        flipList = [origin]
        flips = self.incrementMove(origin, direction)
        print(flips)
        for x,y in flips:
            print("Working on ")
            if self.pieces[x][y] == -color:
                print("appended")
                flipList.append((x,y))
            elif (self.pieces[x][y] == 0 or (self[x][y] == color and len(flipList) == 1)):
                print("nothing here")
                break
            elif self.pieces[x][y] == color and len(flipList) > 1:
                print(flipList)
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

    def countNum(self):
        # Counts the number of stones each player has
        # Returns both counts
        countW = 0
        countB = 0
        for y in range(8):
            for x in range(8):
                piece = self.pieces[x][y]
                if piece == -1:
                    countB += 1
                elif piece == 1:
                    countW += 1
        print("White count: " + str(countW))
        print("Black count: " + str(countB))
        return countW, countB
    
    def display(self):
        # Display the board #
        print("    A  B  C  D  E  F  G  H")
        print("    ----------------------")
        for y in range(7,-1,-1):
            # Print the row number
            print(str(y) + ' |', end = ''),
            for x in range(8):
                # Get the piece to print
                piece = self.pieces[x][y]
                print("(", x, y, ")",  end = ''),
                if piece == -1: 
                    print(" B ", end = ''),
                elif piece == 1: 
                    print(" W ", end = ''),
                else:
                    print(" . ", end = ''),
            print('| ' + str(y))
        print("    ----------------------")
        print("    A  B  C  D  E  F  G  H")

if __name__ == '__main__':
    board = Board()
    board.display()
    board.getEmptySquares()
    board.generateMoves(-1)
    board.generateMoves(1)
    board.executeMove(-1, (3,2))
    board.display()
    board.generateMoves(1)
    board.executeMove(1, (2,2))
    board.display()
