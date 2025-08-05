# lib functions for X usage

def print_board(board):
    for i in range(len(board)):
        if ((0 < i) and (0 == i % 8)):
            print()
        print(board[i], end='\t')
    print()
    print('-' * 10)



def read_board(sensehat):
    board = []
    pixels = sensehat.get_pixels()
    for pixel in pixels:
        for i in range(len(pixel)):
            if (0 < pixel[i]):
                pixel[i] = 255
        board.append(MAP.index(pixel))
    return board

