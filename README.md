Bejeweld Blitz Bot
==================

Usage
-----
For training the block image classifier,
    $ python learn_board.py
This drops a file named `trained`.

At the beginning of the game, run the following script.
    $ python bot.py


Method
------
Recognizing the board state is arguably the most difficult part.
Each block image spins, changes colors, gets covered by scores etc.
These changes makes it very difficult to figure out the color/shape of a block.

Since a block consists of 40 x 40 pixel values, this can be divided into 10 x 10 pixel boxes.
Each block is divided into 4 x 4 pixel sub-block and among those 16 sub-blocks,
middle 4 blocks are used to represent the entire block.
The RGB value of the sub-block is averaged over to represent that sub-block.
Therefore, a single block is represented by four features.
Or rather, four-value tuple of a single feature.

Classification
--------------
It is worth mentioning that we need more data when the board state is unstable.
Without such data, the classifier classifies invalid blocks as valid blocks,
which in turn, affects how valid blocks are being classified as well.
