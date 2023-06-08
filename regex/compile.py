
from typing import Self
from pickle import dumps, loads
from regex.automata import ENFA, NFA, DFA


class Match:

    def __init__(self, text: str, span: tuple[int, int], __reg: 'CompiledRegex' = None):
        self.text = text
        self.span = span
        self.reg = __reg

    def __repr__(self):
        return f"<Match: {repr(self.get_match)}, span: {self.span}>"

    @property
    def regex(self):
        return self.reg

    @property
    def get_match(self) -> str:
        return self.text[self.span[0]:self.span[1]]


class CompiledRegex:

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

    def match_all(self, text: str) -> list[Match]:
        automatons: list[(int, int, int)] = []
        next_automatons: list[(int, int, int)] = []
        for i, letter in enumerate(text):
            next_automatons.clear()

            if self.dfa.start_state not in self.dfa.end_states:
                automatons.append((i, -1, self.dfa.start_state))
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
                    if last != -1:
                        next_automatons.append((index, last, -1))

            automatons = next_automatons.copy()

        return [Match(text, (start, stop + 1), self) for start, stop, _ in automatons if stop != -1]

    def pack(self) -> bytes:
        return dumps(self)

    @classmethod
    def unpack(cls, contents: bytes) -> Self:
        return loads(contents)
