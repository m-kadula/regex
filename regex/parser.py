"""Regular expressions parser"""

from abc import ABC
from typing import NamedTuple, Iterator, Union, Any
from enum import Enum, auto
from json import dumps


class PartType(Enum):
    NORMAL = auto()
    SPECIAL = auto()
    TOKEN = auto()


class Part(NamedTuple):
    symbol: str
    sym_type: PartType


class Lexer:

    tokens: tuple[str] = '[', ']', '(', ')', '+', '*', '.', '?', '{', '}', '|', '\\'
    special: dict[str, str] = {'n': '\n', 't': '\t', '0': '\0', 'x': '\\x00'}
    substitute: tuple[str] = 's', 'S', 'd', 'D', 'a', 'A'

    def __init__(self, regular_expression: str):
        self.regex = regular_expression
        self.parts = self._tokenize(regular_expression)

    def __len__(self):
        return len(self.parts)

    def __getitem__(self, item: int) -> Part:
        return self.parts[item]

    def __iter__(self):
        self._cur_index = 0
        return self

    def __next__(self, __default=None) -> tuple[int, Part]:
        if self._cur_index >= len(self.parts):
            raise StopIteration
        self._cur_index += 1
        return self._cur_index - 1, self.parts[self._cur_index - 1]

    def rollback(self) -> None:
        if self._cur_index == 0:
            raise Exception  # TODO
        self._cur_index -= 1

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
        return Part(regex[0], PartType.TOKEN), 1

    @classmethod
    def _tokenize(cls, regular_expression: str) -> tuple[Part]:
        i = 0
        out: list[Part] = []
        while i < len(regular_expression):
            current = regular_expression[i]
            new: Part | None = None

            if current == '\\':
                if i + 1 >= len(regular_expression):
                    raise Exception  # TODO

                if regular_expression[i + 1] in cls.special or regular_expression[i + 1] in cls.substitute:
                    new, j = cls._handle_escape(regular_expression[i:])
                    i = i + j
                elif regular_expression[i + 1] in cls.tokens:
                    new = Part(regular_expression[i + 1], PartType.NORMAL)
                    i = i + 2
                else:
                    i = i + 1
                    continue

            elif current in cls.tokens:
                new, j = cls._handle_token(regular_expression[i:])
                i = i + j

            else:
                new = Part(current, PartType.NORMAL)
                i = i + 1

            assert new is not None
            out.append(new)

        return tuple([Part('(', PartType.TOKEN)] + out + [Part(')', PartType.TOKEN)])


class BaseNode(ABC):

    def repr(self) -> Any:  ...


class Symbol(BaseNode):

    def __init__(self, symbol: str, operator: Union[BaseNode, None]):
        self.symbol = symbol
        self.operator = operator

    def repr(self):
        if self.operator is not None:
            return f'<Symbol: {repr(self.symbol)}, {self.operator.repr()}>'
        else:
            return f'<Symbol: {repr(self.symbol)}>'


class SpecialSymbol(BaseNode):

    def __init__(self, symbol: str, operator: Union[BaseNode, None]):
        self.symbol = symbol
        self.operator = operator

    def repr(self):
        if self.operator is not None:
            return f'<SpecialSymbol: {repr(self.symbol)}, {self.operator.repr()}>'
        else:
            return f'<SpecialSymbol: {repr(self.symbol)}>'


class Concatenation(BaseNode):

    def __init__(self, contents: list[BaseNode]):
        self.contents = contents

    def repr(self):
        base = []
        for i in self.contents:
            base.append(i.repr())
        return {"<Concatenation>": base}


class OperatorType(Enum):
    STAR = auto()
    PLUS = auto()
    EXACT = auto()


class Operator(BaseNode):

    def __init__(self, op_type: OperatorType, operator: Union[str, tuple[int, int]]):
        self.op_type = op_type
        self.operator = operator

    def repr(self):
        return f"({repr(self.op_type)}, {repr(self.operator)})"


class Alternative(BaseNode):

    def __init__(self, operands: list[Concatenation], operator: Union[BaseNode, None]):
        self.operands = operands
        self.operator = operator

    def repr(self):
        base = []
        for i in self.operands:
            base.append(i.repr())
        return {f"<Alternative: {self.operator.repr() if self.operator is not None else 'None'}>": base}


class ParsingError(Exception):
    pass


class Parser:

    def __init__(self, lexer: Lexer):
        self.root = self._parse(lexer)

    def __repr__(self):
        return dumps(self.root.repr(), indent=4)

    @classmethod
    def _parse(cls, regex: Lexer) -> BaseNode:
        iterator = iter(regex)
        out = cls._parse_group(iterator)
        try:
            next(iterator)
        except StopIteration:
            return out
        else:
            raise ParsingError  # TODO

    @classmethod
    def _parse_operator(cls, iterator: Iterator[tuple[int, Part]]) -> Operator | None:
        try:
            str_index, current = next(iterator)
        except StopIteration:
            return None

        if current.sym_type != PartType.TOKEN or current.symbol not in ['*', '+', '?', '{']:
            iterator.rollback()
            return None

        elif current.symbol == '{':
            number_one_str = ''
            while True:
                str_index, current = next(iterator)
                if current.symbol.isnumeric():
                    number_one_str += current.symbol
                elif current.symbol == ',':
                    two_numbers = True
                    break
                elif current.symbol == '}':
                    two_numbers = False
                    break
                else:
                    raise ParsingError  # TODO
            number_one = int(number_one_str)
            if two_numbers:
                number_two_str = ''
                while True:
                    str_index, current = next(iterator)
                    if current.symbol.isnumeric():
                        number_two_str += current.symbol
                    elif current.symbol == '}':
                        break
                    else:
                        raise ParsingError  # TODO
                number_two = int(number_two_str)
                range_tuple = (number_one, number_two)
            else:
                range_tuple = (number_one, number_one)
            return Operator(OperatorType.EXACT, range_tuple)

        elif current.symbol == '?':
            return Operator(OperatorType.EXACT, (0, 1))

        elif current.symbol == '*':
            return Operator(OperatorType.STAR, '*')

        elif current.symbol == '+':
            return Operator(OperatorType.PLUS, '+')

        else:
            raise Exception  # TODO

    @classmethod
    def _parse_alter_set(cls, iterator: Iterator[tuple[int, Part]]) -> Alternative:  # TODO
        ...

    @classmethod
    def _parse_concatenation(cls, iterator: Iterator[tuple[int, Part]]) -> Concatenation:
        out = Concatenation(contents=[])
        while True:
            str_index, current = next(iterator)

            match current.sym_type:
                case PartType.TOKEN:
                    if current.symbol == '(':
                        iterator.rollback()
                        cur = cls._parse_group(iterator)
                        cur.operator = cls._parse_operator(iterator)
                        out.contents.append(cur)
                    elif current.symbol == '[':
                        ...
                    elif current.symbol in ['|', ')']:
                        iterator.rollback()
                        break
                    else:
                        raise ParsingError  # TODO

                case PartType.NORMAL:
                    cur = Symbol(
                        symbol=current.symbol,
                        operator=cls._parse_operator(iterator)
                    )
                    out.contents.append(cur)

                case PartType.SPECIAL:
                    cur = SpecialSymbol(
                        symbol=current.symbol,
                        operator=cls._parse_operator(iterator)
                    )
                    out.contents.append(cur)

        return out

    @classmethod
    def _parse_group(cls, iterator: Iterator[tuple[int, Part]]) -> Alternative:
        out = Alternative(operands=[], operator=None)
        str_index, current = next(iterator)
        assert current.symbol == '(' and current.sym_type == PartType.TOKEN
        while True:
            str_index, current = next(iterator)

            if current.symbol == ')' and current.sym_type == PartType.TOKEN:
                break
            elif current.symbol == '|' and current.sym_type == PartType.TOKEN:
                continue
            else:
                iterator.rollback()
                cur = cls._parse_concatenation(iterator)
                out.operands.append(cur)

        return out


if __name__ == '__main__':
    re = r"((1|2|3)(\+|-\s)?)+"
    lex = Lexer(re)
    pars = Parser(lex)
    with open('out.json', 'w') as f:
        f.write(repr(pars))
