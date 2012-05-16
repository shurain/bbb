#!/usr/bin/env python

import os
import time
import tempfile
import autopy
import Image
import learn_board as lb
import random
import sys


BOX = (379, 398, 702, 715)  # top x, y, bottom x, y of the board
#G=1, B=2, W=3, O=4, Y=5, R=6, P=7, Nothing=0


def grab_screen():
    timestamp = str(int(time.time()))
    filename = 'full_snapshot_' + timestamp + '.png'
    filepath = os.path.join(tempfile.gettempdir(), filename)
    os.system("screencapture -x -T 0 " + filepath)
    image = Image.open(filepath)
    im = image.crop(BOX)
    #if random.random() > .95:
    #    im.save('snapshot_' + timestamp + '.png')
    return im


def can_destroy(board):
    "Find 3 or more consecutive blocks"
    for x in range(6):
        for y in range(8):
            if board[x][y] == board[x + 1][y] == board[x + 2][y]:
                if board[x][y] != '?':
                    return True
    for x in range(8):
        for y in range(6):
            if board[x][y] == board[x][y + 1] == board[x][y + 2]:
                if board[x][y] != '?':
                    return True
    return False


def find_valid_move(b):
    "Find a valid move"
    valid_moves = []
    for row in range(7):
        if '*' in b[row]:
            valid_moves.append((row, b[row].index('*'), 'down'))
        for col in range(8):
            b[row][col], b[row + 1][col] = b[row + 1][col], b[row][col]
            if can_destroy(b):
                valid_moves.append((row, col, 'down'))
            # Rollback
            b[row][col], b[row + 1][col] = b[row + 1][col], b[row][col]

    for row in range(8):
        if '*' in b[row]:
            valid_moves.append((row, b[row].index('*'), 'right'))
        for col in range(7):
            b[row][col], b[row][col + 1] = b[row][col + 1], b[row][col]
            if can_destroy(b):
                valid_moves.append((row, col, 'right'))
            # Rollback
            b[row][col], b[row][col + 1] = b[row][col + 1], b[row][col]

    #for row in range(7):
    #    if '*' in b[row]:
    #        valid_moves.append(row, b[row].index('*'), 'down')
    #    for col in range(7):
    #        b[row][col], b[row + 1][col] = b[row + 1][col], b[row][col]
    #        if can_destroy(b):
    #            valid_moves.append((row, col, 'down'))
    #        # Rollback
    #        b[row][col], b[row + 1][col] = b[row + 1][col], b[row][col]
    #        b[row][col], b[row][col + 1] = b[row][col + 1], b[row][col]
    #        if can_destroy(b):
    #            valid_moves.append((row, col, 'right'))
    #        # Rollback
    #        b[row][col], b[row][col + 1] = b[row][col + 1], b[row][col]
    return valid_moves


def apply_move(row, col, direction):
    autopy.mouse.move(BOX[0] + 20 + 40 * col, BOX[1] + 20 + 40 * row)
    time.sleep(0.01)
    autopy.mouse.click()
    time.sleep(0.01)
    if direction == 'down':
        autopy.mouse.move(BOX[0] + 20 + 40 * col,
                BOX[1] + 20 + 40 * (row + 1))
    if direction == 'right':
        autopy.mouse.move(BOX[0] + 20 + 40 * (col + 1),
                BOX[1] + 20 + 40 * row)
    time.sleep(0.01)
    autopy.mouse.click()


def run():
    b = lb.Board()
    bp = lb.BoardParser
    f = open('trained', 'r')
    b.load(f)
    begin = time.time()
    count = 0
    while(True):
        im = grab_screen()
        board = bp.get_board(im, b)
        valid_moves = find_valid_move(board)
        if not valid_moves:
            count += 1
            if count > 10:
                im.save('snapshot_' + str(int(time.time())) + '.png')
                print board
                sys.exit()
            continue
        count = 0
        random.shuffle(valid_moves)
        #for row, col, direction in valid_moves[:5]:
        for row, col, direction in valid_moves:
            apply_move(row, col, direction)
        cur = time.time()
        if cur - begin > 63:
            break


if __name__ == '__main__':
    run()
