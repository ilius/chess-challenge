
class Unit(object):
    name = ''
    moveSteps = ()
    moveMaxLength = 1
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




class King(Unit):
    name = 'king'
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

class Queen(Unit):
    name = 'queen'
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

class Bishop(Unit):
    name = 'bishop'
    moveSteps = (
        (-1, -1),
        (-1, 1),
        (1, -1),
        (1, 1),
    )
    moveMaxLength = -1

class Rook(Unit):
    name = 'rook'
    moveSteps = (
        (-1, 0),
        (0, -1),
        (0, 1),
        (1, 0),
    )
    moveMaxLength = -1

class Knight(Unit):
    name = 'knight'
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
    













