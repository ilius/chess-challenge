#!/usr/bin/env python3
"""responsible for calling other modules and interacting with user"""

import sys
from time import time as now
import random

from units import Unit
from solution import (
    find_solutions_s,
    find_solutions_r,
    find_solutions_q,
)


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


def input_units_count(row_count, col_count):
    """
    ask the user the number or chess units / pieces of each type
    return a dict { unit_symbol => count }

    row_count: number of rows
    col_count: number of columns
    """
    cell_count = row_count * col_count
    count_by_symbol = {}
    total_count = 0
    for cls in Unit.class_list:
        plural_name = cls.name.capitalize() + 's'
        count = input_int(
            'Number of %s: ' % plural_name,
            default=0,
            minimum=0,
            maximum=cell_count-total_count,
        )
        count_by_symbol[cls.symbol] = count
        total_count += count
    return count_by_symbol


def format_board(board, row_count, col_count):
    """
    convert a `board` into string than can be shown in console

    board: a dict { (row_num, col_num) => unit_symbol }
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
            index = int(factor * len(Unit.class_list))
            board[(row_num, col_num)] = Unit.class_list[index].symbol
    return board


def input_problem():
    """
    get the board size and units count from stdin or command line arguments
    """
    if len(sys.argv) == 3 + len(Unit.class_list):
        row_count = int(sys.argv[1])
        col_count = int(sys.argv[2])
        count_by_symbol = {}
        print('Number of rows: %s' % row_count)
        print('Number of columns: %s' % col_count)
        print()
        for index, cls in enumerate(Unit.class_list):
            count_by_symbol[cls.symbol] = int(sys.argv[3+index])
            print('Number of %ss: %s' % (
                cls.name.capitalize(),
                count_by_symbol[cls.symbol],
            ))
    else:
        row_count = input_int('Number of rows: ', minimum=2)
        col_count = input_int('Number of columns: ', minimum=2)
        print()
        count_by_symbol = input_units_count(row_count, col_count)

    return row_count, col_count, count_by_symbol


def main():
    """
    ask the board size and units count
    calculate and show all possible unique configuration
    """
    row_count, col_count, count_by_symbol = input_problem()
    print('Found Configurations:\n')
    for board in find_solutions_s(row_count, col_count, count_by_symbol):
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


def test_input_units_count(row_count, col_count):
    """test `input_units_count` function"""
    count_by_symbol = input_units_count(row_count, col_count)
    assert set(count_by_symbol.keys()) == set(Unit.class_by_symbol.keys())
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

    for func in func_list:#  pylint!
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

    for func in func_list:#  pylint!
        tm0 = now()
        for _ in func(row_count, col_count, count_by_symbol):
            pass
        delta = now() - tm0
        time_list.append(delta)
        print('%.4f seconds   (%s)' % (delta, func))

if __name__ == '__main__':
    # test_input_int()
    # test_input_units_count(5, 6)
    # test_format_random_board(density=0.5)
    # compare_find_solutions_time()
    # compare_find_solutions_result()
    main()
