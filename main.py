#!/usr/bin/env python3

import sys

from units import Unit
from solution import findSolutions

def inputInt(prompt, default=None, minimum=None, maximum=None):
    while True:
        valueStr = input(prompt).strip()
        if not valueStr:
            if default is None:
                print('Can not leave empty')
                continue
            else:
                return default
        try:
            value = int(valueStr)
        except ValueError:
            print('Must enter an integer number')
            continue

        if minimum is not None and value < minimum:
            print('Must enter greater than or equal to %s'%minimum)
            continue

        if maximum is not None and value > maximum:
            print('Must enter less than or equal to %s'%maximum)
            continue

        return value

def inputUnitsCount(rowCount, colCount):
    cellCount = rowCount * colCount
    countBySymbol = {}
    totalCount = 0
    for cls in Unit.classList:
        pluralName = cls.name.capitalize() + 's'
        count = inputInt(
            'Number of %s: '%pluralName,
            default=0,
            minimum=0,
            maximum=cellCount-totalCount,
        )
        countBySymbol[cls.symbol] = count
        totalCount += count
    return countBySymbol

def formatBoard(board, rowCount, colCount):
    sepLine = '-' * (colCount * 4 + 1)
    lines = [sepLine]
    for rowNum in range(rowCount):
        lines.append(
            '| ' + ' | '.join([
                board.get((rowNum, colNum), ' ')
                for colNum in range(colCount)
            ]) + ' |'
        )
        lines.append(sepLine)
    return '\n'.join(lines)

def makeRandomBoard(rowCount, colCount, density=0.5):
    import random
    board = {}
    for rowNum in range(rowCount):
        for colNum in range(colCount):
            factor = random.random() / density
            if factor >= 1:
                continue
            index = int(factor * len(Unit.classList))
            board[(rowNum, colNum)] = Unit.classList[index].symbol
    return board

def inputProblem():
    if len(sys.argv) == 3 + len(Unit.classList):
        rowCount = int(sys.argv[1])
        colCount = int(sys.argv[2])
        countBySymbol = {}
        print('Number of rows: %s'%rowCount)
        print('Number of columns: %s'%colCount)
        print()
        for index, cls in enumerate(Unit.classList):
            countBySymbol[cls.symbol] = int(sys.argv[3+index])
            print('Number of %ss: %s'%(cls.name.capitalize(), countBySymbol[cls.symbol]))
    else:
        rowCount = inputInt('Number of rows: ', minimum=2)
        colCount = inputInt('Number of columns: ', minimum=2)
        print()
        countBySymbol = inputUnitsCount(rowCount, colCount)

    return rowCount, colCount, countBySymbol

def main():
    rowCount, colCount, countBySymbol = inputProblem()
    print('Found Configurations:\n')
    for board in findSolutions(rowCount, colCount, countBySymbol):
        print(formatBoard(board, rowCount, colCount))
        input('Press enter to see the next')


def test_inputInt():
    print(inputInt('Enter an integer: '))
    print(inputInt('Enter an integer (default=0): ', default=0))
    print(inputInt('Enter an integer (>= 3): ', minimum=3))
    print(inputInt('Enter an integer (<= 9): ', maximum=9))
    print(inputInt(
        'Enter a number (0-99, default 40):',
        default=40,
        minimum=0,
        maximum=99,
    ))

def test_inputUnitsCount(rowCount, colCount):
    countBySymbol = inputUnitsCount(rowCount, colCount)
    assert set(countBySymbol.keys()) == set(Unit.classBySymbol.keys())
    for count in countBySymbol.values():
        assert isinstance(count, int)
        assert count >= 0

    assert sum(countBySymbol.values()) <= rowCount * colCount

    for symbol, count in countBySymbol.items():
        print('%s: %s'%(symbol, count))

def test_formatRandomBoard(density=0.5):
    while True:
        rowCount = inputInt('Number of rows: ', minimum=2, default=0)
        if rowCount==0:
            break
        colCount = inputInt('Number of columns: ', minimum=2)
        board = makeRandomBoard(rowCount, colCount, density)
        print(formatBoard(board, rowCount, colCount))
        print('\n\n')


def test_findSolutions_compareOutput():
    from solution import findSolutions_S, findSolutions_R, findSolutions_Q
    rowCount, colCount, countBySymbol = inputProblem()

    solutionSetList = []
    # solutionSetList is a list of sets, one set for each implementation
    for func in (
        findSolutions_R,
        findSolutions_Q,
        findSolutions_S,
    ):
        solutionSet = set()
        for board in func(rowCount, colCount, countBySymbol):
            boardS = str(board)
            assert boardS not in solutionSet
            solutionSet.add(boardS)
        solutionSetList.append(solutionSet)

    assert solutionSetList[1:] == solutionSetList[:-1]  # all items equal
    print('Number of solutions: %s'%len(solutionSetList[0]))


def test_findSolutions_compareTime():
    from time import time
    from solution import findSolutions_S, findSolutions_R, findSolutions_Q

    rowCount, colCount, countBySymbol = inputProblem()

    timeList = []

    for func in (
        findSolutions_S,
        findSolutions_R,
        findSolutions_Q,
        findSolutions_S,
        findSolutions_R,
        findSolutions_Q,
    ):
        t0 = time()
        for board in func(rowCount, colCount, countBySymbol):
            pass
        delta = time() - t0
        timeList.append(delta)
        print('%.4f seconds'%delta)


    #print('Running time of implementations:')
    #for delta in timeList:
    #    print('%.4f seconds'%delta)



if __name__ == '__main__':
    #test_inputInt()
    #test_inputUnitsCount(5, 6)
    #test_formatRandomBoard(density=0.5)
    #test_findSolutions_compareTime()
    #test_findSolutions_compareOutput()
    main()
