
class Unit(object):
    name = ''
    moveSteps = ()
    moveMaxLength = 1


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
    













