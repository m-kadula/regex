
from typing import Self

class eNFA:

    def __init__(self,
                 states: frozenset[int],
                 alphabet: frozenset[str],
                 d: dict[(int, str), frozenset[int]],
                 start_state: int,
                 end_states: frozenset[int],
                 ):
        self.states = states.copy()
        self.alphabet = alphabet.copy()
        self.d = d.copy()
        self.start_state = start_state
        self.end_states = end_states.copy()


class NFA:

    def __init__(self,
                 states: frozenset[int],
                 alphabet: frozenset[str],
                 d: dict[(int, str), frozenset[int]],
                 start_state: int,
                 end_states: frozenset[int],
                 ):
        self.states = states.copy()
        self.alphabet = alphabet.copy()
        self.d = d.copy()
        self.start_state = start_state
        self.end_states = end_states.copy()

    @classmethod
    def eNFA_to_NFA(cls, enfa: eNFA) -> Self:
        ...


class CompiledRegex:

    def __init__(self,
                 states: frozenset[int],
                 alphabet: frozenset[str],
                 d: dict[(int, str), int],
                 start_state: int,
                 end_states: frozenset[int],
                 sinkhole_state: int | None = None
                 ):
        self.states = states.copy()
        self.alphabet = alphabet.copy()
        self.d = d.copy()
        self.start_state = start_state
        self.end_states = end_states.copy()
        self.sinkhole_state = sinkhole_state

    @classmethod
    def NFA_to_DFA(cls, nfa: NFA) -> Self:
        ...

    def minimalize(self) -> Self:
        ...
