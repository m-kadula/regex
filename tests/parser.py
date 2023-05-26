"""Tests for the lexer and the parser"""

import unittest as ut
import regex.parser as par


class LexerTest(ut.TestCase):

    def test_basic(self):
        re = r'[^a-zA-Z]+\(\d+\)'
        lexer = par.Lexer(re)
        print(*lexer.parts, sep='\n')
        self.assertTrue(len(lexer) == 13)
        for pair in lexer:
            if pair.symbol in par.Lexer.tokens:
                self.assertTrue(pair.sym_type == par.PartType.TOKEN or pair.symbol in '()')
            elif pair.symbol != 'd':
                self.assertTrue(pair.sym_type == par.PartType.NORMAL)
