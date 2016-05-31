

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

    def __init__(self, col, row):
        """
            col: column index, starting from 0
            row: row index, starting from 0
        """
        self.move(col, row)
    
    def move(self, col, row):
        """
            col: column index, starting from 0
            row: row index, starting from 0
            
            moves the unit to the position
        """
        self.col = col
        self.row = row

    def getPos(self):
        """
            returns the current position as tuple (col, row)
        """
        return (self.col, self.row)

    def canAttackPos(self, col, row):
        raise NotImplementedError

    canAttackUnit = lambda self, other: self.canAttackPos(other.col, other.row)

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

    canAttackPos = lambda self, col, row: 1 == max(
        abs(col - self.col),
        abs(row - self.row),
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

    canAttackPos = lambda self, col, row: \
        col == self.col or row == self.row or \
        abs(col - self.col) == abs(row - self.row)



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

    canAttackPos = lambda self, col, row: \
        abs(col - self.col) == abs(row - self.row)


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

    canAttackPos = lambda self, col, row: \
        col == self.col or row == self.row


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
    
    canAttackPos = lambda self, col, row: \
        {1, 2} == {
            abs(col - self.col),
            abs(row - self.row),
        }





if __name__=='__main__':
    from pprint import pprint
    pprint(Unit.classByName)
    pprint(Unit.classBySymbol)
    





