"""tests for automata"""

import unittest as ut
import regex.automata as aut


class ConversionTestENFA(ut.TestCase):

    @classmethod
    def _convert(cls, re: str):
        enfa = aut.ENFA.get_enfa(re)
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
            {(0, 'a'): {1}, (0, 'b'): {1}}
        )

    def test_special_symbols(self):
        self.assertDictEqual(
            self._convert(r"."),
            {(0, '\x00'): {1}, (0, '\x01'): {1}, (0, '\x02'): {1}, (0, '\x03'): {1}, (0, '\x04'): {1}, (0, '\x05'): {1},
             (0, '\x06'): {1}, (0, '\x07'): {1}, (0, '\x08'): {1}, (0, '\t'): {1}, (0, '\x0b'): {1}, (0, '\x0c'): {1},
             (0, '\r'): {1}, (0, '\x0e'): {1}, (0, '\x0f'): {1}, (0, '\x10'): {1}, (0, '\x11'): {1}, (0, '\x12'): {1},
             (0, '\x13'): {1}, (0, '\x14'): {1}, (0, '\x15'): {1}, (0, '\x16'): {1}, (0, '\x17'): {1}, (0, '\x18'): {1},
             (0, '\x19'): {1}, (0, '\x1a'): {1}, (0, '\x1b'): {1}, (0, '\x1c'): {1}, (0, '\x1d'): {1}, (0, '\x1e'): {1},
             (0, '\x1f'): {1}, (0, ' '): {1}, (0, '!'): {1}, (0, '"'): {1}, (0, '#'): {1}, (0, '$'): {1}, (0, '%'): {1},
             (0, '&'): {1}, (0, "'"): {1}, (0, '('): {1}, (0, ')'): {1}, (0, '*'): {1}, (0, '+'): {1}, (0, ','): {1},
             (0, '-'): {1}, (0, '.'): {1}, (0, '/'): {1}, (0, '0'): {1}, (0, '1'): {1}, (0, '2'): {1}, (0, '3'): {1},
             (0, '4'): {1}, (0, '5'): {1}, (0, '6'): {1}, (0, '7'): {1}, (0, '8'): {1}, (0, '9'): {1}, (0, ':'): {1},
             (0, ';'): {1}, (0, '<'): {1}, (0, '='): {1}, (0, '>'): {1}, (0, '?'): {1}, (0, '@'): {1}, (0, 'A'): {1},
             (0, 'B'): {1}, (0, 'C'): {1}, (0, 'D'): {1}, (0, 'E'): {1}, (0, 'F'): {1}, (0, 'G'): {1}, (0, 'H'): {1},
             (0, 'I'): {1}, (0, 'J'): {1}, (0, 'K'): {1}, (0, 'L'): {1}, (0, 'M'): {1}, (0, 'N'): {1}, (0, 'O'): {1},
             (0, 'P'): {1}, (0, 'Q'): {1}, (0, 'R'): {1}, (0, 'S'): {1}, (0, 'T'): {1}, (0, 'U'): {1}, (0, 'V'): {1},
             (0, 'W'): {1}, (0, 'X'): {1}, (0, 'Y'): {1}, (0, 'Z'): {1}, (0, '['): {1}, (0, '\\'): {1}, (0, ']'): {1},
             (0, '^'): {1}, (0, '_'): {1}, (0, '`'): {1}, (0, 'a'): {1}, (0, 'b'): {1}, (0, 'c'): {1}, (0, 'd'): {1},
             (0, 'e'): {1}, (0, 'f'): {1}, (0, 'g'): {1}, (0, 'h'): {1}, (0, 'i'): {1}, (0, 'j'): {1}, (0, 'k'): {1},
             (0, 'l'): {1}, (0, 'm'): {1}, (0, 'n'): {1}, (0, 'o'): {1}, (0, 'p'): {1}, (0, 'q'): {1}, (0, 'r'): {1},
             (0, 's'): {1}, (0, 't'): {1}, (0, 'u'): {1}, (0, 'v'): {1}, (0, 'w'): {1}, (0, 'x'): {1}, (0, 'y'): {1},
             (0, 'z'): {1}, (0, '{'): {1}, (0, '|'): {1}, (0, '}'): {1}, (0, '~'): {1}, (0, '\x7f'): {1}}
        )
        self.assertDictEqual(
            self._convert("\d"),
            {(0, '0'): {1}, (0, '1'): {1}, (0, '2'): {1}, (0, '3'): {1}, (0, '4'): {1},
             (0, '5'): {1}, (0, '6'): {1}, (0, '7'): {1}, (0, '8'): {1}, (0, '9'): {1}}
        )
        self.assertDictEqual(
            self._convert("\D"),
            {(0, '\x00'): {1}, (0, '\x01'): {1}, (0, '\x02'): {1}, (0, '\x03'): {1}, (0, '\x04'): {1}, (0, '\x05'): {1},
             (0, '\x06'): {1}, (0, '\x07'): {1}, (0, '\x08'): {1}, (0, '\t'): {1}, (0, '\n'): {1}, (0, '\x0b'): {1},
             (0, '\x0c'): {1}, (0, '\r'): {1}, (0, '\x0e'): {1}, (0, '\x0f'): {1}, (0, '\x10'): {1}, (0, '\x11'): {1},
             (0, '\x12'): {1}, (0, '\x13'): {1}, (0, '\x14'): {1}, (0, '\x15'): {1}, (0, '\x16'): {1}, (0, '\x17'): {1},
             (0, '\x18'): {1}, (0, '\x19'): {1}, (0, '\x1a'): {1}, (0, '\x1b'): {1}, (0, '\x1c'): {1}, (0, '\x1d'): {1},
             (0, '\x1e'): {1}, (0, '\x1f'): {1}, (0, ' '): {1}, (0, '!'): {1}, (0, '"'): {1}, (0, '#'): {1},
             (0, '$'): {1}, (0, '%'): {1}, (0, '&'): {1}, (0, "'"): {1}, (0, '('): {1}, (0, ')'): {1}, (0, '*'): {1},
             (0, '+'): {1}, (0, ','): {1}, (0, '-'): {1}, (0, '.'): {1}, (0, '/'): {1}, (0, ':'): {1}, (0, ';'): {1},
             (0, '<'): {1}, (0, '='): {1}, (0, '>'): {1}, (0, '?'): {1}, (0, '@'): {1}, (0, 'A'): {1}, (0, 'B'): {1},
             (0, 'C'): {1}, (0, 'D'): {1}, (0, 'E'): {1}, (0, 'F'): {1}, (0, 'G'): {1}, (0, 'H'): {1}, (0, 'I'): {1},
             (0, 'J'): {1}, (0, 'K'): {1}, (0, 'L'): {1}, (0, 'M'): {1}, (0, 'N'): {1}, (0, 'O'): {1}, (0, 'P'): {1},
             (0, 'Q'): {1}, (0, 'R'): {1}, (0, 'S'): {1}, (0, 'T'): {1}, (0, 'U'): {1}, (0, 'V'): {1}, (0, 'W'): {1},
             (0, 'X'): {1}, (0, 'Y'): {1}, (0, 'Z'): {1}, (0, '['): {1}, (0, '\\'): {1}, (0, ']'): {1}, (0, '^'): {1},
             (0, '_'): {1}, (0, '`'): {1}, (0, 'a'): {1}, (0, 'b'): {1}, (0, 'c'): {1}, (0, 'd'): {1}, (0, 'e'): {1},
             (0, 'f'): {1}, (0, 'g'): {1}, (0, 'h'): {1}, (0, 'i'): {1}, (0, 'j'): {1}, (0, 'k'): {1}, (0, 'l'): {1},
             (0, 'm'): {1}, (0, 'n'): {1}, (0, 'o'): {1}, (0, 'p'): {1}, (0, 'q'): {1}, (0, 'r'): {1}, (0, 's'): {1},
             (0, 't'): {1}, (0, 'u'): {1}, (0, 'v'): {1}, (0, 'w'): {1}, (0, 'x'): {1}, (0, 'y'): {1}, (0, 'z'): {1},
             (0, '{'): {1}, (0, '|'): {1}, (0, '}'): {1}, (0, '~'): {1}, (0, '\x7f'): {1}, (0, '\x80'): {1}}
        )
        self.assertDictEqual(
            self._convert("\s"),
            {(0, ' '): {1}, (0, '\t'): {1}, (0, '\x0b'): {1}, (0, '\n'): {1}, (0, '\r'): {1}, (0, '\x0c'): {1}}
        )
        self.assertDictEqual(
            self._convert("\S"),
            {(0, '\x00'): {1}, (0, '\x01'): {1}, (0, '\x02'): {1}, (0, '\x03'): {1}, (0, '\x04'): {1}, (0, '\x05'): {1},
             (0, '\x06'): {1}, (0, '\x07'): {1}, (0, '\x08'): {1}, (0, '\x0e'): {1}, (0, '\x0f'): {1}, (0, '\x10'): {1},
             (0, '\x11'): {1}, (0, '\x12'): {1}, (0, '\x13'): {1}, (0, '\x14'): {1}, (0, '\x15'): {1}, (0, '\x16'): {1},
             (0, '\x17'): {1}, (0, '\x18'): {1}, (0, '\x19'): {1}, (0, '\x1a'): {1}, (0, '\x1b'): {1}, (0, '\x1c'): {1},
             (0, '\x1d'): {1}, (0, '\x1e'): {1}, (0, '\x1f'): {1}, (0, '!'): {1}, (0, '"'): {1}, (0, '#'): {1},
             (0, '$'): {1}, (0, '%'): {1}, (0, '&'): {1}, (0, "'"): {1}, (0, '('): {1}, (0, ')'): {1}, (0, '*'): {1},
             (0, '+'): {1}, (0, ','): {1}, (0, '-'): {1}, (0, '.'): {1}, (0, '/'): {1}, (0, '0'): {1}, (0, '1'): {1},
             (0, '2'): {1}, (0, '3'): {1}, (0, '4'): {1}, (0, '5'): {1}, (0, '6'): {1}, (0, '7'): {1}, (0, '8'): {1},
             (0, '9'): {1}, (0, ':'): {1}, (0, ';'): {1}, (0, '<'): {1}, (0, '='): {1}, (0, '>'): {1}, (0, '?'): {1},
             (0, '@'): {1}, (0, 'A'): {1}, (0, 'B'): {1}, (0, 'C'): {1}, (0, 'D'): {1}, (0, 'E'): {1}, (0, 'F'): {1},
             (0, 'G'): {1}, (0, 'H'): {1}, (0, 'I'): {1}, (0, 'J'): {1}, (0, 'K'): {1}, (0, 'L'): {1}, (0, 'M'): {1},
             (0, 'N'): {1}, (0, 'O'): {1}, (0, 'P'): {1}, (0, 'Q'): {1}, (0, 'R'): {1}, (0, 'S'): {1}, (0, 'T'): {1},
             (0, 'U'): {1}, (0, 'V'): {1}, (0, 'W'): {1}, (0, 'X'): {1}, (0, 'Y'): {1}, (0, 'Z'): {1}, (0, '['): {1},
             (0, '\\'): {1}, (0, ']'): {1}, (0, '^'): {1}, (0, '_'): {1}, (0, '`'): {1}, (0, 'a'): {1}, (0, 'b'): {1},
             (0, 'c'): {1}, (0, 'd'): {1}, (0, 'e'): {1}, (0, 'f'): {1}, (0, 'g'): {1}, (0, 'h'): {1}, (0, 'i'): {1},
             (0, 'j'): {1}, (0, 'k'): {1}, (0, 'l'): {1}, (0, 'm'): {1}, (0, 'n'): {1}, (0, 'o'): {1}, (0, 'p'): {1},
             (0, 'q'): {1}, (0, 'r'): {1}, (0, 's'): {1}, (0, 't'): {1}, (0, 'u'): {1}, (0, 'v'): {1}, (0, 'w'): {1},
             (0, 'x'): {1}, (0, 'y'): {1}, (0, 'z'): {1}, (0, '{'): {1}, (0, '|'): {1}, (0, '}'): {1}, (0, '~'): {1},
             (0, '\x7f'): {1}}
        )
        self.assertDictEqual(
            self._convert("\w"),
            {(0, 'A'): {1}, (0, 'B'): {1}, (0, 'C'): {1}, (0, 'D'): {1}, (0, 'E'): {1}, (0, 'F'): {1}, (0, 'G'): {1},
             (0, 'H'): {1}, (0, 'I'): {1}, (0, 'J'): {1}, (0, 'K'): {1}, (0, 'L'): {1}, (0, 'M'): {1}, (0, 'N'): {1},
             (0, 'O'): {1}, (0, 'P'): {1}, (0, 'Q'): {1}, (0, 'R'): {1}, (0, 'S'): {1}, (0, 'T'): {1}, (0, 'U'): {1},
             (0, 'V'): {1}, (0, 'W'): {1}, (0, 'X'): {1}, (0, 'Y'): {1}, (0, 'Z'): {1}, (0, 'a'): {1}, (0, 'b'): {1},
             (0, 'c'): {1}, (0, 'd'): {1}, (0, 'e'): {1}, (0, 'f'): {1}, (0, 'g'): {1}, (0, 'h'): {1}, (0, 'i'): {1},
             (0, 'j'): {1}, (0, 'k'): {1}, (0, 'l'): {1}, (0, 'm'): {1}, (0, 'n'): {1}, (0, 'o'): {1}, (0, 'p'): {1},
             (0, 'q'): {1}, (0, 'r'): {1}, (0, 's'): {1}, (0, 't'): {1}, (0, 'u'): {1}, (0, 'v'): {1}, (0, 'w'): {1},
             (0, 'x'): {1}, (0, 'y'): {1}, (0, 'z'): {1}, (0, '0'): {1}, (0, '1'): {1}, (0, '2'): {1}, (0, '3'): {1},
             (0, '4'): {1}, (0, '5'): {1}, (0, '6'): {1}, (0, '7'): {1}, (0, '8'): {1}, (0, '9'): {1}, (0, '_'): {1}}
        )
        self.assertDictEqual(
            self._convert("\W"),
            {(0, '\x00'): {1}, (0, '\x01'): {1}, (0, '\x02'): {1}, (0, '\x03'): {1}, (0, '\x04'): {1}, (0, '\x05'): {1},
             (0, '\x06'): {1}, (0, '\x07'): {1}, (0, '\x08'): {1}, (0, '\t'): {1}, (0, '\n'): {1}, (0, '\x0b'): {1},
             (0, '\x0c'): {1}, (0, '\r'): {1}, (0, '\x0e'): {1}, (0, '\x0f'): {1}, (0, '\x10'): {1}, (0, '\x11'): {1},
             (0, '\x12'): {1}, (0, '\x13'): {1}, (0, '\x14'): {1}, (0, '\x15'): {1}, (0, '\x16'): {1}, (0, '\x17'): {1},
             (0, '\x18'): {1}, (0, '\x19'): {1}, (0, '\x1a'): {1}, (0, '\x1b'): {1}, (0, '\x1c'): {1}, (0, '\x1d'): {1},
             (0, '\x1e'): {1}, (0, '\x1f'): {1}, (0, ' '): {1}, (0, '!'): {1}, (0, '"'): {1}, (0, '#'): {1},
             (0, '$'): {1}, (0, '%'): {1}, (0, '&'): {1}, (0, "'"): {1}, (0, '('): {1}, (0, ')'): {1}, (0, '*'): {1},
             (0, '+'): {1}, (0, ','): {1}, (0, '-'): {1}, (0, '.'): {1}, (0, '/'): {1}, (0, ':'): {1}, (0, ';'): {1},
             (0, '<'): {1}, (0, '='): {1}, (0, '>'): {1}, (0, '?'): {1}, (0, '@'): {1}, (0, '['): {1}, (0, '\\'): {1},
             (0, ']'): {1}, (0, '^'): {1}, (0, '_'): {1}, (0, '`'): {1}, (0, '{'): {1}, (0, '|'): {1}, (0, '}'): {1},
             (0, '~'): {1}, (0, '\x7f'): {1}, (0, '\x80'): {1}}
        )


class ConversionTestNFA(ut.TestCase):

    @classmethod
    def _convert(cls, re: str):
        enfa = aut.ENFA.get_enfa(re)
        nfa = aut.NFA.get_nfa(enfa)
        return nfa.transitions, nfa.end_states

    def test_basic(self):
        self.assertTupleEqual(
            self._convert("a"),
            (
                {
                    (0, 'a'): {1}
                },
                {1}
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
                    (0, 'a'): {1}, (0, 'b'): {1}
                },
                {1}
            )
        )


if __name__ == '__main__':
    ut.main()
