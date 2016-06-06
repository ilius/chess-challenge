#!/usr/bin/env python3
"""
this module contains test cases (based on Python's unittest)
"""

import unittest

from pieces import (
    ChessPiece,
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


if __name__ == '__main__':
    unittest.main()
