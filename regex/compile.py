
from typing import Self
from pickle import dumps, loads
from regex.automata import ENFA, NFA, DFA


class CompiledRegex:

    def __init__(self, regular_expression: str, __execute=True):
        self.regex = regular_expression
        if __execute:
            enfa = ENFA.get_enfa(regular_expression)
            nfa = NFA.get_nfa(enfa)
            dfa = DFA.get_dfa(nfa)
            dfa = dfa.minimalize()
            dfa.detect_sinkhole()
            self.dfa = dfa
        else:
            self.dfa = None

    def __repr__(self):
        return f"<compile.CompiledRegex({repr(self.regex)})>"

    def match_all(self, text: str) -> bool:
        current_state = self.dfa.start_state
        for letter in text:
            if letter not in self.dfa.alphabet:
                return False
            current_state = self.dfa.transitions[(current_state, letter)]
            if current_state == self.dfa.sink_state:
                return False
        return current_state in self.dfa.end_states

    def pack(self) -> bytes:
        return dumps(self)

    @classmethod
    def unpack(cls, contents: bytes) -> Self:
        return loads(contents)
