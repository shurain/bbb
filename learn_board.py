import os
from sklearn import svm
import Image
import numpy as np
#import ImageOps
#import sys
from itertools import chain

classes = {
        'G': 1,
        'B': 2,
        'W': 3,
        'O': 4,
        'Y': 5,
        'R': 6,
        'P': 7,
        '?': 8,
        }


def print_image(im, c):
    for y in range(8):
        for x in range(8):
            GRID = (40 * x, 40 * y, 40 * (x + 1), 40 * (y + 1))
            grid = im.crop(GRID)
            grid.save(str(c[8 * y + x]) + "_" + str(x) + "_" + str(y) + '.png')


def parse_data(im, c):
    X = []
    Y = []
    for y in range(8):
        for x in range(8):
            GRID = (40 * x, 40 * y, 40 * (x + 1), 40 * (y + 1))
            grid = im.crop(GRID)
            pixels = grid.load()
            data = []
            for i in range(4):
                for j in range(4):
                    tot = (0, 0, 0)
                    for k in range(10):
                        for l in range(10):
                            tot = map(sum,
                                    zip(tot, pixels[10 * i + k, 10 * j + l]))
                    rgb = tuple(map(lambda x: x / 100, tot))
                    data.append(rgb)
                    # For testing picked color
                    #for k in range(5):
                    #    for l in range(5):
                    #        pixels[10 * i + k, 10 * j + l] = rgb
            #grid.save(c[y][x] + str(x) + "_" + str(y) + '.png')
            data = list(chain.from_iterable(data))
            pixels = np.array(data)

            cls = classes[c[y][x]]
            X.append(pixels)
            Y.append(cls)
    return X, Y


def learn_board(X, Y):
    clf = svm.SVC()
    clf.fit(X, Y)
    return clf


def test_board(clf, X):
    result = clf.predict(X)
    return result


def run(PATH):
    data = []
    for root, dirs, files in os.walk(PATH):
        for f in files:
            if f.endswith('.png'):
                filename = f.split('.')[0]
                im = Image.open(os.path.join(root, f))
                with open(os.path.join(root, filename + '.dat'), 'r') as c:
                    dat = c.readlines()
                d = []
                for row in dat:
                    d.append(row.split())
                data.append((im, d))

    count = 0
    train_X = []
    train_Y = []
    test_images = ''
    for im, dat in data:
        if count == 0:
            test_images = im
            test_X, test_Y = parse_data(im, dat)
            count += 1
            continue
        temp_X, temp_Y = parse_data(im, dat)
        train_X += temp_X
        train_Y += temp_Y

    clf = learn_board(train_X, train_Y)
    prediction = test_board(clf, test_X)

    #print_image(test_images, prediction)


if __name__ == '__main__':
    PATH = 'learn'
    run(PATH)
