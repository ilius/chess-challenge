#!/usr/bin/env python3
"""responsible for calling other modules and interacting with user"""

import sys
from time import time as now
import random

from pieces import ChessPiece
from solution import (
    find_solutions_s,
    find_solutions_r,
    find_solutions_q,
)

PIECE_SYMBOLS = 'KQBRN'  # must not re-order


def input_int(prompt, default=None, minimum=None, maximum=None):
    """
    ask the user to enter an integer number
    make sure it's an integer, and within possibly given criteria
    default: default value (if the user leaves it empty)
             if default is None, user can not leave it empty
    minimum: minimum allowed value, or None
    maximum: maximum allowed value, or None
    """
    while True:
        value_str = input(prompt).strip()
        if not value_str:
            if default is None:
                print('Can not leave empty')
                continue
            else:
                return default
        try:
            value = int(value_str)
        except ValueError:
            print('Must enter an integer number')
            continue

        if minimum is not None and value < minimum:
            print('Must enter greater than or equal to %s' % minimum)
            continue

        if maximum is not None and value > maximum:
            print('Must enter less than or equal to %s' % maximum)
            continue

        return value


def input_pieces_count(row_count, col_count):
    """
    ask the user the number or chess pieces of each type
    return a dict { piece_symbol => count }

    row_count: number of rows
    col_count: number of columns
    """
    cell_count = row_count * col_count
    count_by_symbol = {}
    total_count = 0
    for symbol in PIECE_SYMBOLS:
        cls = ChessPiece.class_by_symbol[symbol]
        plural_name = cls.name.capitalize() + 's'
        count = input_int(
            'Number of %s: ' % plural_name,
            default=0,
            minimum=0,
            maximum=cell_count-total_count,
        )
        count_by_symbol[symbol] = count
        total_count += count
    return count_by_symbol


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


def input_problem():
    """
    get the board size and pieces count from stdin or command line arguments
    """
    if len(sys.argv) == 3 + len(ChessPiece.class_list):
        row_count = int(sys.argv[1])
        col_count = int(sys.argv[2])
        count_by_symbol = {}
        print('Number of rows: %s' % row_count)
        print('Number of columns: %s' % col_count)
        print()
        for index, symbol in enumerate(PIECE_SYMBOLS):
            cls = ChessPiece.class_by_symbol[symbol]
            count_by_symbol[cls.symbol] = int(sys.argv[3+index])
            print('Number of %ss: %s' % (
                cls.name.capitalize(),
                count_by_symbol[cls.symbol],
            ))
    else:
        row_count = input_int('Number of rows: ', minimum=2)
        col_count = input_int('Number of columns: ', minimum=2)
        print()
        count_by_symbol = input_pieces_count(row_count, col_count)

    return row_count, col_count, count_by_symbol


def mark_board_under_attack_cells(board, row_count, col_count, symbol='.'):
    """
    fill the empty cells that are under attack by other cells,
    with given symbol
    return a new board dict
    """
    new_board = {}
    for row_num in range(row_count):
        for col_num in range(col_count):
            try:
                new_board[(row_num, col_num)] = board[(row_num, col_num)]
            except KeyError:
                if ChessPiece.pos_attacked_by_board(row_num, col_num, board):
                    new_board[(row_num, col_num)] = symbol
    return new_board


def show_all_confs(under_attack_symbol=''):
    """
    ask the board size and pieces count
    calculate and show all possible unique configuration
    """
    row_count, col_count, count_by_symbol = input_problem()
    print('Found Configurations:\n')
    for board in find_solutions_s(row_count, col_count, count_by_symbol):
        if under_attack_symbol:
            board = mark_board_under_attack_cells(
                board,
                row_count,
                col_count,
                under_attack_symbol,
            )
        print(format_board(board, row_count, col_count))
        input('Press enter to see the next')


def test_input_int():
    """test `input_int` function"""
    print(input_int('Enter an integer: '))
    print(input_int('Enter an integer (default=0): ', default=0))
    print(input_int('Enter an integer (>= 3): ', minimum=3))
    print(input_int('Enter an integer (<= 9): ', maximum=9))
    print(input_int(
        'Enter a number (0-99, default 40):',
        default=40,
        minimum=0,
        maximum=99,
    ))


def test_input_pieces_count(row_count, col_count):
    """test `input_pieces_count` function"""
    count_by_symbol = input_pieces_count(row_count, col_count)
    assert set(count_by_symbol.keys()) == \
        set(ChessPiece.class_by_symbol.keys())
    for count in count_by_symbol.values():
        assert isinstance(count, int)
        assert count >= 0

    assert sum(count_by_symbol.values()) <= row_count * col_count

    for symbol, count in count_by_symbol.items():
        print('%s: %s' % (symbol, count))


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


def compare_find_solutions_result():
    """
    run and compare the result of 3 implementations of find_solutions
    make sure they all return the same set of configurations
    with no duplicates
    """
    row_count, col_count, count_by_symbol = input_problem()

    solution_set_list = []
    # solution_set_list is a list of sets, one set for each implementation

    func_list = (
        find_solutions_r,
        find_solutions_q,
        find_solutions_s,
    )

    for func in func_list:  # pylint!
        solution_set = set()
        for board in func(row_count, col_count, count_by_symbol):
            board_tuple = tuple(sorted(board.items()))
            assert board_tuple not in solution_set
            solution_set.add(board_tuple)
        solution_set_list.append(solution_set)
        print('Number of solutions: %s  (%s)' % (len(solution_set), func))

    assert solution_set_list[1:] == solution_set_list[:-1]  # all items equal


def compare_find_solutions_time():
    """
    run and compare the running time of 3 implementations of find_solutions
    """

    row_count, col_count, count_by_symbol = input_problem()

    time_list = []

    func_list = (
        find_solutions_s,
        find_solutions_r,
        find_solutions_q,
        find_solutions_s,
        find_solutions_r,
        find_solutions_q,
    )

    for func in func_list:  # pylint!
        tm0 = now()
        for _ in func(row_count, col_count, count_by_symbol):
            pass
        delta = now() - tm0
        time_list.append(delta)
        print('%.4f seconds   (%s)' % (delta, func))


def chess_challenge_no_input():
    """
    solves the probem for the exact parameters given in the challange
    prints out the number of unique configuration, and running time
    """
    row_count = 7
    col_count = 7
    count_by_symbol = {
        'K': 2,
        'Q': 2,
        'B': 2,
        'R': 0,
        'N': 1,
    }

    count = 0
    tm0 = now()
    count = sum(1 for _ in find_solutions_s(
        row_count,
        col_count,
        count_by_symbol,
    ))
    delta = now() - tm0

    print('Number of Unique Configurations: %s' % solution_count)
    print('Running Time: %.4f seconds' % delta)




if __name__ == '__main__':
    show_all_confs()
    #  chess_challenge_no_input()
