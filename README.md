Bejeweld Blitz Bot
==================

Usage
-----
    $ python learn_board.py

Modify the given code for training.
Simple test of accuracy can be also performed with this script.

    $ python bot.py

Still a lot has to be done but it's a start.


Method
------
Recognizing the board state is arguably the most difficult part.
Each block image spins, changes colors, gets covered by scores etc.
These changes makes it very difficult to figure out the color/shape of a block.


Since a block consists of 40 x 40 pixel values, this can be divided into 10 x 10 pixel boxes.
Each block is divided into 4 x 4 sub-block and among those 16 sub-blocks,
middle 4 blocks are used to represent the entire block.
The RGB value of the sub-block is averaged over to represent that sub-block.
Therefore, a single block is represented by four features.
Or rather, four-value tuple of a single feature.
