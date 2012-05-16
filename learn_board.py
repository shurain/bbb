import os
from sklearn import svm
import Image
import numpy as np
#import ImageOps
#import sys
from itertools import chain
import pickle
import time


class Board:
    def __init__(self):
        pass

    def dump(self, f):
        pickle.dump(self.clf, f)

    def load(self, f):
        self.clf = pickle.load(f)

    def learn(self, X, Y):
        if not hasattr(self, 'clf'):
            self.clf = svm.SVC()
        self.clf.fit(X, Y)

    def predict(self, X):
        return self.clf.predict(X)

    def get_board(self, im):
        X = []
        for y in range(8):
            tmp = []
            for x in range(8):
                GRID = (40 * x, 40 * y, 40 * (x + 1), 40 * (y + 1))
                grid = im.crop(GRID)
                pixels = grid.load()
                data = []
                for i in range(1, 3):
                    for j in range(1, 3):
                        tot = (0, 0, 0)
                        for k in range(10):
                            for l in range(10):
                                tot = map(sum,
                                        zip(tot,
                                            pixels[10 * i + k, 10 * j + l]))
                        # For testing picked color
                        rgb = tuple(map(lambda x: x / 100, tot))
                        data.append(rgb)
                        #for k in range(5):
                        #    for l in range(5):
                        #        pixels[10 * i + k, 10 * j + l] = rgb
                data = list(chain.from_iterable(data))
                pixels = np.array(data)
                result = self.clf.predict(pixels)
                grid.save(str(int(result)) + "_"
                        + str(int(time.time())) + '.png')
                #grid.save(str(int(result)) + '_' +
                #        str(x) + "_" + str(y) + '.png')
                tmp.append(COLORS[int(result)])
            X.append(tmp)
        return X


COLORS = {
        1: 'green',
        2: 'blue',
        3: 'white',
        4: 'orange',
        5: 'yellow',
        6: 'red',
        7: 'purple',
        8: '?',
        }


classes = {
        'G': 1,
        'B': 2,
        'W': 3,
        'O': 4,
        'Y': 5,
        'R': 6,
        'P': 7,
        '?': 8,
        '*': 9,
        }


def parse_data(im, c):
    X = []
    Y = []
    for y in range(8):
        for x in range(8):
            GRID = (40 * x, 40 * y, 40 * (x + 1), 40 * (y + 1))
            grid = im.crop(GRID)
            pixels = grid.load()
            data = []
            for i in range(1, 3):
                for j in range(1, 3):
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

    train_X = []
    train_Y = []
    for im, dat in data:
        temp_X, temp_Y = parse_data(im, dat)
        train_X += temp_X
        train_Y += temp_Y

    f = open('trained', 'w')
    b = Board()
    b.learn(train_X, train_Y)
    b.dump(f)


if __name__ == '__main__':
    PATH = 'learn'
    run(PATH)
