#!/usr/bin/env python3
"""responsible for calling other modules and interacting with user"""

import sys
from time import time as now
import argparse
import random

from pieces import ChessPiece
from solution import (
    find_solutions_s,
    find_solutions_r,
    find_solutions_q,
)
from cmd_util import (
    input_int,
    input_yesno,
)

PIECE_SYMBOLS = 'KQBRN'  # must not re-order


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
    get the board size and pieces count from stdin
    """
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


def count_or_show_by_generator(gen, count_enable, row_count, col_count):
    """
    gen: a generator returned by find_solutions_*
    count_enable: bool, only count solutions/configurations, don't show them
    """
    if count_enable:
        print('Calculating, please wait... (Control+C to cancel)')
        tm0 = now()
        try:
            solution_count = sum(1 for _ in gen)
        except KeyboardInterrupt:
            print('\nGoodbye')
            return
        delta = now() - tm0
        print('Number of Unique Configurations: %s' % solution_count)
        print('Running Time: %.4f seconds' % delta)
    else:
        print('Found Configurations:\n')
        for board in gen:
            print(format_board(board, row_count, col_count))
            try:
                input('Press Enter to see the next, Control+C to exit')
            except KeyboardInterrupt:
                print('\nGoodbye')
                break


def interactive_main(under_attack_symbol=''):
    """
    ask the board size and pieces count
    calculate and show all possible unique configurations
    or just count unique configurations depending on user input
    """
    row_count, col_count, count_by_symbol = input_problem()
    count_enable = input_yesno(
        'Count configurations? [Yes/No] ',
        default=True,
    )
    gen = find_solutions_s(
        row_count,
        col_count,
        count_by_symbol,
    )
    count_or_show_by_generator(
        gen,
        count_enable,
        row_count,
        col_count,
    )

def argparse_main():
    parser = argparse.ArgumentParser(add_help=True)
    parser.add_argument(
        action='store',
        dest='row_count',
        type=int,
        help='number of rows in the board',
    )
    parser.add_argument(
        action='store',
        dest='col_count',
        type=int,
        help='number of columns in the board',
    )
    parser.add_argument(
        '-c',
        '--count',
        dest='count_enable',
        action='store_true',
        default=False,
        help='only count the number of unique configurations, don\'t show them',
    )

    for cls in ChessPiece.class_list:
        plural_name = cls.name + 's'
        parser.add_argument(
            '-' + cls.symbol.lower(),
            '--' + plural_name,
            dest=cls.name,
            type=int,
            default=0,
            help='number of %s'%plural_name
        )

    args = parser.parse_args()

    count_by_symbol = {
        cls.symbol: getattr(args, cls.name, 0)
        for cls in ChessPiece.class_list
    }

    gen = find_solutions_s(
        args.row_count,
        args.col_count,
        count_by_symbol,
    )
    count_or_show_by_generator(
        gen,
        args.count_enable,
        args.row_count,
        args.col_count,
    )


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
    if len(sys.argv) > 1:
        argparse_main()
    else:
        interactive_main()
    #  chess_challenge_no_input()
