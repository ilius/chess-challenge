#!/usr/bin/env python3
from units import Unit


def findSolutions(rowCount, colCount, symbolsCount):
    """
        rowCount: int, number or rows
        colCount: int, number of columns
        symbolsCount: dict of { unitSymbol => count }
        
        this is a generator, yields a completed `board` each time
        where `board` is a dict of {(rowNum, colNum) => unitSymbol}
    """
    # `todo` is a stack (we use .append, and .pop), each item is a tuple of (board, stage, cellNum)
    #   `board` is a dict of {(rowNum, colNum) => unitSymbol}
    #   `stage` is a tuple containing count or each unit type
    #       stage == (kingCount, queenCount, bishopCount, rookCount, knightCount)
    #   `cellNum` is an int resulting from `rowNum * colCount + colNum`
    #       representing the next cell that we want to check
    #       and we don't want any unit to put before this cell on the current board
    #       this way we avoid giving duplicate solutions and extra computation
    #       To decode cellNum: rowNum, colNum = divmod(cellNum, colCount)
    cellCount = rowCount * colCount
    stage = (
        symbolsCount.get(cls.symbol, 0)
        for cls in Unit.classList
    )
    todo = [(
        {}, # initial board
        stage, # initial stage
        0, # first cell (top-left corner)
    )]
    
    while todo: # stack not empty
        board, stage, startCellNum = todo.pop()
        stageSize = sum(stage)

        if startCellNum < cellCount - stageSize:
            # we can leave cell empty, skip to next one
            todo.append((
                board,
                stage,
                startCellNum + 1,
            ))

        for cellNum in range(startCellNum, cellCount):
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

                if not any(newStage): # newStage is empty, newBoard is complete
                    yield newBoard

                if cellNum < cellCount - 1:
                    todo.append((
                        newBoard,
                        tuple(newStage),
                        cellNum + 1,
                    ))
            
    
    





