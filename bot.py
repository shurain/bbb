#!/usr/bin/env python

import os
import time
import tempfile
import autopy
import Image
import learn_board as lb
#import random
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


def n_destroyed(board):
    t_board = []
    for x in board:
        tmp = []
        for y in x:
            tmp.append(y)
        t_board.append(tmp)

    for y in range(6):
        for x in range(8):
            if board[y][x] == board[y + 1][x] == board[y + 2][x]:
                if board[y][x] == '?' or board[y][x] == 'x':
                    continue

                block = board[y][x]

                t_board[y][x] = 'x'
                t_board[y + 1][x] = 'x'
                t_board[y + 2][x] = 'x'

                try:
                    k = 3
                    while k < 8:
                        if block != board[y + k][x]:
                            break
                        t_board[y + k][x] = 'x'
                        k += 1
                except IndexError:
                    pass

    for y in range(8):
        for x in range(6):
            if board[y][x] == board[y][x + 1] == board[y][x + 2]:
                if board[y][x] == '?' or board[y][x] == 'x':
                    continue

                block = board[y][x]

                t_board[y][x] = 'x'
                t_board[y][x + 1] = 'x'
                t_board[y][x + 2] = 'x'

                try:
                    k = 3
                    while k < 8:
                        if block != board[y][x + k]:
                            break
                        t_board[y][x + k] = 'x'
                        k += 1
                except IndexError:
                    pass

    count = 0
    for row in t_board:
        count += row.count('x')

    for y in range(7, -1, -1):
        for x in range(7, -1, -1):
            if t_board[y][x] == 'x':
                k = 0
                while y - k > 0 and t_board[y - k][x] == 'x':
                    k += 1

                if y - k == 0:
                    for j in range(k + 1):
                        t_board[y - j][x] = '?'
                else:
                    for j in range(y, k - 1, -1):
                        t_board[j][x] = t_board[j - k][x]
                    for j in range(k - 1, -1, -1):
                        t_board[j][x] = '?'

    if count == 0:
        return count
    else:
        return count + n_destroyed(t_board)


def find_valid_move(b):
    "Find a valid move"
    valid_moves = []
    for row in range(7):
        if '*' in b[row]:
            valid_moves.append((row, b[row].index('*'), 'down'))
        for col in range(8):
            b[row][col], b[row + 1][col] = b[row + 1][col], b[row][col]
            #if can_destroy(b):
            #    valid_moves.append((row, col, 'down'))
            k = n_destroyed(b)
            if k:
                valid_moves.append((k, row, col, 'down'))
            # Rollback
            b[row][col], b[row + 1][col] = b[row + 1][col], b[row][col]

    for row in range(8):
        if '*' in b[row]:
            valid_moves.append((row, b[row].index('*'), 'right'))
        for col in range(7):
            b[row][col], b[row][col + 1] = b[row][col + 1], b[row][col]
            #if can_destroy(b):
            #    valid_moves.append((row, col, 'right'))
            k = n_destroyed(b)
            if k:
                valid_moves.append((k, row, col, 'right'))
            # Rollback
            b[row][col], b[row][col + 1] = b[row][col + 1], b[row][col]

    return valid_moves


def apply_move(row, col, direction):
    autopy.mouse.move(BOX[0] + 20 + 40 * col, BOX[1] + 20 + 40 * row)
    time.sleep(0.01)
    autopy.mouse.toggle(True)
    time.sleep(0.01)
    if direction == 'down':
        autopy.mouse.move(BOX[0] + 20 + 40 * col,
                BOX[1] + 20 + 40 * (row + 1))
    if direction == 'right':
        autopy.mouse.move(BOX[0] + 20 + 40 * (col + 1),
                BOX[1] + 20 + 40 * row)
    time.sleep(0.01)
    autopy.mouse.toggle(False)
    time.sleep(0.01)


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
        valid_moves.sort(reverse=True)
        #random.shuffle(valid_moves)
        for k, row, col, direction in valid_moves[:4]:
        #for row, col, direction in valid_moves[:1]:
            #print board
            print k, row, col, direction
            #print row, col, direction
            apply_move(row, col, direction)
        cur = time.time()
        if cur - begin > 63:
            break
        #time.sleep(0.125)


if __name__ == '__main__':
    run()
