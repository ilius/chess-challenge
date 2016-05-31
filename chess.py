#!/usr/bin/env python3


class Unit(object):
    name = ''
    symbol = ''
    moveSteps = ()
    moveMaxLength = 1
    classByName = {}
    classBySymbol = {}

    @classmethod
    def registerClass(myCls, cls):
        myCls.classByName[cls.name] = cls
        myCls.classBySymbol[cls.symbol] = cls

    def __init__(self, colNum, rowNum):
        """
            colNum: column number, starting from 0
            rowNum: row number, starting from 0
        """
        self.move(colNum, rowNum)
    
    def move(self, colNum, rowNum):
        """
            colNum: column number, starting from 0
            rowNum: row number, starting from 0
            
            moves the unit to the position
        """
        self.colNum = colNum
        self.rowNum = rowNum

    def getPos(self):
        """
            returns the current position as tuple (col, row)
        """
        return (self.colNum, self.rowNum)

    def canAttackPos(self, colNum, rowNum):
        raise NotImplementedError

    canAttackUnit = lambda self, other: self.canAttackPos(other.colNum, other.rowNum)




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

    canAttackPos = lambda self, colNum, rowNum: 1 == max(
        abs(colNum - self.colNum),
        abs(rowNum - self.rowNum),
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

    canAttackPos = lambda self, colNum, rowNum: \
        colNum == self.colNum or rowNum == self.rowNum or \
        abs(colNum - self.colNum) == abs(rowNum - self.rowNum)



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

    canAttackPos = lambda self, colNum, rowNum: \
        abs(colNum - self.colNum) == abs(rowNum - self.rowNum)


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

    canAttackPos = lambda self, colNum, rowNum: \
        colNum == self.colNum or rowNum == self.rowNum


@Unit.registerClass
class Knight(Unit):
    name = 'knight'
    symbol = 'K'
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
    
    canAttackPos = lambda self, colNum, rowNum: \
        {1, 2} == {
            abs(colNum - self.colNum),
            abs(rowNum - self.rowNum),
        }





if __name__=='__main__':
    from pprint import pprint, pformat
    print('classByName = %s'%pformat(Unit.classByName))
    print('classBySymbol = %s'%pformat(Unit.classBySymbol))
    





