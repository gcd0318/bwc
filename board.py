RED = [255, 0, 0]
GREEN = [0, 255, 0]
BLUE = [0, 0, 255]
WHITE = [255, 255, 255]
DARK = [0, 0, 0]
ON = WHITE
OFF = DARK
MAP = [DARK, RED, GREEN, WHITE]
#REMAP = {}
#for i in range(len(MAP)):
#    REMAP[MAP[i]] = i



GAP = 0.5

BOARD = [0] *8 * 8

turns = []
pos0 = (0, 0)
pos1 = (0, 0)

import threading
import time
from signal import pause

from sense_hat import SenseHat, ACTION_PRESSED, ACTION_HELD, ACTION_RELEASED


def pos2index(x=None, y=None):
    return 8 * x + y


def index2pos(index):
    return (index // 8, index % 8)


def print_board(board=BOARD):
    for i in range(len(board)):
        if ((0 < i) and (0 == i % 8)):
            print()
        print(board[i], end='\t')
    print()
    print('-' * 10)


def led_board(sensehat, board=BOARD, bg=DARK):
    sensehat.clear(bg)
    brd = []
    for i in board:
        if isinstance(i, int):
            brd.append(MAP[i])
        elif isinstance(i, list):
            bar.append(i)

    sensehat.set_pixels(brd)
    return brd


def valid_pos(board, color):
    res = []
    for index in range(len(board)):
        if eq_color(board[index], DARK) and (0 < len(check_step(board, index2pos(index), color))):
            res.append(index)
#            print_board(board)
            print(index)
#            input(index)
    for index in res:
        print('valid:', index2pos(index))
    return res



def default_pos(board, color):
    x, y = None, None

    '''
    index = 0
    while (index < len(board)) and (not eq_color(board[index], DARK)):
        index += 1
    if(index < len(board)):
        x, y = index2pos(index)
    '''
    valids =  valid_pos(board, color)
    if valids:
        x, y = index2pos(valids[0])
    else:
        pass
    print('a valid pos:', x, y)
    ''''''
    return (x, y)


def init_board(sensehat):
    global pos0, pos1, color0, color1, board
    brd = [
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 1, 2, 0, 0, 0,
            0, 0, 0, 2, 1, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            ]
    board = led_board(sensehat, brd)

    pos0 = default_pos(board, color1)
    pos1 = default_pos(board, color1)
    color0 = DARK
    color1 = RED
    
    return board


def eq_color(c0, c1):
    res = True
    i = 0
    while (i < len(c1)) and res:
        res = res and (bool(c0[i]) == bool(c1[i]))
        i += 1
    return res


def clamp(value, min_value=0, max_value=7):
    return value % 8
#    return min(max_value, max(min_value, value))

def pushed_up(event):
    global pos0, pos1, color0, board
    tmp = []
    color0 = DARK
    x, y = pos0
    if event.action != ACTION_RELEASED:
        y = clamp(y - 1)
        while (not eq_color(board[pos2index(x, y)], DARK)) and (8 > len(tmp)):
            tmp.append(y)
            y = clamp(y - 1)
        pos1 = (x, y)


def pushed_down(event):
    global pos0, pos1, color0, board
    tmp = []
    color0 = DARK
    x, y = pos0
    if event.action != ACTION_RELEASED:
        y = clamp(y + 1)
        while (not eq_color(board[pos2index(x, y)], DARK)) and (8 > len(tmp)):
            tmp.append(y)
            y = clamp(y + 1)
        pos1 = (x, y)


def pushed_left(event):
    global pos0, pos1, color0, board
    tmp = []
    color0 = DARK
    x, y = pos0
    if event.action != ACTION_RELEASED:
        x = clamp(x - 1)
        while (not eq_color(board[pos2index(x, y)], DARK)) and (8 > len(tmp)):
            tmp.append(x)
            x = clamp(x - 1)
        pos1 = (x, y)


def pushed_right(event):
    global pos0, pos1, color0, board
    tmp = []
    color0 = DARK
    x, y = pos0
    if event.action != ACTION_RELEASED:
        x = clamp(x + 1)
        while (not eq_color(board[pos2index(x, y)], DARK)) and (8 > len(tmp)):
            tmp.append(x)
            x = clamp(x + 1)
        pos1 = (x, y)



def press(event):
    print(event.action)
    global order, color0, color1, pos0, pos1, board, turns

    if event.action == ACTION_PRESSED:
#    if event.action == ACTION_RELEASED:
        print('pressed at', pos1, 'as', color1)
        turns = check_step(board, pos1, color1)
        print(turns)

        if turns:
            print('to change:', turns)
            for t in turns:
                x, y = t
                print('change', board[pos2index(x, y)], 'to', color1)
                board[pos2index(x, y)] = color1
            
            print_board(board)

            pos0 = pos1
            
            color0 = color1
            if eq_color(RED, color1):
                color1 = GREEN
            elif eq_color(GREEN, color1):
                color1 = RED
            
            pos1 = default_pos(board, color1)

    elif event.action == ACTION_HELD:
        init_board(sh)


def refresh():
    print('to update led matrix')
    global pos0, pos1, color0, color1, board, turns
    
    print('to change:', turns)
    for pos in turns:
        x, y = pos
        board[pos2index(x, y)] = color0
        sh.set_pixel(x, y, color0)
    turns = []
    
    x0, y0 = pos0
    sh.set_pixel(x0, y0, color0)
    board[pos2index(x0, y0)] = color0
    x1, y1 = pos1
    sh.set_pixel(x1, y1, color1)
    board[pos2index(x1, y1)] = color1
    pos0 = (x1, y1)
    print('refreshed all')


def move(sensehat):
    sensehat.stick.direction_up = pushed_up
    sensehat.stick.direction_down = pushed_down
    sensehat.stick.direction_left = pushed_left
    sensehat.stick.direction_right = pushed_right
    sensehat.stick.direction_middle = press
    sensehat.stick.direction_any = refresh
    refresh()
    pause()



def blink(sensehat, gap=GAP, bg=DARK):
    global pos1, color1
    while True:
        time.sleep(gap)
        x, y = pos1
        sensehat.set_pixel(x, y, color1)
        time.sleep(gap)
        x, y = pos1
        sensehat.set_pixel(x, y, bg)



def read_board(sensehat):
    board = []
    pixels = sensehat.get_pixels()
    for pixel in pixels:
        for i in range(len(pixel)):
            if (0 < pixel[i]):
                pixel[i] = 255
        board.append(MAP.index(pixel))
    return board


def check_step(board, step, color):
    turns = []

    print('to check', step, 'as', color)
    
    xs, ys = step
    
    x = xs -1
    while (-1 < x) and (not eq_color(board[pos2index(x, ys)], DARK)) and (not eq_color(board[pos2index(x, ys)], color)):
        x -= 1
    if (-1 < x) and eq_color(board[pos2index(x, ys)], color):
        for i in range(x + 1, xs):
            turns.append((i, ys))
    x = xs + 1
    while (x < 8) and (not eq_color(board[pos2index(x, ys)], DARK)) and (not eq_color(board[pos2index(x, ys)], color)):
#        print(x, board[pos2index(x, ys)], color)
        x += 1
#    print(x)
#    if (x < 8):
#        print(x, ys, board[pos2index(x, ys)], color)
    print_board(board)
    if (x < 8) and eq_color(board[pos2index(x, ys)], color):
        for i in range(xs + 1, x):
            turns.append((i, ys))
    print('- checked:', turns)
    
    y = ys - 1
    while (-1 < y) and (not eq_color(board[pos2index(xs, y)], DARK)) and (not eq_color(board[pos2index(xs, y)], color)):
        y -= 1
    if (-1 < y) and eq_color(board[pos2index(xs, y)], color):
        for i in range(y + 1, ys):
            turns.append((xs, i))
    y = ys + 1
    while (y < 8) and (not eq_color(board[pos2index(xs, y)], DARK)) and (not eq_color(board[pos2index(xs, y)],  color)):
        y += 1
    if (y < 8) and eq_color(board[pos2index(xs, y)], color):
        for i in range(ys + 1, y):
            turns.append((xs, i))
    print('| checked:', turns)

    x, y = xs - 1, ys - 1
    while (-1 < x) and (-1 < y) and (not eq_color(board[pos2index(x, y)], DARK)) and (not eq_color(board[pos2index(x, y)], color)):
        x -= 1
        y -= 1
    if (-1 < x < xs - 1) and (-1 < y < ys - 1) and eq_color(board[pos2index(x, y)], color):
        while (x < xs - 1) and (y < ys - 1):
            x += 1
            y += 1
            turns.append((x, y))
    x, y = xs + 1, ys + 1
    while (x < 8) and (y < 8) and (not eq_color(board[pos2index(x, y)], DARK)) and (not eq_color(board[pos2index(x, y)], color)):
        x += 1
        y += 1
    if (x < 8) and (y < 8) and (not eq_color(board[pos2index(x, y)], DARK)):
        while (xs + 1 < x) and (ys + 1 < y):
            x -= 1
            y -= 1
            turns.append((x, y))
    print('/ checked:', turns)

    x, y = xs - 1, ys + 1
    while (-1 < x) and (y < 8) and (not eq_color(board[pos2index(x, y)], DARK)) and (not eq_color(board[pos2index(x, y)], color)):
        x -= 1
        y += 1
    if (-1 < x < xs - 1) and (ys + 1 < y < 8) and eq_color(board[pos2index(x, y)], color):
        while (x < xs - 1) and (ys + 1 < y):
            x += 1
            y -= 1
            turns.append((x, y))
    x, y = xs + 1, ys - 1
    while (x < 8) and (-1 < y) and (not eq_color(board[pos2index(x, y)], DARK)) and (not eq_color(board[pos2index(x, y)], color)):
        x += 1
        y -= 1
    if (xs + 1 < x < 8) and (-1 < y < ys - 1) and eq_color(board[pos2index(x, y)], color):
        while (xs + 1 < x) and (y < ys - 1):
            x -= 1
            y += 1
            turns.append((x, y))
    print('\ checked:', turns)

    return turns


def winner(sensehat):
    w = 0
    pixels = sensehat.get_pixels()
    for pixel in pixels:
        w += int(eq_color(pixel, RED))
    return w <= len(pixels) / 2






if ('__main__' == __name__):
    sh = SenseHat()
    sh.low_light = True
    sh.clear(DARK)
    sh.set_rotation(0)

    color0 = DARK
    color1 = RED

    board = init_board(sh)
#    pos0 = default_pos(board)
#    pos1 = default_pos(board)


    read_board(sh)

    t0 = threading.Thread(target=move, args=(sh,))
    t1 = threading.Thread(target=blink, args=(sh, GAP, DARK))
    ts = [t0, t1]
    for th in ts:
        th.start()


    print('start')
    for th in ts:
        th.join()


    input('stop')
    sh.clear()

