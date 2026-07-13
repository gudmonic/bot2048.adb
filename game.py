import numpy as np

SIZE = 4

LEFT = 0
RIGHT = 1
UP = 2
DOWN = 3


def compress(row):

    row = row[row != 0]

    result = []

    i = 0

    while i < len(row):

        if i + 1 < len(row) and row[i] == row[i + 1]:
            result.append(row[i] * 2)
            i += 2
        else:
            result.append(row[i])
            i += 1

    while len(result) < SIZE:
        result.append(0)

    return np.array(result)



def move_left(board):

    new = np.zeros((4,4), dtype=int)

    changed = False

    for i in range(4):

        row = compress(board[i])

        new[i] = row

        if not np.array_equal(row, board[i]):
            changed = True

    return new, changed



def move_right(board):

    b = np.fliplr(board)

    b, changed = move_left(b)

    return np.fliplr(b), changed



def move_up(board):

    b = board.T

    b, changed = move_left(b)

    return b.T, changed



def move_down(board):

    b = board.T

    b, changed = move_right(b)

    return b.T, changed



MOVES = {
    0: move_left,
    1: move_right,
    2: move_up,
    3: move_down
}



def make_move(board, move):

    return MOVES[move](board)



def empty_cells(board):

    return list(zip(*np.where(board == 0)))



def game_over(board):

    if len(empty_cells(board)) > 0:
        return False


    for move in MOVES:

        _, changed = make_move(board, move)

        if changed:
            return False


    return True