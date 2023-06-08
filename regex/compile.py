"""Regex toolset"""

from typing import Self, Union, Any
from pickle import dumps, loads
from regex.automata import ENFA, NFA, DFA


class Match:
    """Stores one substring of a text that belongs to the language expressed in regex"""

    def __init__(self, text: str, span: tuple[int, int], __reg: 'CompiledRegex' = None):
        self.text = text
        self.span = span
        self._reg = __reg

    def __repr__(self):
        return f"<Match: {repr(self.get_str)}, span: {self.span}>"

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, type(self)):
            return False
        return self.text == other.text and self.span == other.span

    @property
    def begin(self) -> int:
        return self.span[0]

    @property
    def end(self) -> int:
        return self.span[1]

    @property
    def regex(self) -> Union['CompiledRegex', None]:
        return self._reg

    @property
    def get_str(self) -> str:
        return self.text[self.begin:self.end]


class CompiledRegex:
    """Compile a regular expression"""

    def __init__(self, regular_expression: str):
        self.regex = regular_expression
        enfa = ENFA.get_enfa(regular_expression)
        nfa = NFA.get_nfa(enfa)
        dfa = DFA.get_dfa(nfa)
        dfa = dfa.minimalize()
        dfa.detect_sinkhole()
        self.dfa = dfa

    def __repr__(self):
        return f"compile.CompiledRegex({repr(self.regex)})"

    def full_match(self, text: str) -> Match | None:
        """
        Returns Match object if the entire text matches the regular expression,
        returns None otherwise.
        """
        current_state = self.dfa.start_state
        for letter in text:
            if letter not in self.dfa.alphabet:
                return None
            current_state = self.dfa.transitions[(current_state, letter)]
            if current_state == self.dfa.sink_state:
                return None
        if current_state in self.dfa.end_states:
            return Match(text, (0, len(text)), self)
        else:
            return None

    def match(self, text: str) -> Match | None:
        """
        Returns Match object if the beginning of text matches the regular expression,
        returns None otherwise.
        """
        last_end_state = None if self.dfa.start_state not in self.dfa.end_states else -1
        current_state = self.dfa.start_state
        for i, letter in enumerate(text):
            next_state = self.dfa.transitions.get((current_state, letter), None)
            if next_state is None or next_state == self.dfa.sink_state:
                break
            if next_state in self.dfa.end_states:
                last_end_state = i
            current_state = next_state
        return Match(text, (0, last_end_state + 1), self) if last_end_state is not None else None

    def search(self, text: str) -> Match | None:
        """
        Returns the first substring in text that matches the regular expression,
        returns None if no such substring is found.
        """
        automatons: list[(int, int, int)] = []
        next_automatons: list[(int, int, int)] = []
        for i, letter in enumerate(text):
            next_automatons.clear()

            if self.dfa.start_state not in self.dfa.end_states:
                automatons.append((i, None, self.dfa.start_state))
            else:
                automatons.append((i, i - 1, self.dfa.start_state))

            for index, last, state in automatons:
                next_state = self.dfa.transitions.get((state, letter), None)
                if next_state in self.dfa.end_states:
                    next_automatons.append((index, i, next_state))
                    break
                elif next_state is not None and next_state != self.dfa.sink_state:
                    next_automatons.append((index, last, next_state))
                elif last is not None:
                    return Match(text, (index, last + 1), self)

            automatons = next_automatons.copy()

        if len(automatons) > 0:
            index, last, _ = automatons[0]
            if last is None:
                return None
            return Match(text, (index, last + 1), self)
        else:
            return None

    def find_all(self, text: str) -> list[Match]:
        """
        Returns a list of all substrings that match the regular expression.
        """
        automatons: list[(int, int, int)] = []
        next_automatons: list[(int, int, int)] = []
        for i, letter in enumerate(text):
            next_automatons.clear()

            if self.dfa.start_state not in self.dfa.end_states:
                automatons.append((i, None, self.dfa.start_state))
            else:
                automatons.append((i, i - 1, self.dfa.start_state))

            for index, last, state in automatons:
                next_state = self.dfa.transitions.get((state, letter), None)
                if next_state in self.dfa.end_states:
                    next_automatons.append((index, i, next_state))
                    break
                elif next_state is not None and next_state != self.dfa.sink_state:
                    next_automatons.append((index, last, next_state))
                else:
                    if last is not None:
                        next_automatons.append((index, last, -1))

            automatons = next_automatons.copy()

        return [Match(text, (start, stop + 1), self) for start, stop, _ in automatons if stop is not None]

    def pack(self) -> bytes:
        """Returns a serialised version of Self that can be stored in a file."""
        return dumps(self)

    @classmethod
    def unpack(cls, contents: bytes) -> Self:
        """Returns an instance of class serialised by self.pack()"""
        return loads(contents)
