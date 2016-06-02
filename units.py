#!/usr/bin/env python3

class Unit(object):
    name = ''
    symbol = ''
    id = None
    move_steps = ()
    move_max_length = 1
    class_by_name = {}
    class_by_symbol = {}
    class_list = []

    @classmethod
    def register_class(my_cls, cls):
        my_cls.class_by_name[cls.name] = cls
        my_cls.class_by_symbol[cls.symbol] = cls

        cls.id = len(my_cls.class_list)
        my_cls.class_list.append(cls)

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
        raise NotImplementedError

    def attacks_unit(self, other):
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
    def pos_attcked_by_board(cls, row_num, col_num, board):
        for (brow_num, bcol_num), symbol in board.items():
            other = cls.class_by_symbol[symbol](brow_num, bcol_num)
            if other.attacks_pos(row_num, col_num):
                return True

        return False

    def can_put_on_board(self, board):
        """check if this unit can be added to the board without threatening
            or being threatened by any unit on board
            return True if it can, False otherwise

        board: a dict { (row_num, col_num) => unitSymbol }
            we use dict instead of 2-dimentional array bcoz the number of units
            on board is probably small comparing to the whole table (N*M)
            should we use numpy matrix? FIXME
        """
        for (row_num, col_num), symbol in board.items():
            if self.attacks_pos(row_num, col_num):
                return False

            other = self.class_by_symbol[symbol](row_num, col_num)
            if other.attacks_unit(self):
                return False

        return True


@Unit.register_class
class King(Unit):
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
        return 1 == max(
            abs(row_num - self.row_num),
            abs(col_num - self.col_num),
        )


@Unit.register_class
class Queen(Unit):
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


if __name__ == '__main__':
    from pprint import pprint, pformat
    print('class_by_name = %s' % pformat(Unit.class_by_name))
    print('class_by_symbol = %s' % pformat(Unit.class_by_symbol))
