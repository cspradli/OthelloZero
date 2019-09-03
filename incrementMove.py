def _incrementMove(move, direction):
    moves = list()
    x, y = move
    direcX, direcY = direction
    print(x)
    print(y)
    print(direcX)
    print(direcY)
    x+=direcX
    y+=direcY
    while x>=0 and x<8 and y>=0 and y<8:
        moves.append((x,y))
        x+=direcX
        y+=direcY
    print(moves)

if __name__ == "__main__":
    move = (3,3)
    direction = (0,1)
    _incrementMove(move, direction)