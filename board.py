from const import RED, GREEN, BLUE, WHITE, DARK, ON, OFF, MAP
from const import GAP, BOARD
from const import init_brd

from lib import print_board

import threading
import time
from signal import pause

from sense_hat import SenseHat, ACTION_PRESSED, ACTION_HELD, ACTION_RELEASED


turns = []
valids = {}
pos0 = (0, 0)
pos1 = (0, 0)
switchs = 0



def pos2index(x=None, y=None):
    return x + 8 * y


def index2pos(index):
    return (index % 8, index // 8)


def show_board(sensehat, board=BOARD, bg=DARK):
    sensehat.clear(bg)
    brd = []
    for i in board:
        if isinstance(i, int):
            brd.append(MAP[i])
        elif isinstance(i, list):
            brd.append(i)

    sensehat.set_pixels(brd)
    return brd


def valid_pos(board, color):
    res = {}
    for index in range(len(board)):
        turns = check_step(board, index2pos(index), color)
        if eq_color(board[index], DARK) and (0 < len(turns)):
            res[index] = turns
    for index in res:
        print('valid:', index2pos(index))
    return res



def default_pos(board, color):
    global valids

    x, y = None, None

    valids =  valid_pos(board, color)
    if valids:
        x, y = index2pos(list(valids.keys())[0])
        print('a valid pos:', x, y)
#    else:
#        index = 0
#        while (index < len(board)) and (not eq_color(board[index], DARK)):
#            index += 1
#        if(index < len(board)):
#            x, y = index2pos(index)
    return (x, y)


def init_board(sensehat, brd=None):
    global pos0, pos1, color0, color1

    if brd is None:
        brd = init_brd

    board = show_board(sensehat, brd, bg=DARK)

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
    global order, color0, color1, pos0, pos1, board, turns, switchs

    print('to press at:', pos1, 'as', color1)

    if event.action == ACTION_PRESSED:
#    if event.action == ACTION_RELEASED:
        print('pressed at', pos1, 'as', color1)

#        turns = check_step(board, pos1, color1)
        x1, y1 = pos1
        index1 = pos2index(x1, y1)
        if index1 in valids:
            turns = valids[index1]

 #       if turns:
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
            x1, y1 = pos1
            switchs = 0
            while (x1 is None) and (y1 is None) and (switchs < 2):
                color0, color1 = color1, color0
                pos1 = default_pos(board, color1)
                x1, y1 = pos1
                switchs += 1

    elif event.action == ACTION_HELD:
        board = init_board(sh)


def refresh():
    print('to update led matrix')
    global pos0, pos1, color0, color1, board, turns, switchs

    color = [color0, color1][switchs // 2]

    print('to change:', turns, 'to', color)

    for pos in turns:
        x, y = pos
        board[pos2index(x, y)] = color
        sh.set_pixel(x, y, color)
    turns = []

    x0, y0 = pos0
    sh.set_pixel(x0, y0, color0)
    board[pos2index(x0, y0)] = color0

    if (2 <= switchs):
        i = board_as_matrix(board, sh)
        if (len(board) == board_as_matrix(board, sh)):
            pos1 = (None, None)
            x, y = pos0
            sh.set_pixel(x, y, color)
            if redwin(sh):
               winner = RED
            else:
                winner = GREEN
            print(winner)
            sh.set_pixels([winner] * 64)
            print('board and matrix match')
        else:
            i = board_as_matrix(board, sh)
            print(i, board[i], index2pos(i))
            x, y = index2pos(i)
            p = sh.get_pixel(x, y)
            print(x, y, p)
            print_board(board)
            input('board and matrix not match')

    else:
        x1, y1 = pos1
        sh.set_pixel(x1, y1, color1)
        board[pos2index(x1, y1)] = color1
        pos0 = (x1, y1)

    print('refreshed all')


def board_as_matrix(board, sensehat):
    pixels = sensehat.get_pixels()
    for i in range(64):
        print(i, index2pos(i), pixels[i])
    index = 0
    while (index < len(pixels)) and eq_color(board[index], pixels[index]):
        index += 1
    return index



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
    global pos1, color1, blinking
    while True:
        time.sleep(gap)
        x, y = pos1
        if (x is not None) and (y is not None):
            sensehat.set_pixel(x, y, color1)
        time.sleep(gap)
        x, y = pos1
        if (x is not None) and (y is not None):
            sensehat.set_pixel(x, y, bg)



def check_step(board, step, color):
    turns = []

    print('to check', step, 'as', color)

    xs, ys = step

    if (xs is not None) and (ys is not None):
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
 #       print_board(board)
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


def redwin(sensehat):
    r = 0
    d = 0
    pixels = sensehat.get_pixels()
    for pixel in pixels:
        r += int(eq_color(pixel, RED))
        d += int(eq_color(pixel, DARK))
    return (len(pixels) - d) / 2 < r



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

