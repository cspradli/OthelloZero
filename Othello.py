class Board():

    directions = [(1,1), (1,0), (1,-1), (0,-1), (-1,-1), (-1, 0), (-1,-1), (0,1)]

    def __init__(self):
        self.pieces = [None]*8
        for i in range(8):
            self.pieces[i] = [0]*8
        
        