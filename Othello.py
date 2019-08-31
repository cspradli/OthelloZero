class Board():

    directions = [(1,1), (1,0), (1,-1), (0,-1), (-1,-1), (-1, 0), (-1,-1), (0,1)]

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
        print(self.pieces)

    def __getIndexedItem__(self, indeX, indeY):
        print(self.pieces[indeX][indeY])
        return self.pieces[indeX][indeY]

if __name__ == '__main__':
    board = Board()
    board.__getIndexedItem__(3,3)
