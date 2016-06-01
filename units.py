#!/usr/bin/env python3


class Unit(object):
    name = ''
    symbol = ''
    id = None
    moveSteps = ()
    moveMaxLength = 1
    classByName = {}
    classBySymbol = {}
    classList = []

    @classmethod
    def registerClass(myCls, cls):
        myCls.classByName[cls.name] = cls
        myCls.classBySymbol[cls.symbol] = cls

        cls.id = len(myCls.classList)
        myCls.classList.append(cls)

    def __init__(self, rowNum, colNum):
        """
        rowNum: row number, starting from 0
        colNum: column number, starting from 0
        """
        self.setPos(rowNum, colNum)

    def setPos(self, rowNum, colNum):
        """set position of unit

        rowNum: row number, starting from 0
        colNum: column number, starting from 0
        """
        self.rowNum = rowNum
        self.colNum = colNum

    def getPos(self):
        """return the current position as tuple (col, row)"""
        return (self.rowNum, self.colNum)

    def attacksPos(self, rowNum, colNum):
        raise NotImplementedError

    def attacksUnit(self, other):
        return self.attacksPos(other.rowNum, other.colNum)

    def attacksBoard(self, board):
        """check if this unit can attck (threatens) any unit on board
            return True if it can, False otherwise

        board: a dict { (rowNum, colNum) => unitSymbol }
        """
        for rowNum, colNum in board.keys():
            if self.attacksPos(rowNum, colNum):
                return True

        return False

    @classmethod
    def posAttckedByBoard(cls, rowNum, colNum, board):
        for (bRowNum, bColNum), symbol in board.items():
            other = cls.classBySymbol[symbol](bRowNum, bColNum)
            if other.attacksPos(rowNum, colNum):
                return True

        return False

    def canPutOnBoard(self, board):
        """check if this unit can be added to the board without threatening
            or being threatened by any unit on board
            return True if it can, False otherwise

        board: a dict { (rowNum, colNum) => unitSymbol }
            we use dict instead of 2-dimentional array bcoz the number of units
            on board is probably small comparing to the whole table (N*M)
            should we use numpy matrix? FIXME
        """
        for (rowNum, colNum), symbol in board.items():
            if self.attacksPos(rowNum, colNum):
                return False

            other = self.classBySymbol[symbol](rowNum, colNum)
            if other.attacksUnit(self):
                return False

        return True


@Unit.registerClass
class King(Unit):
    name = 'king'
    symbol = 'K'
    moveSteps = (
        (-1, -1),
        (-1, 0),
        (-1, 1),
        (0, -1),
        (0, 1),
        (1, -1),
        (1, 0),
        (1, 1),
    )
    moveMaxLength = 1

    def attacksPos(self, rowNum, colNum):
        return 1 == max(
            abs(rowNum - self.rowNum),
            abs(colNum - self.colNum),
        )


@Unit.registerClass
class Queen(Unit):
    name = 'queen'
    symbol = 'Q'
    moveSteps = (
        (-1, -1),
        (-1, 0),
        (-1, 1),
        (0, -1),
        (0, 1),
        (1, -1),
        (1, 0),
        (1, 1),
    )
    moveMaxLength = -1

    def attacksPos(self, rowNum, colNum):
        return rowNum == self.rowNum or colNum == self.colNum or \
            abs(rowNum - self.rowNum) == abs(colNum - self.colNum)


@Unit.registerClass
class Bishop(Unit):
    name = 'bishop'
    symbol = 'B'
    moveSteps = (
        (-1, -1),
        (-1, 1),
        (1, -1),
        (1, 1),
    )
    moveMaxLength = -1

    def attacksPos(self, rowNum, colNum):
        return abs(rowNum - self.rowNum) == abs(colNum - self.colNum)


@Unit.registerClass
class Rook(Unit):
    name = 'rook'
    symbol = 'R'
    moveSteps = (
        (-1, 0),
        (0, -1),
        (0, 1),
        (1, 0),
    )
    moveMaxLength = -1

    def attacksPos(self, rowNum, colNum):
        return rowNum == self.rowNum or colNum == self.colNum


@Unit.registerClass
class Knight(Unit):
    name = 'knight'
    symbol = 'N'
    moveSteps = (
        (-2, -1),
        (-2, 1),
        (-1, -2),
        (-1, 2),
        (1, -2),
        (1, 2),
        (2, -1),
        (2, 1),
    )
    moveMaxLength = 1

    def attacksPos(self, rowNum, colNum):
        return {1, 2} == {
            abs(rowNum - self.rowNum),
            abs(colNum - self.colNum),
        }


if __name__ == '__main__':
    from pprint import pprint, pformat
    print('classByName = %s' % pformat(Unit.classByName))
    print('classBySymbol = %s' % pformat(Unit.classBySymbol))
