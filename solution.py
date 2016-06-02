#!/usr/bin/env python3
"""
this module is responsible for finding and iterating over all unique possible
solutions / configurations by the given parameters
"""

import queue

from units import Unit


def find_solutions_s(row_count, col_count, count_by_symbol):
    """find and iterate over solution boards, implemented with Stack

    row_count: int, number or rows
    col_count: int, number of columns
    count_by_symbol: dict of { unitSymbol => count }

    this is a generator, yields a completed `board` each time
    where `board` is a dict of {(row_num, col_num) => unitSymbol}
    """
    # `todo` is a stack (we use .append, and .pop)
    # each item is a tuple of (board, stage, cell_num)
    #   `board` is a dict of {(row_num, col_num) => unitSymbol}
    #   `stage` is a tuple containing count or each unit type:
    #       (king_count, queen_count, bishop_count, rook_count, knight_count)
    #   `cell_num` is an int resulting from `row_num * col_count + col_num`
    #       representing the next cell that we want to check
    #       and we don't want any unit to put before this cell on the current
    #       board, this way we avoid giving duplicate solutions and extra
    #       computation
    #       To decode cell_num: row_num, col_num = divmod(cell_num, col_count)
    cell_count = row_count * col_count
    stage = tuple(
        count_by_symbol.get(cls.symbol, 0)
        for cls in Unit.class_list
    )
    todo = [(
        {},     # initial board
        stage,  # initial stage
        sum(stage),  # initial stage_size
        0,      # first cell (top-left corner)
    )]

    while todo:  # stack not empty
        board, stage, stage_size, cell_num = todo.pop()

        if cell_num < cell_count - stage_size:
            # we can leave cell empty, skip to next one
            todo.append((
                board,
                stage,
                stage_size,
                cell_num + 1,
            ))

        cell_pos = divmod(cell_num, col_count)
        # cell_pos == (row_num, col_num)
        if Unit.pos_attacked_by_board(cell_pos[0], cell_pos[1], board):
            continue
        for unit_id, count in enumerate(stage):
            if count < 1:
                continue
            if cell_pos in board:
                continue
            unit = Unit.class_list[unit_id](*cell_pos)
            if unit.attacks_board(board):
                continue

            new_board = board.copy()
            new_board[cell_pos] = unit.symbol

            new_stage = list(stage)
            new_stage[unit_id] -= 1

            if stage_size <= 1:  # new_stage empty, new_board complete
                yield new_board
                continue

            if cell_num < cell_count - (stage_size - 1):
                todo.append((
                    new_board,
                    tuple(new_stage),
                    stage_size - 1,
                    cell_num + 1,
                ))


def _rec_low(row_count, col_count, board, stage, cell_num):
    #   `stage` is a tuple containing count or each unit type:
    #       (king_count, queen_count, bishop_count, rook_count, knight_count)
    #   `cell_num` is an int resulting from `row_num * col_count + col_num`
    #       representing the next cell that we want to check
    #       and we don't want any unit to put before this cell on the current
    #       board, this way we avoid giving duplicate solutions and extra
    #       computation
    #       To decode cell_num: row_num, col_num = divmod(cell_num, col_count)

    cell_count = row_count * col_count
    stage_size = sum(stage)

    if cell_num < cell_count - stage_size:
        # we can leave cell empty, skip to next one
        yield from _rec_low(
            row_count,
            col_count,
            board,
            stage,
            cell_num + 1,
        )

    cell_pos = divmod(cell_num, col_count)
    # cell_pos == (row_num, col_num)
    if Unit.pos_attacked_by_board(cell_pos[0], cell_pos[1], board):
        return
    for unit_id, count in enumerate(stage):
        if count < 1:
            continue
        if cell_pos in board:
            continue
        unit = Unit.class_list[unit_id](*cell_pos)
        if unit.attacks_board(board):
            continue

        new_board = board.copy()
        new_board[cell_pos] = unit.symbol

        new_stage = list(stage)
        new_stage[unit_id] -= 1
        assert new_stage[unit_id] >= 0

        if stage_size <= 1:  # new_stage empty, new_board complete
            yield new_board
            continue

        if cell_num < cell_count - (stage_size - 1):
            yield from _rec_low(
                row_count,
                col_count,
                new_board,
                tuple(new_stage),
                cell_num + 1,
            )


def find_solutions_r(row_count, col_count, count_by_symbol):
    """find and iterate over solution boards, implemented with Recursion
    This works only with Python 3.3 and later, as we use `yield from ...`

    row_count: int, number or rows
    col_count: int, number of columns
    count_by_symbol: dict of { unitSymbol => count }

    this is a generator, yields a completed `board` each time
    where `board` is a dict of {(row_num, col_num) => unitSymbol}
    """
    stage = tuple(
        count_by_symbol.get(cls.symbol, 0)
        for cls in Unit.class_list
    )
    yield from _rec_low(
        row_count,
        col_count,
        {},     # initial board
        stage,  # initial stage
        0,      # first cell (top-left corner)
    )


def find_solutions_q(row_count, col_count, count_by_symbol):
    """find and iterate over solution boards, implemented with Queue

    row_count: int, number or rows
    col_count: int, number of columns
    count_by_symbol: dict of { unitSymbol => count }

    this is a generator, yields a completed `board` each time
    where `board` is a dict of {(row_num, col_num) => unitSymbol}
    """
    # `todo` is a Queue instance (we use .empty, .put, and .get)
    # each item is a tuple of (board, stage, cell_num)
    #   `board` is a dict of {(row_num, col_num) => unitSymbol}
    #   `stage` is a tuple containing count or each unit type:
    #       (king_count, queen_count, bishop_count, rook_count, knight_count)
    #   `cell_num` is an int resulting from `row_num * col_count + col_num`
    #       representing the next cell that we want to check
    #       and we don't want any unit to put before this cell on the current
    #       board, this way we avoid giving duplicate solutions and extra
    #       computation
    #       To decode cell_num: row_num, col_num = divmod(cell_num, col_count)
    cell_count = row_count * col_count
    stage = tuple(
        count_by_symbol.get(cls.symbol, 0)
        for cls in Unit.class_list
    )
    todo = queue.Queue()
    todo.put((
        {},     # initial board
        stage,  # initial stage
        0,      # first cell (top-left corner)
    ))

    while not todo.empty():  # queue not empty
        board, stage, cell_num = todo.get()
        stage_size = sum(stage)

        if cell_num < cell_count - stage_size:
            # we can leave cell empty, skip to next one
            todo.put((
                board,
                stage,
                cell_num + 1,
            ))

        cell_pos = divmod(cell_num, col_count)
        # cell_pos == (row_num, col_num)
        if Unit.pos_attacked_by_board(cell_pos[0], cell_pos[1], board):
            continue
        for unit_id, count in enumerate(stage):
            if count < 1:
                continue
            if cell_pos in board:
                continue
            unit = Unit.class_list[unit_id](*cell_pos)
            if unit.attacks_board(board):
                continue

            new_board = board.copy()
            new_board[cell_pos] = unit.symbol

            new_stage = list(stage)
            new_stage[unit_id] -= 1
            assert new_stage[unit_id] >= 0

            if stage_size <= 1:  # new_stage empty, new_board complete
                yield new_board
                continue

            if cell_num < cell_count - (stage_size - 1):
                todo.put((
                    new_board,
                    tuple(new_stage),
                    cell_num + 1,
                ))
