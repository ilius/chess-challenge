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

    def __init__(self, rowNum, colNum):
        """
            rowNum: row number, starting from 0
            colNum: column number, starting from 0
        """
        self.move(rowNum, colNum)
    
    def move(self, rowNum, colNum):
        """
            rowNum: row number, starting from 0
            colNum: column number, starting from 0
            
            moves the unit to the position
        """
        self.rowNum = rowNum
        self.colNum = colNum


    def getPos(self):
        """
            returns the current position as tuple (col, row)
        """
        return (self.rowNum, self.colNum)

    def canAttackPos(self, rowNum, colNum):
        raise NotImplementedError

    canAttackUnit = lambda self, other: self.canAttackPos(other.rowNum, other.colNum)




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

    canAttackPos = lambda self, rowNum, colNum: 1 == max(
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

    canAttackPos = lambda self, rowNum, colNum: \
        rowNum == self.rowNum or colNum == self.colNum or \
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

    canAttackPos = lambda self, rowNum, colNum: \
        abs(rowNum - self.rowNum) == abs(colNum - self.colNum)


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

    canAttackPos = lambda self, rowNum, colNum: \
        rowNum == self.rowNum or colNum == self.colNum


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
    
    canAttackPos = lambda self, rowNum, colNum: \
        {1, 2} == {
            abs(rowNum - self.rowNum),
            abs(colNum - self.colNum),
        }





if __name__=='__main__':
    from pprint import pprint, pformat
    print('classByName = %s'%pformat(Unit.classByName))
    print('classBySymbol = %s'%pformat(Unit.classBySymbol))
    





