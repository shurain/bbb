import os
from sklearn import svm
import Image
#import ImageOps
from itertools import chain
import pickle
#import time


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


class BoardParser:
    def __init__(self):
        pass

    @classmethod
    def extract_blocks(cls, im):
        X = []
        for y in range(8):
            for x in range(8):
                GRID = (40 * x, 40 * y, 40 * (x + 1), 40 * (y + 1))
                grid = im.crop(GRID)
                pixels = grid.load()
                X.append(pixels)
        return X

    @classmethod
    def extract_features(cls, b_pixels):
        data = []
        for i in range(1, 3):
            for j in range(1, 3):
                tot = (0, 0, 0)
                for k in range(10):
                    for l in range(10):
                        tot = map(sum,
                                zip(tot, b_pixels[10 * i + k, 10 * j + l]))
                rgb = tuple(map(lambda x: x / 100, tot))
                data.append(rgb)
                # For testing picked color
                #for k in range(5):
                #    for l in range(5):
                #        pixels[10 * i + k, 10 * j + l] = rgb
        #grid.save(c[y][x] + str(x) + "_" + str(y) + '.png')
        data = list(chain.from_iterable(data))
        return data

    @classmethod
    def get_board(cls, im, classifier):
        blocks = cls.extract_blocks(im)
        features = []
        for block in blocks:
            features.append(cls.extract_features(block))
        result = list(classifier.predict(features))
        result = [COLORS[int(r)] for r in result]
        result.reverse()
        board = []
        while len(result):
            tmp = []
            for x in range(8):
                tmp.append(result.pop())
            board.append(tmp)
        return board


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

    features = []
    cls = []
    #test_im = ''
    for im, dat in data:
        #test_im = im
        blocks = BoardParser.extract_blocks(im)
        for block in blocks:
            features.append(BoardParser.extract_features(block))
        for y in range(8):
            for x in range(8):
                cls.append(classes[dat[y][x]])

    b = Board()
    b.learn(features, cls)
    with open('trained', 'w') as f:
        b.dump(f)

    #blocks = BoardParser.extract_blocks(test_im)
    #features = []
    #for block in blocks:
    #    features.append(BoardParser.extract_features(block))

    #test_im.save("!.png")
    #print b.predict(features)


if __name__ == '__main__':
    PATH = 'learn'
    run(PATH)
