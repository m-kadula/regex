"""Regular expressions parser"""

from abc import ABC
from typing import NamedTuple, Union
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

    tokens: tuple[str] = '[', ']', '(', ')', '+', '*', '?', '{', '}', '|', '\\', '.'
    special: dict[str, str] = {'n': '\n', 't': '\t', '0': '\0', 'x': '\x00'}
    substitute: tuple[str] = 's', 'd', 'w', 'S', 'D', 'W'

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

    def __next__(self) -> tuple[int, Part]:
        if self._cur_index >= len(self.parts):
            raise StopIteration
        self._cur_index += 1
        return self._cur_index - 1, self.parts[self._cur_index - 1]

    def rollback(self) -> None:
        if self._cur_index == 0:
            raise IndexError("Attempted rollback at index 0.")
        self._cur_index -= 1

    @classmethod
    def _check_brackets(cls, regex: list[Part]) -> bool:
        stack = []
        counterpart = {')': '(', ']': '['}
        for part in regex:
            if part.sym_type != PartType.TOKEN:
                continue
            if part.symbol in ['(', '[']:
                stack.append(part.symbol)
            elif part.symbol in [')', ']']:
                if len(stack) == 0 or stack[-1] != counterpart[part.symbol]:
                    return False
                stack.pop()
        return len(stack) == 0

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
        if regex[0] == '.':
            return Part(regex[0], PartType.SPECIAL), 1
        else:
            return Part(regex[0], PartType.TOKEN), 1

    @classmethod
    def _tokenize(cls, regular_expression: str) -> tuple[Part]:
        i = 0
        out: list[Part] = []
        while i < len(regular_expression):
            current = regular_expression[i]

            if current == '\\':
                if i + 1 >= len(regular_expression):
                    raise SyntaxError("Trailing '\\' symbol.")

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

        if not cls._check_brackets(out):
            raise SyntaxError("Unbalanced brackets.")
        return tuple([Part('(', PartType.TOKEN)] + out + [Part(')', PartType.TOKEN)])


class OperatorType(Enum):
    STAR = auto()
    PLUS = auto()
    EXACT = auto()


class Operator:

    def __init__(self, op_type: OperatorType, operator: Union[str, tuple[int, int]]):
        self.op_type = op_type
        self.operator = operator

    def repr(self):
        return self.operator


class BaseNode(ABC):

    def repr(self) -> dict:  ...


class Symbol(BaseNode):

    def __init__(self, symbol: str, operator: Union[BaseNode, None]):
        self.symbol = symbol
        self.operator = operator

    def repr(self):
        op = self.operator.repr() if self.operator is not None else None
        return {"type": "symbol", "operator": op, "value": self.symbol}


class SpecialSymbol(BaseNode):

    def __init__(self, symbol: str, operator: Union[BaseNode, None]):
        self.symbol = symbol
        self.operator = operator

    def repr(self):
        op = self.operator.repr() if self.operator is not None else None
        return {"type": "special_symbol", "operator": op, "value": self.symbol}


class Alternative(BaseNode):

    def __init__(self, contents: list[BaseNode], operator: Union[BaseNode, None]):
        self.contents = contents
        self.operator = operator

    def repr(self):
        base = []
        for i in self.contents:
            base.append(i.repr())
        op = self.operator.repr() if self.operator is not None else None
        return {"type": "alternative", "operator": op, "contents": base}


class Concatenation(BaseNode):

    def __init__(self, contents: list[BaseNode], operator: Union[BaseNode, None]):
        self.contents = contents
        self.operator = operator

    def repr(self):
        base = []
        for i in self.contents:
            base.append(i.repr())
        op = self.operator.repr() if self.operator is not None else None
        return {"type": "concatenation", "operator": op, "contents": base}


class ParsingError(Exception):

    def __init__(self, msg: str, index: int | None = None):
        super().__init__(f"({index}): " + msg if index is not None else msg)


class Parser:

    def __init__(self, lexer: Lexer):
        self.root = self._parse(lexer)

    def __repr__(self):
        return dumps(self.root.repr(), indent=4)

    def get_tree(self):
        return self.root.repr()

    @classmethod
    def _parse(cls, lexer: Lexer) -> BaseNode:
        iter(lexer)
        out = cls._parse_group(lexer)
        assert lexer._cur_index == len(lexer)
        return out

    @classmethod
    def _parse_number(cls, iterator: Lexer) -> int:
        number_str = ''
        while True:
            str_index, current = next(iterator)
            if current.symbol.isdigit():
                number_str += current.symbol
            else:
                iterator.rollback()
                break
        return int(number_str)

    @classmethod
    def _parse_operator(cls, iterator: Lexer) -> Operator | None:
        str_index, current = next(iterator)

        if current.sym_type != PartType.TOKEN or current.symbol not in ['*', '+', '?', '{']:
            iterator.rollback()
            return None

        elif current.symbol == '{':
            number_one = cls._parse_number(iterator)
            str_index, current = next(iterator)
            if current.symbol == ',':
                number_two = cls._parse_number(iterator)
                if number_two < number_one:
                    raise ValueError("The second number has to be grater than the first number.", str_index - 1)
                range_tuple = (number_one, number_two)
                str_index, current = next(iterator)
            else:
                range_tuple = (number_one, number_one)
            if current.symbol != '}' or current.sym_type != PartType.TOKEN:
                raise ParsingError(f"Illegal symbol '{current.symbol}'.", str_index - 1)
            return Operator(OperatorType.EXACT, range_tuple)

        elif current.symbol == '?':
            return Operator(OperatorType.EXACT, (0, 1))

        elif current.symbol == '*':
            return Operator(OperatorType.STAR, '*')

        elif current.symbol == '+':
            return Operator(OperatorType.PLUS, '+')

        else:
            raise RuntimeError

    @classmethod
    def _parse_alter_set(cls, iterator: Lexer) -> Alternative:
        out = Alternative(contents=[], operator=None)
        str_index, current = next(iterator)
        assert current.sym_type == PartType.TOKEN and current.symbol == '['
        while True:
            str_index, current = next(iterator)

            if current.sym_type == PartType.TOKEN:
                if current.symbol == ']':
                    break
                else:
                    raise ParsingError(f"'{current.symbol}' is not allowed inside '[]'.", str_index - 1)

            elif current.sym_type == PartType.NORMAL:
                if current.symbol == '-' and len(out.contents) > 0:
                    previous = out.contents[-1]
                    _, following = next(iterator)
                    if following.sym_type != PartType.NORMAL or isinstance(previous, SpecialSymbol):
                        raise ParsingError("Range has to be between two ASCII symbols.", str_index - 1)
                    assert isinstance(previous, Symbol)

                    first = ord(previous.symbol)
                    second = ord(following.symbol)
                    if first >= second:
                        raise ValueError(f"The ASCII value of '{chr(first)}' should be "
                                         f"lesser than the ASCII value of '{chr(second)}'", str_index - 1)
                    for i in range(first + 1, second + 1):
                        out.contents.append(Symbol(chr(i), None))

                else:
                    out.contents.append(Symbol(current.symbol, None))

            elif current.sym_type == PartType.SPECIAL:
                out.contents.append(SpecialSymbol(current.symbol, None))

        return out

    @classmethod
    def _parse_concatenation(cls, iterator: Lexer) -> Concatenation:
        out = Concatenation(contents=[], operator=None)
        while True:
            str_index, current = next(iterator)

            if current.sym_type == PartType.TOKEN:

                if current.symbol == '(':
                    iterator.rollback()
                    cur = cls._parse_group(iterator)
                    if len(cur.contents) == 1 and cur.contents[0].operator is None:
                        cur = cur.contents[0]
                    cur.operator = cls._parse_operator(iterator)
                    out.contents.append(cur)
                elif current.symbol == '[':
                    iterator.rollback()
                    cur = cls._parse_alter_set(iterator)
                    if len(cur.contents) == 1 and cur.contents[0].operator is None:
                        cur = cur.contents[0]
                    cur.operator = cls._parse_operator(iterator)
                    out.contents.append(cur)
                elif current.symbol in ['|', ')']:
                    iterator.rollback()
                    break
                else:
                    raise ParsingError(f"'{current.symbol}' is not allowed in this context.", str_index - 1)

            elif current.sym_type == PartType.NORMAL:

                cur = Symbol(
                    symbol=current.symbol,
                    operator=cls._parse_operator(iterator)
                )
                out.contents.append(cur)

            elif current.sym_type == PartType.SPECIAL:

                cur = SpecialSymbol(
                    symbol=current.symbol,
                    operator=cls._parse_operator(iterator)
                )
                out.contents.append(cur)

        return out

    @classmethod
    def _parse_group(cls, iterator: Lexer) -> Alternative:
        out = Alternative(contents=[], operator=None)
        str_index, current = next(iterator)
        assert current.symbol == '(' and current.sym_type == PartType.TOKEN
        while True:
            str_index, current = next(iterator)

            if current.symbol == ')' and current.sym_type == PartType.TOKEN:
                break

            if current.symbol != '|' or current.sym_type != PartType.TOKEN:
                iterator.rollback()

            cur = cls._parse_concatenation(iterator)
            if len(cur.contents) == 1:
                out.contents.append(cur.contents[0])
            else:
                out.contents.append(cur)

        return out
