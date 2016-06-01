#!/usr/bin/env python3

from units import Unit

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


def test_inputUnitsCount(rowCount, colCount):
    countBySymbol = inputUnitsCount(rowCount, colCount)
    assert set(countBySymbol.keys()) == set(Unit.classBySymbol.keys())
    for count in countBySymbol.values():
        assert isinstance(count, int)
        assert count >= 0

    assert sum(countBySymbol.values()) <= rowCount * colCount

    for symbol, count in countBySymbol.items():
        print('%s: %s'%(symbol, count))




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

if __name__ == '__main__':
    #test_inputInt()
    test_inputUnitsCount(5, 6)
