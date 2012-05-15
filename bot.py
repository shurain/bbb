#!/usr/bin/env python

import os
import time
import tempfile
import autopy
import Image


BOX = (379, 398, 702, 715)  # top x, y, bottom x, y of the board
START_X = 188
START_Y = 63  # Grid starting position in pixel.
GRID = 40  # Single grid dimension. 40 x 40 pixel
BOARD = 8  # Whole board. 8 x 8

GREEN = (94, 254, 141)
BLUE = (27, 135, 254)
WHITE = (254, 254, 254)
ORANGE = (254, 251, 130)
YELLOW = (254, 254, 54)
RED = (254, 38, 75)
PURPLE = (254, 124, 254)
#G=1, B=2, W=3, O=4, Y=5, R=6, P=7, Nothing=0

COLORS = {
        (94, 254, 141): 'green',
        (27, 135, 254): 'blue',
        (254, 254, 254): 'white',
        (254, 251, 130): 'orange',
        (254, 254, 54): 'yellow',
        (254, 38, 75): 'red',
        (254, 124, 254): 'purple',
        }


def grab_screen():
    timestamp = str(int(time.time()))
    filename = 'full_snapshot_' + timestamp + '.png'
    filepath = os.path.join(tempfile.gettempdir(), filename)
    os.system("screencapture -x -T 0 " + filepath)
    image = Image.open(filepath)
    im = image.crop(BOX)
    im.save('snapshot_' + timestamp + '.png')
    return im


def parse_screen(im):
    pix = im.load()
    board = []
    for y in range(BOARD):
        row = []
        for x in range(BOARD):
            tmp = pix[(START_X + 40 * x, START_Y + 40 * y)]
            row.append(COLORS[tmp])
        board.append(row)
    return board


def can_destroy(board):
    "Find 3 or more consecutive blocks"
    for x in range(6):
        for y in range(6):
            if board[x][y] == board[x][y + 1] == board[x][y + 2]:
                return True
            if board[x][y] == board[x + 1][y] == board[x + 2][y]:
                return True
    return False


def find_valid_move(b):
    "Find a valid move"
    for row in range(6):
        for col in range(6):
            b[row][col], b[row + 1][col] = b[row + 1][col], b[row][col]
            if can_destroy(b):
                return (row, col, 'down')
            # Rollback
            b[row][col], b[row + 1][col] = b[row + 1][col], b[row][col]
            b[row][col], b[row][col + 1] = b[row][col + 1], b[row][col]
            if can_destroy(b):
                return (row, col, 'right')
            # Rollback
            b[row][col], b[row][col + 1] = b[row][col + 1], b[row][col]
    return None


def apply_move(row, col, direction):
    autopy.mouse.move(BOX[0] + START_X + 40 * col, BOX[1] + START_Y + 40 * row)
    autopy.mouse.click()
    if direction == 'down':
        autopy.mouse.move(BOX[0] + START_X + 40 * col,
                BOX[1] + START_Y + 40 * (row + 1))
    if direction == 'right':
        autopy.mouse.move(BOX[0] + START_X + 40 * (col + 1),
                BOX[1] + START_Y + 40 * row)


def run():
    #im = Image.open('snapshot_1337025932.png')
    #c_list = im.crop((168, 50, 168+40, 50+40)).getcolors(1024)
    #print c_list
    #for cl in COLORS:
    #    print cl
    #    if cl in c_list:
    #        print "!", cl

    while True:
        grab_screen()
        time.sleep(1)
    #while(True):
    #    im = grab_screen()
    #    board = parse_screen(im)
    #    row, col, direction = find_valid_move(board)
    #    apply_move(row, col, direction)
    #    time.sleep(0.1)


if __name__ == '__main__':
    run()
