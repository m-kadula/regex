"""Tests for the lexer and the parser"""

import unittest as ut
import regex.parser as par


class LexerTest(ut.TestCase):

    def test_basic(self):
        re = r'b|[a-zA-Z]+\(\d+\)'
        lexer = par.Lexer(re)
        self.assertTrue(len(lexer) == 17)
        for _, pair in lexer:
            if pair.symbol in par.Lexer.tokens:
                self.assertTrue(pair.sym_type == par.PartType.TOKEN or pair.symbol in '()')
            elif pair.symbol != 'd':
                self.assertTrue(pair.sym_type == par.PartType.NORMAL)


class ParserTest(ut.TestCase):

    prt = False

    @classmethod
    def _parse(cls, re: str):
        pars = par.Parser(par.Lexer(re))
        if cls.prt:
            with open('out.txt', 'a') as f:
                f.seek(0, 2)
                print(pars, file=f, flush=True)
        return pars.get_tree()

    def test_operator(self):
        self.assertEqual(
            self._parse(r"a+"),
            {'type': 'alternative', 'operator': None, 'contents': [{'type': 'symbol', 'operator': '+', 'value': 'a'}]}
        )
        self.assertEqual(
            self._parse(r"a*"),
            {'type': 'alternative', 'operator': None, 'contents': [{'type': 'symbol', 'operator': '*', 'value': 'a'}]}
        )
        self.assertEqual(
            self._parse(r"a?"),
            {'type': 'alternative', 'operator': None, 'contents': [{'type': 'symbol', 'operator': (0, 1), 'value': 'a'}]}
        )
        self.assertEqual(
            self._parse(r"a{12}"),
            {'type': 'alternative', 'operator': None, 'contents': [{'type': 'symbol', 'operator': (12, 12), 'value': 'a'}]}
        )
        self.assertEqual(
            self._parse(r"a{12,15}"),
            {'type': 'alternative', 'operator': None,
             'contents': [{'type': 'symbol', 'operator': (12, 15), 'value': 'a'}]}
        )
        self.assertEqual(
            self._parse(r"a\{12,15\}"),
            {
                "type": "alternative",
                "operator": None,
                "contents": [
                    {
                        "type": "concatenation",
                        "operator": None,
                        "contents": [
                            {
                                "type": "symbol",
                                "operator": None,
                                "value": "a"
                            },
                            {
                                "type": "symbol",
                                "operator": None,
                                "value": "{"
                            },
                            {
                                "type": "symbol",
                                "operator": None,
                                "value": "1"
                            },
                            {
                                "type": "symbol",
                                "operator": None,
                                "value": "2"
                            },
                            {
                                "type": "symbol",
                                "operator": None,
                                "value": ","
                            },
                            {
                                "type": "symbol",
                                "operator": None,
                                "value": "1"
                            },
                            {
                                "type": "symbol",
                                "operator": None,
                                "value": "5"
                            },
                            {
                                "type": "symbol",
                                "operator": None,
                                "value": "}"
                            }
                        ]
                    }
                ]
            }
        )
        self.assertEqual(
            self._parse(r"(ab+){12,15}"),
            {
                'type': 'alternative',
                'operator': None,
                'contents': [
                    {
                        "type": "concatenation",
                        "operator": (12, 15),
                        "contents": [
                            {
                                "type": "symbol",
                                "operator": None,
                                "value": "a"
                            },
                            {
                                "type": "symbol",
                                "operator": "+",
                                "value": "b"
                            }
                        ]
                    }
                ]
            }
        )

    def test_alt_set(self):
        null = None
        self.assertEqual(
            self._parse(r"[-0\s12a-cA-C]+"),
            {
                "type": "alternative",
                "operator": null,
                "contents": [
                    {
                        "type": "alternative",
                        "operator": "+",
                        "contents": [
                            {
                                "type": "symbol",
                                "operator": null,
                                "value": "-"
                            },
                            {
                                "type": "symbol",
                                "operator": null,
                                "value": "0"
                            },
                            {
                                "type": "special_symbol",
                                "operator": null,
                                "value": "s"
                            },
                            {
                                "type": "symbol",
                                "operator": null,
                                "value": "1"
                            },
                            {
                                "type": "symbol",
                                "operator": null,
                                "value": "2"
                            },
                            {
                                "type": "symbol",
                                "operator": null,
                                "value": "a"
                            },
                            {
                                "type": "symbol",
                                "operator": null,
                                "value": "b"
                            },
                            {
                                "type": "symbol",
                                "operator": null,
                                "value": "c"
                            },
                            {
                                "type": "symbol",
                                "operator": null,
                                "value": "A"
                            },
                            {
                                "type": "symbol",
                                "operator": null,
                                "value": "B"
                            },
                            {
                                "type": "symbol",
                                "operator": null,
                                "value": "C"
                            }
                        ]
                    }
                ]
            }
        )

    def test_alternative(self):
        self.assertEqual(
            self._parse("a|b|c"),
            {
                "type": "alternative",
                "operator": None,
                "contents": [
                    {
                        "type": "symbol",
                        'operator': None,
                        "value": 'a'
                    },
                    {
                        "type": "symbol",
                        'operator': None,
                        "value": 'b'
                    },
                    {
                        "type": "symbol",
                        'operator': None,
                        "value": 'c'
                    }
                ]
            }
        )
        self.assertEqual(
            self._parse("(a|b{4,5}|c*)+"),
            {
                "type": "alternative",
                "operator": None,
                "contents": [
                    {
                        "type": "alternative",
                        "operator": "+",
                        "contents": [
                            {
                                "type": "symbol",
                                'operator': None,
                                "value": 'a'
                            },
                            {
                                "type": "symbol",
                                'operator': (4, 5),
                                "value": 'b'
                            },
                            {
                                "type": "symbol",
                                'operator': "*",
                                "value": 'c'
                            }
                        ]
                    }
                ]
            }
        )
        self.assertEqual(
            self._parse("(aa|b)|(c|dd)"),
            {
                "type": "alternative",
                "operator": None,
                "contents": [
                    {
                        "type": "alternative",
                        "operator": None,
                        "contents": [
                            {
                                "type": "concatenation",
                                "operator": None,
                                "contents": [
                                    {
                                        "type": "symbol",
                                        "operator": None,
                                        "value": "a"
                                    },
                                    {
                                        "type": "symbol",
                                        "operator": None,
                                        "value": "a"
                                    }
                                ]
                            },
                            {
                                "type": "symbol",
                                "operator": None,
                                "value": "b"
                            }
                        ]
                    },
                    {
                        "type": "alternative",
                        "operator": None,
                        "contents": [
                            {
                                "type": "symbol",
                                "operator": None,
                                "value": "c"
                            },
                            {
                                "type": "concatenation",
                                "operator": None,
                                "contents": [
                                    {
                                        "type": "symbol",
                                        "operator": None,
                                        "value": "d"
                                    },
                                    {
                                        "type": "symbol",
                                        "operator": None,
                                        "value": "d"
                                    }
                                ]
                            }
                        ]
                    }
                ]
            }
        )

    def test_concatenation(self):
        self.assertEqual(
            self._parse("ab+(c)d(e)fg"),
            {
                "type": "alternative",
                "operator": None,
                "contents": [
                    {
                        "type": "concatenation",
                        "operator": None,
                        "contents": [
                            {
                                "type": "symbol",
                                "operator": None,
                                "value": "a"
                            },
                            {
                                "type": "symbol",
                                "operator": "+",
                                "value": "b"
                            },
                            {
                                "type": "symbol",
                                "operator": None,
                                "value": "c"
                            },
                            {
                                "type": "symbol",
                                "operator": None,
                                "value": "d"
                            },
                            {
                                "type": "symbol",
                                "operator": None,
                                "value": "e"
                            },
                            {
                                "type": "symbol",
                                "operator": None,
                                "value": "f"
                            },
                            {
                                "type": "symbol",
                                "operator": None,
                                "value": "g"
                            },
                        ]
                    }
                ]
            }
        )

    def test_general_one(self):
        null = None
        self.assertEqual(
            self._parse(r"((\\d{3})(\\.|-))?(\\d{3}\y)(\\.|-)(\\d{4})"),
            {
                "type": "alternative",
                "operator": null,
                "contents": [
                    {
                        "type": "concatenation",
                        "operator": null,
                        "contents": [
                            {
                                "type": "concatenation",
                                "operator": (
                                    0,
                                    1
                                ),
                                "contents": [
                                    {
                                        "type": "concatenation",
                                        "operator": null,
                                        "contents": [
                                            {
                                                "type": "symbol",
                                                "operator": null,
                                                "value": "\\"
                                            },
                                            {
                                                "type": "symbol",
                                                "operator": (
                                                    3,
                                                    3
                                                ),
                                                "value": "d"
                                            }
                                        ]
                                    },
                                    {
                                        "type": "alternative",
                                        "operator": null,
                                        "contents": [
                                            {
                                                "type": "concatenation",
                                                "operator": null,
                                                "contents": [
                                                    {
                                                        "type": "symbol",
                                                        "operator": null,
                                                        "value": "\\"
                                                    },
                                                    {
                                                        "type": "special_symbol",
                                                        "operator": null,
                                                        "value": "."
                                                    }
                                                ]
                                            },
                                            {
                                                "type": "symbol",
                                                "operator": null,
                                                "value": "-"
                                            }
                                        ]
                                    }
                                ]
                            },
                            {
                                "type": "concatenation",
                                "operator": null,
                                "contents": [
                                    {
                                        "type": "symbol",
                                        "operator": null,
                                        "value": "\\"
                                    },
                                    {
                                        "type": "symbol",
                                        "operator": (
                                            3,
                                            3
                                        ),
                                        "value": "d"
                                    },
                                    {
                                        "type": "symbol",
                                        "operator": null,
                                        "value": "y"
                                    }
                                ]
                            },
                            {
                                "type": "alternative",
                                "operator": null,
                                "contents": [
                                    {
                                        "type": "concatenation",
                                        "operator": null,
                                        "contents": [
                                            {
                                                "type": "symbol",
                                                "operator": null,
                                                "value": "\\"
                                            },
                                            {
                                                "type": "special_symbol",
                                                "operator": null,
                                                "value": "."
                                            }
                                        ]
                                    },
                                    {
                                        "type": "symbol",
                                        "operator": null,
                                        "value": "-"
                                    }
                                ]
                            },
                            {
                                "type": "concatenation",
                                "operator": null,
                                "contents": [
                                    {
                                        "type": "symbol",
                                        "operator": null,
                                        "value": "\\"
                                    },
                                    {
                                        "type": "symbol",
                                        "operator": (
                                            4,
                                            4
                                        ),
                                        "value": "d"
                                    }
                                ]
                            }
                        ]
                    }
                ]
            }
        )

    def test_general_two(self):
        null = None
        self.assertEqual(
            self._parse(r"([a-z0-9_\.]+)@([-\da-z\.]+)\.([a-z\.]{2,6})"),
            {
                "type": "alternative",
                "operator": null,
                "contents": [
                    {
                        "type": "concatenation",
                        "operator": null,
                        "contents": [
                            {
                                "type": "alternative",
                                "operator": null,
                                "contents": [
                                    {
                                        "type": "alternative",
                                        "operator": "+",
                                        "contents": [
                                            {
                                                "type": "symbol",
                                                "operator": null,
                                                "value": "a"
                                            },
                                            {
                                                "type": "symbol",
                                                "operator": null,
                                                "value": "b"
                                            },
                                            {
                                                "type": "symbol",
                                                "operator": null,
                                                "value": "c"
                                            },
                                            {
                                                "type": "symbol",
                                                "operator": null,
                                                "value": "d"
                                            },
                                            {
                                                "type": "symbol",
                                                "operator": null,
                                                "value": "e"
                                            },
                                            {
                                                "type": "symbol",
                                                "operator": null,
                                                "value": "f"
                                            },
                                            {
                                                "type": "symbol",
                                                "operator": null,
                                                "value": "g"
                                            },
                                            {
                                                "type": "symbol",
                                                "operator": null,
                                                "value": "h"
                                            },
                                            {
                                                "type": "symbol",
                                                "operator": null,
                                                "value": "i"
                                            },
                                            {
                                                "type": "symbol",
                                                "operator": null,
                                                "value": "j"
                                            },
                                            {
                                                "type": "symbol",
                                                "operator": null,
                                                "value": "k"
                                            },
                                            {
                                                "type": "symbol",
                                                "operator": null,
                                                "value": "l"
                                            },
                                            {
                                                "type": "symbol",
                                                "operator": null,
                                                "value": "m"
                                            },
                                            {
                                                "type": "symbol",
                                                "operator": null,
                                                "value": "n"
                                            },
                                            {
                                                "type": "symbol",
                                                "operator": null,
                                                "value": "o"
                                            },
                                            {
                                                "type": "symbol",
                                                "operator": null,
                                                "value": "p"
                                            },
                                            {
                                                "type": "symbol",
                                                "operator": null,
                                                "value": "q"
                                            },
                                            {
                                                "type": "symbol",
                                                "operator": null,
                                                "value": "r"
                                            },
                                            {
                                                "type": "symbol",
                                                "operator": null,
                                                "value": "s"
                                            },
                                            {
                                                "type": "symbol",
                                                "operator": null,
                                                "value": "t"
                                            },
                                            {
                                                "type": "symbol",
                                                "operator": null,
                                                "value": "u"
                                            },
                                            {
                                                "type": "symbol",
                                                "operator": null,
                                                "value": "v"
                                            },
                                            {
                                                "type": "symbol",
                                                "operator": null,
                                                "value": "w"
                                            },
                                            {
                                                "type": "symbol",
                                                "operator": null,
                                                "value": "x"
                                            },
                                            {
                                                "type": "symbol",
                                                "operator": null,
                                                "value": "y"
                                            },
                                            {
                                                "type": "symbol",
                                                "operator": null,
                                                "value": "z"
                                            },
                                            {
                                                "type": "symbol",
                                                "operator": null,
                                                "value": "0"
                                            },
                                            {
                                                "type": "symbol",
                                                "operator": null,
                                                "value": "1"
                                            },
                                            {
                                                "type": "symbol",
                                                "operator": null,
                                                "value": "2"
                                            },
                                            {
                                                "type": "symbol",
                                                "operator": null,
                                                "value": "3"
                                            },
                                            {
                                                "type": "symbol",
                                                "operator": null,
                                                "value": "4"
                                            },
                                            {
                                                "type": "symbol",
                                                "operator": null,
                                                "value": "5"
                                            },
                                            {
                                                "type": "symbol",
                                                "operator": null,
                                                "value": "6"
                                            },
                                            {
                                                "type": "symbol",
                                                "operator": null,
                                                "value": "7"
                                            },
                                            {
                                                "type": "symbol",
                                                "operator": null,
                                                "value": "8"
                                            },
                                            {
                                                "type": "symbol",
                                                "operator": null,
                                                "value": "9"
                                            },
                                            {
                                                "type": "symbol",
                                                "operator": null,
                                                "value": "_"
                                            },
                                            {
                                                "type": "symbol",
                                                "operator": null,
                                                "value": "."
                                            }
                                        ]
                                    }
                                ]
                            },
                            {
                                "type": "symbol",
                                "operator": null,
                                "value": "@"
                            },
                            {
                                "type": "alternative",
                                "operator": null,
                                "contents": [
                                    {
                                        "type": "alternative",
                                        "operator": "+",
                                        "contents": [
                                            {
                                                "type": "symbol",
                                                "operator": null,
                                                "value": "-"
                                            },
                                            {
                                                "type": "special_symbol",
                                                "operator": null,
                                                "value": "d"
                                            },
                                            {
                                                "type": "symbol",
                                                "operator": null,
                                                "value": "a"
                                            },
                                            {
                                                "type": "symbol",
                                                "operator": null,
                                                "value": "b"
                                            },
                                            {
                                                "type": "symbol",
                                                "operator": null,
                                                "value": "c"
                                            },
                                            {
                                                "type": "symbol",
                                                "operator": null,
                                                "value": "d"
                                            },
                                            {
                                                "type": "symbol",
                                                "operator": null,
                                                "value": "e"
                                            },
                                            {
                                                "type": "symbol",
                                                "operator": null,
                                                "value": "f"
                                            },
                                            {
                                                "type": "symbol",
                                                "operator": null,
                                                "value": "g"
                                            },
                                            {
                                                "type": "symbol",
                                                "operator": null,
                                                "value": "h"
                                            },
                                            {
                                                "type": "symbol",
                                                "operator": null,
                                                "value": "i"
                                            },
                                            {
                                                "type": "symbol",
                                                "operator": null,
                                                "value": "j"
                                            },
                                            {
                                                "type": "symbol",
                                                "operator": null,
                                                "value": "k"
                                            },
                                            {
                                                "type": "symbol",
                                                "operator": null,
                                                "value": "l"
                                            },
                                            {
                                                "type": "symbol",
                                                "operator": null,
                                                "value": "m"
                                            },
                                            {
                                                "type": "symbol",
                                                "operator": null,
                                                "value": "n"
                                            },
                                            {
                                                "type": "symbol",
                                                "operator": null,
                                                "value": "o"
                                            },
                                            {
                                                "type": "symbol",
                                                "operator": null,
                                                "value": "p"
                                            },
                                            {
                                                "type": "symbol",
                                                "operator": null,
                                                "value": "q"
                                            },
                                            {
                                                "type": "symbol",
                                                "operator": null,
                                                "value": "r"
                                            },
                                            {
                                                "type": "symbol",
                                                "operator": null,
                                                "value": "s"
                                            },
                                            {
                                                "type": "symbol",
                                                "operator": null,
                                                "value": "t"
                                            },
                                            {
                                                "type": "symbol",
                                                "operator": null,
                                                "value": "u"
                                            },
                                            {
                                                "type": "symbol",
                                                "operator": null,
                                                "value": "v"
                                            },
                                            {
                                                "type": "symbol",
                                                "operator": null,
                                                "value": "w"
                                            },
                                            {
                                                "type": "symbol",
                                                "operator": null,
                                                "value": "x"
                                            },
                                            {
                                                "type": "symbol",
                                                "operator": null,
                                                "value": "y"
                                            },
                                            {
                                                "type": "symbol",
                                                "operator": null,
                                                "value": "z"
                                            },
                                            {
                                                "type": "symbol",
                                                "operator": null,
                                                "value": "."
                                            }
                                        ]
                                    }
                                ]
                            },
                            {
                                "type": "symbol",
                                "operator": null,
                                "value": "."
                            },
                            {
                                "type": "alternative",
                                "operator": null,
                                "contents": [
                                    {
                                        "type": "alternative",
                                        "operator": (
                                            2,
                                            6
                                        ),
                                        "contents": [
                                            {
                                                "type": "symbol",
                                                "operator": null,
                                                "value": "a"
                                            },
                                            {
                                                "type": "symbol",
                                                "operator": null,
                                                "value": "b"
                                            },
                                            {
                                                "type": "symbol",
                                                "operator": null,
                                                "value": "c"
                                            },
                                            {
                                                "type": "symbol",
                                                "operator": null,
                                                "value": "d"
                                            },
                                            {
                                                "type": "symbol",
                                                "operator": null,
                                                "value": "e"
                                            },
                                            {
                                                "type": "symbol",
                                                "operator": null,
                                                "value": "f"
                                            },
                                            {
                                                "type": "symbol",
                                                "operator": null,
                                                "value": "g"
                                            },
                                            {
                                                "type": "symbol",
                                                "operator": null,
                                                "value": "h"
                                            },
                                            {
                                                "type": "symbol",
                                                "operator": null,
                                                "value": "i"
                                            },
                                            {
                                                "type": "symbol",
                                                "operator": null,
                                                "value": "j"
                                            },
                                            {
                                                "type": "symbol",
                                                "operator": null,
                                                "value": "k"
                                            },
                                            {
                                                "type": "symbol",
                                                "operator": null,
                                                "value": "l"
                                            },
                                            {
                                                "type": "symbol",
                                                "operator": null,
                                                "value": "m"
                                            },
                                            {
                                                "type": "symbol",
                                                "operator": null,
                                                "value": "n"
                                            },
                                            {
                                                "type": "symbol",
                                                "operator": null,
                                                "value": "o"
                                            },
                                            {
                                                "type": "symbol",
                                                "operator": null,
                                                "value": "p"
                                            },
                                            {
                                                "type": "symbol",
                                                "operator": null,
                                                "value": "q"
                                            },
                                            {
                                                "type": "symbol",
                                                "operator": null,
                                                "value": "r"
                                            },
                                            {
                                                "type": "symbol",
                                                "operator": null,
                                                "value": "s"
                                            },
                                            {
                                                "type": "symbol",
                                                "operator": null,
                                                "value": "t"
                                            },
                                            {
                                                "type": "symbol",
                                                "operator": null,
                                                "value": "u"
                                            },
                                            {
                                                "type": "symbol",
                                                "operator": null,
                                                "value": "v"
                                            },
                                            {
                                                "type": "symbol",
                                                "operator": null,
                                                "value": "w"
                                            },
                                            {
                                                "type": "symbol",
                                                "operator": null,
                                                "value": "x"
                                            },
                                            {
                                                "type": "symbol",
                                                "operator": null,
                                                "value": "y"
                                            },
                                            {
                                                "type": "symbol",
                                                "operator": null,
                                                "value": "z"
                                            },
                                            {
                                                "type": "symbol",
                                                "operator": null,
                                                "value": "."
                                            }
                                        ]
                                    }
                                ]
                            }
                        ]
                    }
                ]
            }
        )

    def test_general_three(self):
        null = None
        self.assertEqual(
            self._parse(r"((1|2|3)(\++-{89,90}\s).*)+|x"),
            {
                "type": "alternative",
                "operator": null,
                "contents": [
                    {
                        "type": "concatenation",
                        "operator": "+",
                        "contents": [
                            {
                                "type": "alternative",
                                "operator": null,
                                "contents": [
                                    {
                                        "type": "symbol",
                                        "operator": null,
                                        "value": "1"
                                    },
                                    {
                                        "type": "symbol",
                                        "operator": null,
                                        "value": "2"
                                    },
                                    {
                                        "type": "symbol",
                                        "operator": null,
                                        "value": "3"
                                    }
                                ]
                            },
                            {
                                "type": "concatenation",
                                "operator": null,
                                "contents": [
                                    {
                                        "type": "symbol",
                                        "operator": "+",
                                        "value": "+"
                                    },
                                    {
                                        "type": "symbol",
                                        "operator": (
                                            89,
                                            90
                                        ),
                                        "value": "-"
                                    },
                                    {
                                        "type": "special_symbol",
                                        "operator": null,
                                        "value": "s"
                                    }
                                ]
                            },
                            {
                                "type": "special_symbol",
                                "operator": "*",
                                "value": "."
                            }
                        ]
                    },
                    {
                        "type": "symbol",
                        "operator": null,
                        "value": "x"
                    }
                ]
            }
        )

    def test_errors(self):
        self.assertRaises(
            par.ParsingError,
            self._parse,
            r"a++"
        )
        self.assertRaises(
            ValueError,
            self._parse,
            r"[c-a]"
        )
        self.assertRaises(
            par.ParsingError,
            self._parse,
            r"[ab(c)]"
        )
        self.assertRaises(
            ValueError,
            self._parse,
            r"a{10,0}"
        )
        self.assertRaises(
            par.ParsingError,
            self._parse,
            r"a{10.,1}"
        )
        self.assertRaises(
            par.ParsingError,
            self._parse,
            r"a+(+)"
        )
