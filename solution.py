#!/usr/bin/env python3
"""
this module is responsible for finding and iterating over all unique possible
solutions / configurations by the given parameters
"""

import queue

from pieces import ChessPiece


def find_solutions_s(row_count, col_count, count_by_symbol):
    """find and iterate over solution boards, implemented with Stack

    row_count: int, number or rows
    col_count: int, number of columns
    count_by_symbol: dict of { piece_symbol => count }

    this is a generator, yields a completed `board` each time
    where `board` is a dict of {(row_num, col_num) => piece_symbol}
    """
    # `todo` is a stack (we use .append, and .pop)
    # each item is a tuple of (board, stage, cell_num)
    #   `board` is a dict of {(row_num, col_num) => piece_symbol}
    #   `stage` is a list containing count or each piece type:
    #       [king_count, queen_count, bishop_count, rook_count, knight_count]
    #   `cell_num` is an int resulting from `row_num * col_count + col_num`
    #       representing the next cell that we want to check
    #       and we don't want any piece to put before this cell on the current
    #       board, this way we avoid giving duplicate solutions and extra
    #       computation
    #       To decode cell_num: row_num, col_num = divmod(cell_num, col_count)
    cell_count = row_count * col_count
    stage = [
        count_by_symbol.get(cls.symbol, 0)
        for cls in ChessPiece.class_list
    ]
    del count_by_symbol
    todo = [(
        {},     # initial board
        stage,  # initial stage
        sum(stage),  # initial stage_size
        0,      # first cell (top-left corner)
        None,   # last_piece
    )]

    while todo:  # stack not empty
        (
            board,
            stage,
            stage_size,
            cell_num,
            last_piece,
        ) = todo.pop()

        if cell_num < cell_count - stage_size:
            # we can leave cell empty, skip to next one
            todo.append((
                board,
                stage,
                stage_size,
                cell_num + 1,
                last_piece,
            ))

        cell_pos = divmod(cell_num, col_count)
        # cell_pos == (row_num, col_num)
        if last_piece and last_piece.attacks_pos(*cell_pos):
            continue
        if ChessPiece.pos_attacked_by_board(cell_pos[0], cell_pos[1], board):
            continue
        tmp_todo = []
        for piece_id, count in enumerate(stage):
            if count < 1:
                continue
            piece = ChessPiece.class_list[piece_id](*cell_pos)
            if piece.attacks_board(board):
                continue

            new_board = board.copy()
            new_board[cell_pos] = piece.symbol

            new_stage = list(stage)
            new_stage[piece_id] -= 1

            if stage_size <= 1:  # new_stage empty, new_board complete
                yield new_board
                continue

            if cell_num < cell_count - (stage_size - 1):
                tmp_todo.append((
                    new_board,
                    new_stage,
                    stage_size - 1,
                    cell_num + 1,
                    piece,  # the new last_piece
                ))
        todo += reversed(tmp_todo)
        tmp_todo = []


def _rec_low(row_count,
             col_count,
             board,
             stage,
             stage_size,
             cell_num,
             last_piece):
    #   `stage` is a list containing count or each piece type:
    #       [king_count, queen_count, bishop_count, rook_count, knight_count]
    #   `cell_num` is an int resulting from `row_num * col_count + col_num`
    #       representing the next cell that we want to check
    #       and we don't want any piece to put before this cell on the current
    #       board, this way we avoid giving duplicate solutions and extra
    #       computation
    #       To decode cell_num: row_num, col_num = divmod(cell_num, col_count)

    cell_count = row_count * col_count

    cell_pos = divmod(cell_num, col_count)
    # cell_pos == (row_num, col_num)
    if not ChessPiece.pos_attacked_by_board(cell_pos[0], cell_pos[1], board):
        for piece_id, count in enumerate(stage):
            if count < 1:
                continue
            piece = ChessPiece.class_list[piece_id](*cell_pos)
            if piece.attacks_board(board):
                continue

            new_board = board.copy()
            new_board[cell_pos] = piece.symbol

            new_stage = list(stage)
            new_stage[piece_id] -= 1

            if stage_size <= 1:  # new_stage empty, new_board complete
                yield new_board
                continue

            if cell_num < cell_count - (stage_size - 1):
                yield from _rec_low(
                    row_count,
                    col_count,
                    new_board,
                    new_stage,
                    stage_size - 1,
                    cell_num + 1,
                    piece,  # the new last_piece
                )

    if cell_num < cell_count - stage_size:
        # we can leave cell empty, skip to next one
        yield from _rec_low(
            row_count,
            col_count,
            board,
            stage,
            stage_size,
            cell_num + 1,
            last_piece,
        )


def find_solutions_r(row_count, col_count, count_by_symbol):
    """find and iterate over solution boards, implemented with Recursion
    This works only with Python 3.3 and later, as we use `yield from ...`

    row_count: int, number or rows
    col_count: int, number of columns
    count_by_symbol: dict of { piece_symbol => count }

    this is a generator, yields a completed `board` each time
    where `board` is a dict of {(row_num, col_num) => piece_symbol}
    """
    stage = [
        count_by_symbol.get(cls.symbol, 0)
        for cls in ChessPiece.class_list
    ]
    yield from _rec_low(
        row_count,
        col_count,
        {},     # initial board
        stage,  # initial stage
        sum(stage),  # initial stage_size
        0,      # first cell (top-left corner)
        None,   # last_piece
    )


def find_solutions_q(row_count, col_count, count_by_symbol):
    """find and iterate over solution boards, implemented with Queue

    row_count: int, number or rows
    col_count: int, number of columns
    count_by_symbol: dict of { piece_symbol => count }

    this is a generator, yields a completed `board` each time
    where `board` is a dict of {(row_num, col_num) => piece_symbol}
    """
    # `todo` is a Queue instance (we use .empty, .put, and .get)
    # each item is a tuple of (board, stage, cell_num)
    #   `board` is a dict of {(row_num, col_num) => piece_symbol}
    #   `stage` is a list containing count or each piece type:
    #       [king_count, queen_count, bishop_count, rook_count, knight_count]
    #   `cell_num` is an int resulting from `row_num * col_count + col_num`
    #       representing the next cell that we want to check
    #       and we don't want any piece to put before this cell on the current
    #       board, this way we avoid giving duplicate solutions and extra
    #       computation
    #       To decode cell_num: row_num, col_num = divmod(cell_num, col_count)
    cell_count = row_count * col_count
    stage = [
        count_by_symbol.get(cls.symbol, 0)
        for cls in ChessPiece.class_list
    ]
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
        if ChessPiece.pos_attacked_by_board(cell_pos[0], cell_pos[1], board):
            continue
        for piece_id, count in enumerate(stage):
            if count < 1:
                continue
            if cell_pos in board:
                continue
            piece = ChessPiece.class_list[piece_id](*cell_pos)
            if piece.attacks_board(board):
                continue

            new_board = board.copy()
            new_board[cell_pos] = piece.symbol

            new_stage = list(stage)
            new_stage[piece_id] -= 1

            if stage_size <= 1:  # new_stage empty, new_board complete
                yield new_board
                continue

            if cell_num < cell_count - (stage_size - 1):
                todo.put((
                    new_board,
                    new_stage,
                    cell_num + 1,
                ))
