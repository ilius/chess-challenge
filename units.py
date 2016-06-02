#!/usr/bin/env python3
"""defines classes for different types of chess units / pieces"""


class Unit(object):
    """base class for chess unit / piece type
    should not be instanciated directly
    """
    name = ''
    symbol = ''
    cid = None
    move_steps = ()
    move_max_length = 1
    class_by_name = {}
    class_by_symbol = {}
    class_list = []

    @classmethod
    def register_class(cls, sub):
        """
        registers a Unit subclass
        """
        cls.class_by_name[sub.name] = sub
        cls.class_by_symbol[sub.symbol] = sub

        sub.cid = len(cls.class_list)
        cls.class_list.append(sub)

    def __init__(self, row_num, col_num):
        """
        row_num: row number, starting from 0
        col_num: column number, starting from 0
        """
        self.set_pos(row_num, col_num)

    def set_pos(self, row_num, col_num):
        """set position of unit

        row_num: row number, starting from 0
        col_num: column number, starting from 0
        """
        self.row_num = row_num
        self.col_num = col_num

    def get_pos(self):
        """return the current position as tuple (col, row)"""
        return (self.row_num, self.col_num)

    def attacks_pos(self, row_num, col_num):
        """check if this unit can attck (threatens) the given position"""
        raise NotImplementedError

    def attacks_unit(self, other):
        """check if this unit can attck (threatens) the given unit object"""
        return self.attacks_pos(other.row_num, other.col_num)

    def attacks_board(self, board):
        """check if this unit can attck (threatens) any unit on board
            return True if it can, False otherwise

        board: a dict { (row_num, col_num) => unitSymbol }
        """
        for row_num, col_num in board.keys():
            if self.attacks_pos(row_num, col_num):
                return True

        return False

    @classmethod
    def pos_attacked_by_board(cls, row_num, col_num, board):
        """
        check if any unit on given `board` can attck (threatens) the given
        position (row_num, col_num)
        """
        for (brow_num, bcol_num), symbol in board.items():
            other = cls.class_by_symbol[symbol](brow_num, bcol_num)
            if other.attacks_pos(row_num, col_num):
                return True

        return False


@Unit.register_class
class King(Unit):
    """King unit/piece class"""
    name = 'king'
    symbol = 'K'
    move_steps = (
        (-1, -1),
        (-1, 0),
        (-1, 1),
        (0, -1),
        (0, 1),
        (1, -1),
        (1, 0),
        (1, 1),
    )
    move_max_length = 1

    def attacks_pos(self, row_num, col_num):
        return max(
            abs(row_num - self.row_num),
            abs(col_num - self.col_num),
        ) == 1


@Unit.register_class
class Queen(Unit):
    """Queen unit/piece class"""
    name = 'queen'
    symbol = 'Q'
    move_steps = (
        (-1, -1),
        (-1, 0),
        (-1, 1),
        (0, -1),
        (0, 1),
        (1, -1),
        (1, 0),
        (1, 1),
    )
    move_max_length = -1

    def attacks_pos(self, row_num, col_num):
        return row_num == self.row_num or col_num == self.col_num or \
            abs(row_num - self.row_num) == abs(col_num - self.col_num)


@Unit.register_class
class Bishop(Unit):
    """Bishop unit/piece class"""
    name = 'bishop'
    symbol = 'B'
    move_steps = (
        (-1, -1),
        (-1, 1),
        (1, -1),
        (1, 1),
    )
    move_max_length = -1

    def attacks_pos(self, row_num, col_num):
        return abs(row_num - self.row_num) == abs(col_num - self.col_num)


@Unit.register_class
class Rook(Unit):
    """Rook unit/piece class"""
    name = 'rook'
    symbol = 'R'
    move_steps = (
        (-1, 0),
        (0, -1),
        (0, 1),
        (1, 0),
    )
    move_max_length = -1

    def attacks_pos(self, row_num, col_num):
        return row_num == self.row_num or col_num == self.col_num


@Unit.register_class
class Knight(Unit):
    """Knight unit/piece class"""
    name = 'knight'
    symbol = 'N'
    move_steps = (
        (-2, -1),
        (-2, 1),
        (-1, -2),
        (-1, 2),
        (1, -2),
        (1, 2),
        (2, -1),
        (2, 1),
    )
    move_max_length = 1

    def attacks_pos(self, row_num, col_num):
        return {1, 2} == {
            abs(row_num - self.row_num),
            abs(col_num - self.col_num),
        }
