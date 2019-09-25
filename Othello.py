class Board():
    # All 8 directions for the agent to look/go
    directions = [(1,1), (1,0), (1,-1), (0,-1), (-1,-1), (-1, 0), (-1,-1), (0,1)]

    def __init__(self, color):

        self.color = color
        #initializes 2-D array showing the pieces
        self.pieces = [None]*8

        for i in range(8):
            self.pieces[i] = [0]*8
        
        #Set up the original pieces 2 black, 2 white
        self.pieces[3][4] = -1
        self.pieces[4][3] = -1
        self.pieces[3][3] = 1
        self.pieces[4][4] = 1
        print(self.pieces)

    def __getitem__(self, index):
        return self.pieces[index]
    
    def generateMoves(self):
        #Looks for valid moves at current board state#
        #Returns a list of moves#
        color = self.color

    def makeFlips(self, color, direction, origin):

        flipList = [origin]

        for x,y in self.incrementMove(origin, direction):
            print("Working on ")
            print(self.pieces[x][y])
            if self.pieces[x][y] == 0 :
                print("None found")
                print(flipList)
                return flipList

            if self.pieces[x][y] == -color:
                print("Appended")
                flipList.append((x,y))

            elif self.pieces[x][y] == color and len(flipList) > 1:
                print(flipList)
                return flipList
    

    def executeMove(self, color, move):
        flipMoves = []
        for direction in self.directions:
            flipList = self.makeFlips(color, direction, move)
            if len(flipList) > 0:
                flipMoves = flipList
        for x,y in flipMoves:
            self.pieces[x][y] = color

    def getValidMoves(self, color):

        validMoves = set()

        for x in range(8):
            for y in range(8):
                if self.pieces[x][y]==color:
                    newValidMoves = self.findAllMoves(color, (x,y))
                    validMoves.update(newValidMoves)

        return list(validMoves)

    def findAllMoves(self, color, origin):

        possibleMoves = []
        x, y = origin

        if color==0:
            return None
        
        for direction in self.directions:
            oneMove = self.findMoves(origin, direction)
            if oneMove:
                possibleMoves.append(oneMove)

        return possibleMoves

    
    def findMoves(self, originPiece, direction):
        #Finds moves based on origin tuple given and the direction wanted to go#
        x, y = originPiece
        flipMoves = []

        for x,y in self.incrementMove(originPiece, direction):
            if self.pieces[x][y] == color and flipMoves:
                return (x,y)
            elif self.pieces[x][y] == -(color):
                flipMoves.append((x,y))
            elif self.pieces[x][y] == color:
                return None
        
    def incrementMove(self, move, direction):
        moves = list()
        x, y = move
        direcX, direcY = direction
        x+=direcX
        y+=direcY
        while x>=0 and x<8 and y>=0 and y<8:
            print(x, y)
            moves.append((x,y))
            x+=direcX
            y+=direcY
        print(moves)
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
            print(str(y+1) + ' |', end = ''),
            for x in range(8):
                # Get the piece to print
                piece = self.pieces[x][y]
                if piece == -1: 
                    print(" B ", end = ''),
                elif piece == 1: 
                    print(" W ", end = ''),
                else:
                    print(" . ", end = ''),
            print('| ' + str(y+1))
        print("    ----------------------")
        print("    A  B  C  D  E  F  G  H")

if __name__ == '__main__':
    board = Board(1)
    board.display()
    board.countNum()
    #board.incrementMove((3,3), (1,1))
    board.makeFlips(1, (0,1), (3,3))
    board.executeMove(1, (3,5))
    board.display()
