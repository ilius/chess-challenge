#!/usr/bin/env python3
from units import Unit


def findSolutions(rowCount, colCount, countBySymbol, debug=True):
    """find and iterate over solution boards
    
    rowCount: int, number or rows
    colCount: int, number of columns
    countBySymbol: dict of { unitSymbol => count }

    this is a generator, yields a completed `board` each time
    where `board` is a dict of {(rowNum, colNum) => unitSymbol}
    """
    # `todo` is a stack (we use .append, and .pop)
    # each item is a tuple of (board, stage, cellNum)
    #   `board` is a dict of {(rowNum, colNum) => unitSymbol}
    #   `stage` is a tuple containing count or each unit type:
    #       (kingCount, queenCount, bishopCount, rookCount, knightCount)
    #   `cellNum` is an int resulting from `rowNum * colCount + colNum`
    #       representing the next cell that we want to check
    #       and we don't want any unit to put before this cell on the current
    #       board, this way we avoid giving duplicate solutions and extra
    #       computation
    #       To decode cellNum: rowNum, colNum = divmod(cellNum, colCount)
    cellCount = rowCount * colCount
    stage = tuple(
        countBySymbol.get(cls.symbol, 0)
        for cls in Unit.classList
    )
    todo = [(
        {},     # initial board
        stage,  # initial stage
        0,      # first cell (top-left corner)
    )]

    while todo:  # stack not empty
        board, stage, cellNum = todo.pop()
        stageSize = sum(stage)

        if debug:
            print('len(todo)=%s, len(board)=%s, stage=%s, cellNum=%s'%(len(todo), len(board), str(stage), cellNum))

        if cellNum < cellCount - stageSize:
            # we can leave cell empty, skip to next one
            todo.append((
                board,
                stage,
                cellNum + 1,
            ))

        (rowNum, colNum) = cellPos = divmod(cellNum, colCount)
        for unitId, count in enumerate(stage):
            if not count:
                continue
            unitCls = Unit.classList[unitId]
            if cellPos in board:
                continue
            unit = unitCls(rowNum, colNum)
            if not unit.canPutOnBoard(board):
                continue

            newBoard = board.copy()
            newBoard[cellPos] = unit.symbol

            newStage = list(stage)
            newStage[unitId] -= 1
            assert newStage[unitId] >= 0

            if stageSize <= 1:  # newStage empty, newBoard complete
                yield newBoard
                continue

            if cellNum < cellCount - (stageSize - 1):
                todo.append((
                    newBoard,
                    tuple(newStage),
                    cellNum + 1,
                ))
