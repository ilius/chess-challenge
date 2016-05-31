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
    ## `todo` is a stack (we use .append, and .pop), each item is a tuple of (board, stage)
    ## where `board` is a dict of {(rowNum, colNum) => unitSymbol}
    ## and `stage` is a tuple containing count or each unit type
    ## stage == (kingCount, queenCount, bishopCount, rookCount, knightCount)
    stage = (
        symbolsCount.get(cls.symbol, 0)
        for cls in Unit.classList
    )
    todo = [(
        {}, ## initial board
        stage,## initial stage
    )]
    
    while todo:## stack not empty
        board, stage = todo.pop()
        
        for unitId, count in enumerate(stage):
            if not count:
                continue
            unitCls = Unit.classList[unitId]
            for rowNum in range(rowCount):
                for colNum in range(colCount):
                    if (rowNum, colNum) in board:
                        continue
                    unit = unitCls(rowNum, colNum)
                    if not unit.canPutOnBoard(board):
                        continue
                    
                    newBoard = board.copy()
                    newBoard[(rowNum, colNum)] = unit.symbol
                    
                    newStage = list(stage)
                    newStage[unitId] -= 1
                    assert newStage[unitId] >= 0

                    if not any(newStage):## newStage is empty, newBoard is complete
                        yield newBoard

                    
                    todo.append((newBoard, tuple(newStage)))
            
    
    


