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


class ChessPieceTest(unittest.TestCase):
    def test_set_pos(self):
        """
        test case for ChessPiece.set_pos and ChessPiece.get_pos methods
        """
        piece = ChessPiece(3, 4)
        self.assertEqual(piece.get_pos(), (3, 4))

        piece.set_pos(6, 5)
        self.assertEqual(piece.get_pos(), (6, 5))


class KingTest(unittest.TestCase):
    def test_attacks_1(self):
        """
        test case for King.attacks_pos method
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
    def test_attacks_1(self):
        """
        test case for Queen.attacks_pos method
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
    def test_attacks_1(self):
        """
        test case for Bishop.attacks_pos method
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
    def test_attacks_1(self):
        """
        test case for Rook.attacks_pos method
        """
        rook = Rook(5, 5)

        self.assertTrue(rook.attacks_pos(1, 5))
        self.assertTrue(rook.attacks_pos(5, 3))
        self.assertTrue(rook.attacks_pos(5, 4))

        self.assertFalse(rook.attacks_pos(4, 4))
        self.assertFalse(rook.attacks_pos(3, 4))
        self.assertFalse(rook.attacks_pos(6, 6))


class KnightTest(unittest.TestCase):
    def test_attacks_1(self):
        """
        test case for Knight.attacks_pos method
        """
        knight = Knight(5, 5)

        self.assertTrue(knight.attacks_pos(6, 7))
        self.assertTrue(knight.attacks_pos(4, 3))
        self.assertTrue(knight.attacks_pos(3, 6))

        self.assertFalse(knight.attacks_pos(5, 4))
        self.assertFalse(knight.attacks_pos(0, 5))
        self.assertFalse(knight.attacks_pos(4, 4))


if __name__ == '__main__':
    unittest.main()
