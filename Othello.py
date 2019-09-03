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

        
    
    def findMoves(self, originPiece, direction):
        #Finds moves based on origin tuple given and the direction wanted to go#
        (x, y) = originPiece
        


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
    board = Board((3, 3))
    board.__getIndexedItem__(3,3)
    board.display()
    board.countNum()
    board.findMoves((3,3), (1,1))

