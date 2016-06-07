"""
contains some chess-related utility functions to use in command line
"""

from pieces import ChessPiece
from cmd_util import input_int

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


# ______________________ Test Functions ______________________ #


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

if __name__ == '__main__':
    test_input_pieces_count(7, 7)
