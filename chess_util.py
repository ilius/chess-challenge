"""
contains some chess-related utility functions
"""

import random
from cmd_util import input_int


def format_board(board, row_count, col_count):
    """
    convert a `board` into string than can be shown in console

    board: a dict { (row_num, col_num) => piece_symbol }
    row_count: number of rows
    col_count: number of columns
    """
    sep_line = '-' * (col_count * 4 + 1)
    lines = [sep_line]
    for row_num in range(row_count):
        lines.append(
            '| ' + ' | '.join([
                board.get((row_num, col_num), ' ')
                for col_num in range(col_count)
            ]) + ' |'
        )
        lines.append(sep_line)
    return '\n'.join(lines)


def make_random_board(row_count, col_count, density=0.5):
    """create a random chess board with given size and density"""
    board = {}
    for row_num in range(row_count):
        for col_num in range(col_count):
            factor = random.random() / density
            if factor >= 1:
                continue
            index = int(factor * len(ChessPiece.class_list))
            board[(row_num, col_num)] = ChessPiece.class_list[index].symbol
    return board


def test_format_random_board(density=0.5):
    """test `format_random_board` function"""
    while True:
        row_count = input_int('Number of rows: ', minimum=2, default=0)
        if row_count == 0:
            break
        col_count = input_int('Number of columns: ', minimum=2)
        board = make_random_board(row_count, col_count, density)
        print(format_board(board, row_count, col_count))
        print('\n\n')


if __name__ == '__main__':
    test_format_random_board(density=0.5)
