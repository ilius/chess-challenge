#!/usr/bin/env python3
"""defines classes for different types of chess pieces"""


class ChessPiece(object):
    """base class for chess piece / piece type
    should not be instanciated directly
    """
    name = ''
    symbol = ''
    cid = None
    class_by_name = {}
    class_by_symbol = {}
    class_list = []

    @classmethod
    def register_class(cls, sub):
        """
        registers a ChessPiece subclass
        """
        cls.class_by_name[sub.name] = sub
        cls.class_by_symbol[sub.symbol] = sub

        sub.cid = len(cls.class_list)
        cls.class_list.append(sub)

        return sub

    def __init__(self, row_num, col_num):
        """
        row_num: row number, starting from 0
        col_num: column number, starting from 0
        """
        self.set_pos(row_num, col_num)

    def set_pos(self, row_num, col_num):
        """set position of piece

        row_num: row number, starting from 0
        col_num: column number, starting from 0
        """
        self.row_num = row_num
        self.col_num = col_num

    def get_pos(self):
        """return the current position as tuple (col, row)"""
        return (self.row_num, self.col_num)

    def attacks_pos(self, row_num, col_num):
        """check if this piece can attck (threatens) the given position"""
        raise NotImplementedError

    def attacks_piece(self, other):
        """check if this piece can attck (threatens) the given piece object"""
        return self.attacks_pos(other.row_num, other.col_num)

    def attacks_board(self, board):
        """check if this piece can attck (threatens) any piece on board
            return True if it can, False otherwise

        board: a dict { (row_num, col_num) => piece_symbol }
        """
        for row_num, col_num in board.keys():
            if self.attacks_pos(row_num, col_num):
                return True

        return False

    @classmethod
    def pos_attacked_by_board(cls, row_num, col_num, board):
        """
        check if any piece on given `board` can attck (threatens) the given
        position (row_num, col_num)
        """
        for (brow_num, bcol_num), symbol in board.items():
            if cls.class_by_symbol[symbol](brow_num, bcol_num)\
            .attacks_pos(row_num, col_num):
                return True

        return False


@ChessPiece.register_class
class King(ChessPiece):
    """King piece/piece class"""
    name = 'king'
    symbol = 'K'

    def attacks_pos(self, row_num, col_num):
        return max(
            abs(row_num - self.row_num),
            abs(col_num - self.col_num),
        ) == 1


@ChessPiece.register_class
class Queen(ChessPiece):
    """Queen piece/piece class"""
    name = 'queen'
    symbol = 'Q'

    def attacks_pos(self, row_num, col_num):
        drow = row_num - self.row_num
        dcol = col_num - self.col_num
        return drow is 0 or dcol is 0 or \
               abs(drow) == abs(dcol)


@ChessPiece.register_class
class Bishop(ChessPiece):
    """Bishop piece/piece class"""
    name = 'bishop'
    symbol = 'B'

    def attacks_pos(self, row_num, col_num):
        return abs(row_num - self.row_num) == abs(col_num - self.col_num)


@ChessPiece.register_class
class Rook(ChessPiece):
    """Rook piece/piece class"""
    name = 'rook'
    symbol = 'R'

    def attacks_pos(self, row_num, col_num):
        return row_num == self.row_num or col_num == self.col_num


@ChessPiece.register_class
class Knight(ChessPiece):
    """Knight piece/piece class"""
    name = 'knight'
    symbol = 'N'

    def attacks_pos(self, row_num, col_num):
        return {1, 2} == {
            abs(row_num - self.row_num),
            abs(col_num - self.col_num),
        }
