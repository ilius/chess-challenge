#!/usr/bin/env python3
"""contains utility functions for a command line interface"""

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


def input_yesno(prompt, default=None):
    """
    ask the user to enter Yes or No

    prompt: string to be shown as prompt
    default: True (=Yes), False (=No), or None (can not leave empty)
    """
    while True:
        value = input(prompt).strip()
        if not value:
            if default is None:
                print('Can not leave empty')
                continue
            else:
                return default
        value = value.lower()
        if value in ('y', 'yes'):
            return True

        if value in ('n', 'no'):
            return False

        print('Enter Yes or No')


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


if __name__ == '__main__':
    test_input_int()
