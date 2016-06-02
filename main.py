#!/usr/bin/env python3

import sys

from units import Unit
from solution import find_solutions_s as find_solutions


def input_int(prompt, default=None, minimum=None, maximum=None):
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
    import random
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
    row_count, col_count, count_by_symbol = input_problem()
    print('Found Configurations:\n')
    for board in find_solutions(row_count, col_count, count_by_symbol):
        print(format_board(board, row_count, col_count))
        input('Press enter to see the next')


def test_input_int():
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
    count_by_symbol = input_units_count(row_count, col_count)
    assert set(count_by_symbol.keys()) == set(Unit.class_by_symbol.keys())
    for count in count_by_symbol.values():
        assert isinstance(count, int)
        assert count >= 0

    assert sum(count_by_symbol.values()) <= row_count * col_count

    for symbol, count in count_by_symbol.items():
        print('%s: %s' % (symbol, count))


def test_format_random_board(density=0.5):
    while True:
        row_count = input_int('Number of rows: ', minimum=2, default=0)
        if row_count == 0:
            break
        col_count = input_int('Number of columns: ', minimum=2)
        board = make_random_board(row_count, col_count, density)
        print(format_board(board, row_count, col_count))
        print('\n\n')


def compare_find_solutions_result():
    from solution import find_solutions_s, find_solutions_r, find_solutions_q
    row_count, col_count, count_by_symbol = input_problem()

    solution_set_list = []
    # solution_set_list is a list of sets, one set for each implementation
    for func in (
        find_solutions_r,
        find_solutions_q,
        find_solutions_s,
    ):
        solution_set = set()
        for board in func(row_count, col_count, count_by_symbol):
            board_tuple = tuple(sorted(board.items()))
            assert board_tuple not in solution_set
            solution_set.add(board_tuple)
        solution_set_list.append(solution_set)
        print('Number of solutions: %s  (%s)' % (len(solution_set), func))

    assert solution_set_list[1:] == solution_set_list[:-1]  # all items equal


def compare_find_solutions_time():
    from time import time
    from solution import find_solutions_s, find_solutions_r, find_solutions_q

    row_count, col_count, count_by_symbol = input_problem()

    time_list = []

    for func in (
        find_solutions_s,
        find_solutions_r,
        find_solutions_q,
        find_solutions_s,
        find_solutions_r,
        find_solutions_q,
    ):
        tm0 = time()
        for board in func(row_count, col_count, count_by_symbol):
            pass
        delta = time() - tm0
        time_list.append(delta)
        print('%.4f seconds   (%s)' % (delta, func))

if __name__ == '__main__':
    # test_input_int()
    # test_input_units_count(5, 6)
    # test_format_random_board(density=0.5)
    # compare_find_solutions_time()
    # compare_find_solutions_result()
    main()
