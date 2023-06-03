
from typing import Self
from parser import parse

class eNFA:

    def __init__(self):
        self.states: set[int] = set()
        self.transitions: dict[(int, str), set[int]] = dict()
        self.start_state: int | None = None
        self.end_state: int | None = None

    def _regex_to_enfa(self, regex: str):
        parsed_regex = parse(regex)
        start_state = self._create_state()
        self.states.add(start_state)
        self.start_state = start_state
        self.end_state = self._build_enfa(parsed_regex.root, self.start_state)

    def _build_enfa(self, node: dict, start_state: int) -> int:


        if node["operator"] is not None:
            pass # TODO

        if node["type"] == "symbol":
           pass # TODO

        elif node["type"] == "alternative":
            pass # TODO

        elif node["type"] == "concatenation":
            pass # TODO

        elif node["type"] == "special_symbol":
            pass # TODO

        else:
            raise ValueError("Invalid node type: " + node["type"])


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
