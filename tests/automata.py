"""tests for automata"""

import unittest as ut
import regex.automata as aut


class ConversionTestENFA(ut.TestCase):

    prt = False

    @classmethod
    def _convert(cls, re: str):
        enfa = aut.ENFA.get_enfa(re)
        if cls.prt:
            with open('out.txt', 'a') as f:
                f.seek(0, 2)
                print(enfa, file=f, flush=True)
        return enfa.transitions

    def test_operator(self):
        self.assertDictEqual(
            self._convert(r"a+"),
            {(0, ''): {2}, (3, 'a'): {4}, (2, ''): {3}, (4, ''): {3, 5}, (5, ''): {1}}
        )
        self.assertDictEqual(
            self._convert(r"a*"),
            {(0, ''): {2}, (3, 'a'): {4}, (2, ''): {3, 5}, (4, ''): {3, 5}, (5, ''): {1}}
        )
        self.assertDictEqual(
            self._convert(r"a?"),
            {(0, ''): {2}, (3, 'a'): {4}, (2, ''): {3, 5}, (4, ''): {5}, (5, ''): {1}}
        )
        self.assertDictEqual(
            self._convert(r"a{3}"),
            {(0, ''): {2}, (2, 'a'): {4}, (4, 'a'): {5}, (5, 'a'): {6}, (6, ''): {3}, (3, ''): {1}}
        )
        self.assertDictEqual(
            self._convert(r"a{2,4}"),
            {(0, ''): {2}, (2, 'a'): {4}, (4, 'a'): {5}, (5, ''): {3}, (5, 'a'): {6}, (6, ''): {3}, (6, 'a'): {7},
             (7, ''): {3}, (3, ''): {1}}
        )

    def test_concatenation(self):
        self.assertDictEqual(
            self._convert(r"ab"),
            {(0, ''): {2}, (2, 'a'): {3}, (3, 'b'): {4}, (4, ''): {1}}
        )
        self.assertDictEqual(
            self._convert(r"abc"),
            {(0, ''): {2}, (2, 'a'): {3}, (3, 'b'): {4}, (4, 'c'): {5}, (5, ''): {1}}
        )

    def test_alternative(self):
        self.assertDictEqual(
            self._convert(r"a|b"),
            {(0, ''): {2, 4}, (2, 'a'): {3}, (3, ''): {1}, (4, 'b'): {5}, (5, ''): {1}}
        )

    def test_special_symbols(self):
        self.assertDictEqual(
            self._convert(r"."),
            {(0, ''): {2}, (2, '\x00'): {3}, (2, '\x01'): {3}, (2, '\x02'): {3}, (2, '\x03'): {3}, (2, '\x04'): {3},
             (2, '\x05'): {3}, (2, '\x06'): {3}, (2, '\x07'): {3}, (2, '\x08'): {3}, (2, '\t'): {3}, (2, '\x0b'): {3},
             (2, '\x0c'): {3}, (2, '\r'): {3}, (2, '\x0e'): {3}, (2, '\x0f'): {3}, (2, '\x10'): {3}, (2, '\x11'): {3},
             (2, '\x12'): {3}, (2, '\x13'): {3}, (2, '\x14'): {3}, (2, '\x15'): {3}, (2, '\x16'): {3}, (2, '\x17'): {3},
             (2, '\x18'): {3}, (2, '\x19'): {3}, (2, '\x1a'): {3}, (2, '\x1b'): {3}, (2, '\x1c'): {3}, (2, '\x1d'): {3},
             (2, '\x1e'): {3}, (2, '\x1f'): {3}, (2, ' '): {3}, (2, '!'): {3}, (2, '"'): {3}, (2, '#'): {3},
             (2, '$'): {3}, (2, '%'): {3}, (2, '&'): {3}, (2, "'"): {3}, (2, '('): {3}, (2, ')'): {3}, (2, '*'): {3},
             (2, '+'): {3}, (2, ','): {3}, (2, '-'): {3}, (2, '.'): {3}, (2, '/'): {3}, (2, '0'): {3}, (2, '1'): {3},
             (2, '2'): {3}, (2, '3'): {3}, (2, '4'): {3}, (2, '5'): {3}, (2, '6'): {3}, (2, '7'): {3}, (2, '8'): {3},
             (2, '9'): {3}, (2, ':'): {3}, (2, ';'): {3}, (2, '<'): {3}, (2, '='): {3}, (2, '>'): {3}, (2, '?'): {3},
             (2, '@'): {3}, (2, 'A'): {3}, (2, 'B'): {3}, (2, 'C'): {3}, (2, 'D'): {3}, (2, 'E'): {3}, (2, 'F'): {3},
             (2, 'G'): {3}, (2, 'H'): {3}, (2, 'I'): {3}, (2, 'J'): {3}, (2, 'K'): {3}, (2, 'L'): {3}, (2, 'M'): {3},
             (2, 'N'): {3}, (2, 'O'): {3}, (2, 'P'): {3}, (2, 'Q'): {3}, (2, 'R'): {3}, (2, 'S'): {3}, (2, 'T'): {3},
             (2, 'U'): {3}, (2, 'V'): {3}, (2, 'W'): {3}, (2, 'X'): {3}, (2, 'Y'): {3}, (2, 'Z'): {3}, (2, '['): {3},
             (2, '\\'): {3}, (2, ']'): {3}, (2, '^'): {3}, (2, '_'): {3}, (2, '`'): {3}, (2, 'a'): {3}, (2, 'b'): {3},
             (2, 'c'): {3}, (2, 'd'): {3}, (2, 'e'): {3}, (2, 'f'): {3}, (2, 'g'): {3}, (2, 'h'): {3}, (2, 'i'): {3},
             (2, 'j'): {3}, (2, 'k'): {3}, (2, 'l'): {3}, (2, 'm'): {3}, (2, 'n'): {3}, (2, 'o'): {3}, (2, 'p'): {3},
             (2, 'q'): {3}, (2, 'r'): {3}, (2, 's'): {3}, (2, 't'): {3}, (2, 'u'): {3}, (2, 'v'): {3}, (2, 'w'): {3},
             (2, 'x'): {3}, (2, 'y'): {3}, (2, 'z'): {3}, (2, '{'): {3}, (2, '|'): {3}, (2, '}'): {3}, (2, '~'): {3},
             (2, '\x7f'): {3}, (3, ''): {1}}
        )
        self.assertDictEqual(
            self._convert("\d"),
            {(0, ''): {2}, (2, '0'): {3}, (2, '1'): {3}, (2, '2'): {3}, (2, '3'): {3}, (2, '4'): {3}, (2, '5'): {3},
             (2, '6'): {3}, (2, '7'): {3}, (2, '8'): {3}, (2, '9'): {3}, (3, ''): {1}}
        )
        self.assertDictEqual(
            self._convert("\D"),
            {(0, ''): {2}, (2, '\x00'): {3}, (2, '\x01'): {3}, (2, '\x02'): {3}, (2, '\x03'): {3}, (2, '\x04'): {3},
             (2, '\x05'): {3}, (2, '\x06'): {3}, (2, '\x07'): {3}, (2, '\x08'): {3}, (2, '\t'): {3}, (2, '\n'): {3},
             (2, '\x0b'): {3}, (2, '\x0c'): {3}, (2, '\r'): {3}, (2, '\x0e'): {3}, (2, '\x0f'): {3}, (2, '\x10'): {3},
             (2, '\x11'): {3}, (2, '\x12'): {3}, (2, '\x13'): {3}, (2, '\x14'): {3}, (2, '\x15'): {3}, (2, '\x16'): {3},
             (2, '\x17'): {3}, (2, '\x18'): {3}, (2, '\x19'): {3}, (2, '\x1a'): {3}, (2, '\x1b'): {3}, (2, '\x1c'): {3},
             (2, '\x1d'): {3}, (2, '\x1e'): {3}, (2, '\x1f'): {3}, (2, ' '): {3}, (2, '!'): {3}, (2, '"'): {3},
             (2, '#'): {3}, (2, '$'): {3}, (2, '%'): {3}, (2, '&'): {3}, (2, "'"): {3}, (2, '('): {3}, (2, ')'): {3},
             (2, '*'): {3}, (2, '+'): {3}, (2, ','): {3}, (2, '-'): {3}, (2, '.'): {3}, (2, '/'): {3}, (2, ':'): {3},
             (2, ';'): {3}, (2, '<'): {3}, (2, '='): {3}, (2, '>'): {3}, (2, '?'): {3}, (2, '@'): {3}, (2, 'A'): {3},
             (2, 'B'): {3}, (2, 'C'): {3}, (2, 'D'): {3}, (2, 'E'): {3}, (2, 'F'): {3}, (2, 'G'): {3}, (2, 'H'): {3},
             (2, 'I'): {3}, (2, 'J'): {3}, (2, 'K'): {3}, (2, 'L'): {3}, (2, 'M'): {3}, (2, 'N'): {3}, (2, 'O'): {3},
             (2, 'P'): {3}, (2, 'Q'): {3}, (2, 'R'): {3}, (2, 'S'): {3}, (2, 'T'): {3}, (2, 'U'): {3}, (2, 'V'): {3},
             (2, 'W'): {3}, (2, 'X'): {3}, (2, 'Y'): {3}, (2, 'Z'): {3}, (2, '['): {3}, (2, '\\'): {3}, (2, ']'): {3},
             (2, '^'): {3}, (2, '_'): {3}, (2, '`'): {3}, (2, 'a'): {3}, (2, 'b'): {3}, (2, 'c'): {3}, (2, 'd'): {3},
             (2, 'e'): {3}, (2, 'f'): {3}, (2, 'g'): {3}, (2, 'h'): {3}, (2, 'i'): {3}, (2, 'j'): {3}, (2, 'k'): {3},
             (2, 'l'): {3}, (2, 'm'): {3}, (2, 'n'): {3}, (2, 'o'): {3}, (2, 'p'): {3}, (2, 'q'): {3}, (2, 'r'): {3},
             (2, 's'): {3}, (2, 't'): {3}, (2, 'u'): {3}, (2, 'v'): {3}, (2, 'w'): {3}, (2, 'x'): {3}, (2, 'y'): {3},
             (2, 'z'): {3}, (2, '{'): {3}, (2, '|'): {3}, (2, '}'): {3}, (2, '~'): {3}, (2, '\x7f'): {3},
             (2, '\x80'): {3}, (3, ''): {1}}
        )
        self.assertDictEqual(
            self._convert("\s"),
            {(0, ''): {2}, (2, ' '): {3}, (2, '\t'): {3}, (2, '\x0b'): {3}, (2, '\n'): {3}, (2, '\r'): {3},
             (2, '\x0c'): {3}, (3, ''): {1}}
        )
        self.assertDictEqual(
            self._convert("\S"),
            {(0, ''): {2}, (2, '\x00'): {3}, (2, '\x01'): {3}, (2, '\x02'): {3}, (2, '\x03'): {3}, (2, '\x04'): {3},
             (2, '\x05'): {3}, (2, '\x06'): {3}, (2, '\x07'): {3}, (2, '\x08'): {3}, (2, '\x0e'): {3}, (2, '\x0f'): {3},
             (2, '\x10'): {3}, (2, '\x11'): {3}, (2, '\x12'): {3}, (2, '\x13'): {3}, (2, '\x14'): {3}, (2, '\x15'): {3},
             (2, '\x16'): {3}, (2, '\x17'): {3}, (2, '\x18'): {3}, (2, '\x19'): {3}, (2, '\x1a'): {3}, (2, '\x1b'): {3},
             (2, '\x1c'): {3}, (2, '\x1d'): {3}, (2, '\x1e'): {3}, (2, '\x1f'): {3}, (2, '!'): {3}, (2, '"'): {3},
             (2, '#'): {3}, (2, '$'): {3}, (2, '%'): {3}, (2, '&'): {3}, (2, "'"): {3}, (2, '('): {3}, (2, ')'): {3},
             (2, '*'): {3}, (2, '+'): {3}, (2, ','): {3}, (2, '-'): {3}, (2, '.'): {3}, (2, '/'): {3}, (2, '0'): {3},
             (2, '1'): {3}, (2, '2'): {3}, (2, '3'): {3}, (2, '4'): {3}, (2, '5'): {3}, (2, '6'): {3}, (2, '7'): {3},
             (2, '8'): {3}, (2, '9'): {3}, (2, ':'): {3}, (2, ';'): {3}, (2, '<'): {3}, (2, '='): {3}, (2, '>'): {3},
             (2, '?'): {3}, (2, '@'): {3}, (2, 'A'): {3}, (2, 'B'): {3}, (2, 'C'): {3}, (2, 'D'): {3}, (2, 'E'): {3},
             (2, 'F'): {3}, (2, 'G'): {3}, (2, 'H'): {3}, (2, 'I'): {3}, (2, 'J'): {3}, (2, 'K'): {3}, (2, 'L'): {3},
             (2, 'M'): {3}, (2, 'N'): {3}, (2, 'O'): {3}, (2, 'P'): {3}, (2, 'Q'): {3}, (2, 'R'): {3}, (2, 'S'): {3},
             (2, 'T'): {3}, (2, 'U'): {3}, (2, 'V'): {3}, (2, 'W'): {3}, (2, 'X'): {3}, (2, 'Y'): {3}, (2, 'Z'): {3},
             (2, '['): {3}, (2, '\\'): {3}, (2, ']'): {3}, (2, '^'): {3}, (2, '_'): {3}, (2, '`'): {3}, (2, 'a'): {3},
             (2, 'b'): {3}, (2, 'c'): {3}, (2, 'd'): {3}, (2, 'e'): {3}, (2, 'f'): {3}, (2, 'g'): {3}, (2, 'h'): {3},
             (2, 'i'): {3}, (2, 'j'): {3}, (2, 'k'): {3}, (2, 'l'): {3}, (2, 'm'): {3}, (2, 'n'): {3}, (2, 'o'): {3},
             (2, 'p'): {3}, (2, 'q'): {3}, (2, 'r'): {3}, (2, 's'): {3}, (2, 't'): {3}, (2, 'u'): {3}, (2, 'v'): {3},
             (2, 'w'): {3}, (2, 'x'): {3}, (2, 'y'): {3}, (2, 'z'): {3}, (2, '{'): {3}, (2, '|'): {3}, (2, '}'): {3},
             (2, '~'): {3}, (2, '\x7f'): {3}, (3, ''): {1}}
        )
        self.assertDictEqual(
            self._convert("\w"),
            {(0, ''): {2}, (2, 'A'): {3}, (2, 'B'): {3}, (2, 'C'): {3}, (2, 'D'): {3}, (2, 'E'): {3}, (2, 'F'): {3},
             (2, 'G'): {3}, (2, 'H'): {3}, (2, 'I'): {3}, (2, 'J'): {3}, (2, 'K'): {3}, (2, 'L'): {3}, (2, 'M'): {3},
             (2, 'N'): {3}, (2, 'O'): {3}, (2, 'P'): {3}, (2, 'Q'): {3}, (2, 'R'): {3}, (2, 'S'): {3}, (2, 'T'): {3},
             (2, 'U'): {3}, (2, 'V'): {3}, (2, 'W'): {3}, (2, 'X'): {3}, (2, 'Y'): {3}, (2, 'Z'): {3}, (2, 'a'): {3},
             (2, 'b'): {3}, (2, 'c'): {3}, (2, 'd'): {3}, (2, 'e'): {3}, (2, 'f'): {3}, (2, 'g'): {3}, (2, 'h'): {3},
             (2, 'i'): {3}, (2, 'j'): {3}, (2, 'k'): {3}, (2, 'l'): {3}, (2, 'm'): {3}, (2, 'n'): {3}, (2, 'o'): {3},
             (2, 'p'): {3}, (2, 'q'): {3}, (2, 'r'): {3}, (2, 's'): {3}, (2, 't'): {3}, (2, 'u'): {3}, (2, 'v'): {3},
             (2, 'w'): {3}, (2, 'x'): {3}, (2, 'y'): {3}, (2, 'z'): {3}, (2, '0'): {3}, (2, '1'): {3}, (2, '2'): {3},
             (2, '3'): {3}, (2, '4'): {3}, (2, '5'): {3}, (2, '6'): {3}, (2, '7'): {3}, (2, '8'): {3}, (2, '9'): {3},
             (2, '_'): {3}, (3, ''): {1}}
        )
        self.assertDictEqual(
            self._convert("\W"),
            {(0, ''): {2}, (2, '\x00'): {3}, (2, '\x01'): {3}, (2, '\x02'): {3}, (2, '\x03'): {3}, (2, '\x04'): {3},
             (2, '\x05'): {3}, (2, '\x06'): {3}, (2, '\x07'): {3}, (2, '\x08'): {3}, (2, '\t'): {3}, (2, '\n'): {3},
             (2, '\x0b'): {3}, (2, '\x0c'): {3}, (2, '\r'): {3}, (2, '\x0e'): {3}, (2, '\x0f'): {3}, (2, '\x10'): {3},
             (2, '\x11'): {3}, (2, '\x12'): {3}, (2, '\x13'): {3}, (2, '\x14'): {3}, (2, '\x15'): {3}, (2, '\x16'): {3},
             (2, '\x17'): {3}, (2, '\x18'): {3}, (2, '\x19'): {3}, (2, '\x1a'): {3}, (2, '\x1b'): {3}, (2, '\x1c'): {3},
             (2, '\x1d'): {3}, (2, '\x1e'): {3}, (2, '\x1f'): {3}, (2, ' '): {3}, (2, '!'): {3}, (2, '"'): {3},
             (2, '#'): {3}, (2, '$'): {3}, (2, '%'): {3}, (2, '&'): {3}, (2, "'"): {3}, (2, '('): {3}, (2, ')'): {3},
             (2, '*'): {3}, (2, '+'): {3}, (2, ','): {3}, (2, '-'): {3}, (2, '.'): {3}, (2, '/'): {3}, (2, ':'): {3},
             (2, ';'): {3}, (2, '<'): {3}, (2, '='): {3}, (2, '>'): {3}, (2, '?'): {3}, (2, '@'): {3}, (2, '['): {3},
             (2, '\\'): {3}, (2, ']'): {3}, (2, '^'): {3}, (2, '_'): {3}, (2, '`'): {3}, (2, '{'): {3}, (2, '|'): {3},
             (2, '}'): {3}, (2, '~'): {3}, (2, '\x7f'): {3}, (2, '\x80'): {3}, (3, ''): {1}}
        )


class ConversionTestNFA(ut.TestCase):

    prt = False

    @classmethod
    def _convert(cls, re: str):
        enfa = aut.ENFA.get_enfa(re)
        nfa = aut.NFA.get_nfa(enfa)
        if cls.prt:
            with open('out.txt', 'a') as f:
                f.seek(0, 2)
                print(enfa, nfa, file=f, flush=True)
        return nfa.transitions, nfa.end_states

    def test_basic(self):
        self.assertTupleEqual(
            self._convert("a"),
            (
                {
                    (0, 'a'): {1, 3}
                },
                {1, 3}
            )
        )
        self.assertTupleEqual(
            self._convert("ab"),
            (
                {

                    (0, 'a'): {3}, (3, 'b'): {1, 4}
                },
                {1, 4}
            )
        )
        self.assertTupleEqual(
            self._convert("a*"),
            (
                {
                    (0, 'a'): {1, 3, 4, 5}, (3, 'a'): {1, 3, 4, 5}, (4, 'a'): {1, 3, 4, 5}
                },
                {0, 1, 4, 5}
            )
        )
        self.assertTupleEqual(
            self._convert("a|b"),
            (
                {
                    (0, 'a'): {1, 3}, (0, 'b'): {1, 5}
                },
                {1, 3, 5}
            )
        )
