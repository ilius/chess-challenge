#!/usr/bin/env python3

from pieces import ChessPiece


def get_board_int_value(board, row_count, col_count):
    """
    return an integer representation of board
    can be used for checking order and/or uniqueness of boards
    """
    symbol_count = len(ChessPiece.class_list)
    cell_count = row_count * col_count
    value = 0
    for (row_num, col_num), symbol in board.items():
        cell_ord = cell_count - (row_num * col_count + col_num)
        cell_value = (symbol_count + 1) ** cell_ord
        symbol_value = symbol_count - ChessPiece.class_by_symbol[symbol].cid
        #  assert 1 <= symbol_value <= symbol_count
        value += cell_value * symbol_value
    return value


def check_board_gen_order_uniqueness(board_iter, row_count, col_count):
    """
    check the order and uniqueness of a board iterator
    the integer value of board must decrease in each step of iteration
    """
    last_value = None
    for board in board_iter:
        value = get_board_int_value(board, row_count, col_count)
        if last_value and value >= last_value:
            return False
        last_value = value
    return True
