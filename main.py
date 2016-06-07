#!/usr/bin/env python3
"""
responsible for calling other modules and interacting with user
To solve the challenge problem, run:
    ./main.py --count 7 7 -k2 -q2 -b2 -n1
"""

import sys
from time import time as now
import argparse

from pieces import ChessPiece
from solution import (
    find_solutions_s,
    find_solutions_r,
    find_solutions_q,
)
from chess_util import format_board
from cmd_util import input_yesno
from cmd_chess_util import input_problem


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


def interactive_main():
    """
    ask the board size and pieces count
    calculate and show all possible unique configurations
    or just count unique configurations depending on user input
    """
    row_count, col_count, count_by_symbol = input_problem()
    count_enable = input_yesno(
        'Count configurations? [Yes/No] ',
        default=False,
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
    """
    parses the command line arguments and options, and performs operations
    """
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
        help='only count the number of unique configurations, '
             'don\'t show them',
    )

    for cls in ChessPiece.class_list:
        plural_name = cls.name + 's'
        parser.add_argument(
            '-' + cls.symbol.lower(),
            '--' + plural_name,
            dest=cls.name,
            type=int,
            default=0,
            help='number of %s' % plural_name
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

# ______________________ Test Functions ______________________ #


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


if __name__ == '__main__':
    if len(sys.argv) > 1:
        argparse_main()
    else:
        interactive_main()
