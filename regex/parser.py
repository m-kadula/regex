"""Regular expressions parser"""

from typing import NamedTuple
from enum import Enum, auto


class PartType(Enum):
    NORMAL = auto()
    SPECIAL = auto()
    TOKEN = auto()


class Part(NamedTuple):
    symbol: str
    sym_type: PartType


class Lexer:

    tokens: tuple[str] = '[', '[^', ']', '(', '(?:', ')', '+', '*', '.', '?', '{', '}'
    special: dict[str, str] = {'n': '\n', 't': '\t', '0': '\0', 'x': '\x00'}
    substitute: tuple[str] = 's', 'S', 'd', 'D', 'a', 'A'

    def __init__(self, regular_expression: str):
        self.regex = regular_expression
        self.parts = self._tokenize(regular_expression)

    def __len__(self):
        return len(self.parts)

    def __getitem__(self, item: int) -> Part:
        return self.parts[item]

    @classmethod
    def _handle_escape(cls, regex: str) -> (Part, int):
        if regex[1] in cls.special:
            if regex[1] == 'x':
                sym = chr(int(regex[2:4], 16))
                return Part(sym, PartType.NORMAL), 4
            else:
                sym = cls.special[regex[1]]
                return Part(sym, PartType.NORMAL), 2
        else:
            return Part(regex[1], PartType.SPECIAL), 2

    @classmethod
    def _handle_token(cls, regex: str) -> (Part, int):
        if len(regex) >= 3 and regex[:3] == '(?:':
            return Part(regex[:3], PartType.TOKEN), 3
        elif len(regex) >= 2 and regex[:2] == '[^':
            return Part(regex[:2], PartType.TOKEN), 2
        else:
            return Part(regex[0], PartType.TOKEN), 1

    @classmethod
    def _tokenize(cls, regular_expression: str) -> tuple[Part]:
        i = 0
        out: list[Part] = []
        while i < len(regular_expression):
            current = regular_expression[i]
            new: Part | None = None

            if current == '\\':
                if i + 1 < len(regular_expression):
                    if regular_expression[i + 1] in cls.special or regular_expression[i + 1] in cls.substitute:
                        new, j = cls._handle_escape(regular_expression[i:])
                        i = i + j
                    elif regular_expression[i + 1] in cls.tokens:
                        new = Part(regular_expression[i + 1], PartType.NORMAL)
                        i = i + 2
                    else:
                        new = Part('\\', PartType.NORMAL)
                        i = i + 1
                else:
                    new = Part('\\', PartType.NORMAL)
                    i = i + 1

            elif current in cls.tokens:
                new, j = cls._handle_token(regular_expression[i:])
                i = i + j

            else:
                new = Part(current, PartType.NORMAL)
                i = i + 1

            assert new is not None
            out.append(new)

        return tuple(out)


def parse(regular_expression: str):
    ...
