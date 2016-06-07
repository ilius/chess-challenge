#!/usr/bin/env python3
"""
this module contains test cases (based on Python's unittest)
"""

import unittest

from pieces import (
    ChessPiece,
    King,
    Queen,
    Bishop,
    Rook,
    Knight,
)

from solution import (
    find_solutions_s,
    find_solutions_r,
)
from solution_analyze import check_board_gen_order_uniqueness


class ChessPieceTest(unittest.TestCase):
    """test case for ChessPiece class"""
    def test_set_pos(self):
        """
        test method for ChessPiece.set_pos and ChessPiece.get_pos methods
        """
        piece = ChessPiece(3, 4)
        self.assertEqual(piece.get_pos(), (3, 4))

        piece.set_pos(6, 5)
        self.assertEqual(piece.get_pos(), (6, 5))

    def test_pos_attacked_by_board(self):
        """
        test method for ChessPiece.pos_attacked_by_board class method
        test board:
        ---------------------
        | Q | . | . | . | K |
        ---------------------
        | . | . | . | . | . |
        ---------------------
        | . | . | . | . | R |
        ---------------------
        | B |   | . | . | . |
        ---------------------
        | . | . |   |   | N |
        ---------------------
        """
        #  row_count = 5
        #  col_count = 5
        board = {
            (0, 0): 'Q',
            (0, 4): 'K',
            (2, 4): 'R',
            (3, 0): 'B',
            (4, 4): 'N',
        }

        self.assertTrue(ChessPiece.pos_attacked_by_board(0, 1, board))
        self.assertTrue(ChessPiece.pos_attacked_by_board(0, 2, board))
        self.assertTrue(ChessPiece.pos_attacked_by_board(0, 3, board))
        self.assertTrue(ChessPiece.pos_attacked_by_board(1, 0, board))
        self.assertTrue(ChessPiece.pos_attacked_by_board(1, 1, board))
        self.assertTrue(ChessPiece.pos_attacked_by_board(1, 2, board))
        self.assertTrue(ChessPiece.pos_attacked_by_board(1, 3, board))
        self.assertTrue(ChessPiece.pos_attacked_by_board(1, 4, board))
        self.assertTrue(ChessPiece.pos_attacked_by_board(2, 0, board))
        self.assertTrue(ChessPiece.pos_attacked_by_board(2, 1, board))
        self.assertTrue(ChessPiece.pos_attacked_by_board(2, 2, board))
        self.assertTrue(ChessPiece.pos_attacked_by_board(2, 3, board))
        self.assertFalse(ChessPiece.pos_attacked_by_board(3, 1, board))
        self.assertTrue(ChessPiece.pos_attacked_by_board(3, 2, board))
        self.assertTrue(ChessPiece.pos_attacked_by_board(3, 3, board))
        self.assertTrue(ChessPiece.pos_attacked_by_board(3, 4, board))
        self.assertTrue(ChessPiece.pos_attacked_by_board(4, 0, board))
        self.assertTrue(ChessPiece.pos_attacked_by_board(4, 1, board))
        self.assertFalse(ChessPiece.pos_attacked_by_board(4, 2, board))
        self.assertFalse(ChessPiece.pos_attacked_by_board(4, 3, board))


class KingTest(unittest.TestCase):
    """test case for King class"""
    def test_attacks_1(self):
        """
        test method for King.attacks_pos method
        """
        king = King(5, 5)

        self.assertTrue(king.attacks_pos(4, 5))
        self.assertTrue(king.attacks_pos(5, 4))
        self.assertTrue(king.attacks_pos(4, 4))
        self.assertTrue(king.attacks_pos(6, 5))
        self.assertTrue(king.attacks_pos(5, 6))
        self.assertTrue(king.attacks_pos(6, 6))

        self.assertFalse(king.attacks_pos(0, 0))
        self.assertFalse(king.attacks_pos(1, 1))
        self.assertFalse(king.attacks_pos(2, 2))
        self.assertFalse(king.attacks_pos(3, 3))
        self.assertFalse(king.attacks_pos(3, 4))


class QueenTest(unittest.TestCase):
    """test case for Queen class"""
    def test_attacks_1(self):
        """
        test method for Queen.attacks_pos method
        """
        queen = Queen(5, 5)

        self.assertTrue(queen.attacks_pos(0, 5))
        self.assertTrue(queen.attacks_pos(5, 0))

        self.assertTrue(queen.attacks_pos(4, 5))
        self.assertTrue(queen.attacks_pos(5, 6))

        self.assertTrue(queen.attacks_pos(3, 3))
        self.assertTrue(queen.attacks_pos(8, 2))

        self.assertFalse(queen.attacks_pos(0, 1))
        self.assertFalse(queen.attacks_pos(0, 2))
        self.assertFalse(queen.attacks_pos(1, 2))
        self.assertFalse(queen.attacks_pos(1, 3))
        self.assertFalse(queen.attacks_pos(1, 4))
        self.assertFalse(queen.attacks_pos(3, 2))
        self.assertFalse(queen.attacks_pos(3, 4))


class BishopTest(unittest.TestCase):
    """test case for Bishop class"""
    def test_attacks_1(self):
        """
        test method for Bishop.attacks_pos method
        """
        bishop = Bishop(5, 5)

        self.assertTrue(bishop.attacks_pos(1, 1))
        self.assertTrue(bishop.attacks_pos(2, 8))
        self.assertTrue(bishop.attacks_pos(7, 3))

        self.assertFalse(bishop.attacks_pos(0, 5))
        self.assertFalse(bishop.attacks_pos(5, 0))
        self.assertFalse(bishop.attacks_pos(5, 4))
        self.assertFalse(bishop.attacks_pos(5, 6))


class RookTest(unittest.TestCase):
    """test case for Rook class"""
    def test_attacks_1(self):
        """
        test method for Rook.attacks_pos method
        """
        rook = Rook(5, 5)

        self.assertTrue(rook.attacks_pos(1, 5))
        self.assertTrue(rook.attacks_pos(5, 3))
        self.assertTrue(rook.attacks_pos(5, 4))

        self.assertFalse(rook.attacks_pos(4, 4))
        self.assertFalse(rook.attacks_pos(3, 4))
        self.assertFalse(rook.attacks_pos(6, 6))


class KnightTest(unittest.TestCase):
    """test case for Knight class"""
    def test_attacks_1(self):
        """
        test method for Knight.attacks_pos method
        """
        knight = Knight(5, 5)

        self.assertTrue(knight.attacks_pos(6, 7))
        self.assertTrue(knight.attacks_pos(4, 3))
        self.assertTrue(knight.attacks_pos(3, 6))

        self.assertFalse(knight.attacks_pos(5, 4))
        self.assertFalse(knight.attacks_pos(0, 5))
        self.assertFalse(knight.attacks_pos(4, 4))


class SolutionCountTest(unittest.TestCase):
    """
    test case for counting unique solutions / configurations
    using both stack and recursive implementations
    (queue implementation is too slow, so we don't bother)
    """
    def check_count(self, solution_count, *args):
        """
        solution_count: known count of unique solutions / configurations
        the rest of arguments (*args) are given to find_solutions_s
            and find_solutions_r functions

        calls TestCase.assertEqual for both stack and recursive implementations
        """
        self.assertEqual(
            sum(1 for _ in find_solutions_s(*args)),  # 's' for stack
            solution_count,
        )
        self.assertEqual(
            sum(1 for _ in find_solutions_r(*args)),  # 'r' for recursive
            solution_count,
        )

    def test_count_1(self):
        self.check_count(
            16,  # solution count
            3,  # row count
            3,  # column count
            {'K': 2},
        )

    def test_count_2(self):
        self.check_count(
            78,  # solution count
            4,  # row count
            4,  # column count
            {'K': 2},
        )

    def test_count_3(self):
        self.check_count(
            128,  # solution count
            4,  # row count
            4,  # column count
            {'K': 2, 'Q': 1},
        )

    def test_count_4(self):
        self.check_count(
            104,  # solution count
            4,  # row count
            4,  # column count
            {'K': 2, 'Q': 1, 'B': 1},
        )

    def test_count_5(self):
        self.check_count(
            0,  # solution count
            4,  # row count
            4,  # column count
            {'K': 2, 'Q': 1, 'B': 1, 'R': 1},
        )

    def test_count_6(self):
        self.check_count(
            32,  # solution count
            4,  # row count
            4,  # column count
            {'K': 2, 'Q': 1, 'B': 1, 'N': 1},
        )

    def test_count_7(self):
        self.check_count(
            12,  # solution count
            4,  # row count
            4,  # column count
            {'K': 3, 'N': 3},
        )


class SolutionUniquenessTest(unittest.TestCase):
    """
    test case for checking uniqueness of solutions / configurations
    using both stack and recursive implementations
    (queue implementation is too slow, so we don't bother)
    """
    def check_u_order(self, row_count, col_count, count_by_symbol):
        """
        checks the uniqueness and order of boards by stack implementations
        """
        for find_solutions in (
            find_solutions_s,
            find_solutions_r,
        ):
            gen = find_solutions(row_count, col_count, count_by_symbol)
            self.assertTrue(check_board_gen_order_uniqueness(
                gen,
                row_count,
                col_count,
            ))

    def test_u_order_1(self):
        self.check_u_order(
            4,  # row count
            4,  # column count
            {'K': 2, 'Q': 1, 'B': 1, 'N': 1},
        )

    def test_u_order_2(self):
        self.check_u_order(
            5,  # row count
            5,  # column count
            {'K': 2, 'Q': 1, 'B': 1, 'N': 1},
        )

    def test_u_order_3(self):
        self.check_u_order(
            5,  # row count
            5,  # column count
            {'K': 2, 'Q': 1, 'B': 1, 'R': 1, 'N': 2},
        )


if __name__ == '__main__':
    unittest.main()
