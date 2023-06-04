from typing import Self
from parser import parse


class eNFA:
    def __init__(self):
        self.states: set[int] = set()
        self.transitions: dict[(int, str), set[int]] = dict()
        self.start_state: int | None = None
        self.end_state: int | None = None

    def regex_to_enfa(self, regex_input: str):
        parsed_regex = parse(regex_input)
        start_state = self._create_state()
        self.states.add(start_state)
        self.start_state = start_state
        self.end_state = self._build_enfa(parsed_regex.root.repr(), self.start_state)

    def _build_enfa(self, node: dict, start_state: int) -> int:
        is_operator = False
        is_numb_occurrence = False
        prev_start_state: int | None = None

        if node["operator"] is not None:
            if isinstance(node["operator"], tuple) and node["operator"] != (0, 1):
                is_numb_occurrence = True
                is_operator = False
            else:
                prev_start_state = start_state
                start_state = self._create_state()
                is_operator = True

        if node["type"] == "symbol":
            return self._handle_node_type(node, start_state, prev_start_state, is_numb_occurrence, is_operator,
                                          self._build_symbol_enfa)

        elif node["type"] == "alternative":
            return self._handle_node_type(node, start_state, prev_start_state, is_numb_occurrence, is_operator,
                                          self._build_alternative_enfa)

        elif node["type"] == "concatenation":
            return self._handle_node_type(node, start_state, prev_start_state, is_numb_occurrence, is_operator,
                                          self._build_concatenation_enfa)

        elif node["type"] == "special_symbol":
            ...  # todo

        else:
            raise ValueError("Invalid node type: " + node["type"])

    def _handle_node_type(self, node: dict, start_state: int, prev_start_state: int, is_num_occurences: bool,
                          is_operator: bool, build_type_func) -> int:

        if is_num_occurences:
            i = 0
            end_state = self._create_state()
            prev_end = start_state

            while i < node["operator"][1]:
                if i >= node["operator"][0]:
                    self._add_epsilon_transition(prev_end, end_state)

                prev_end = build_type_func(node, prev_end)
                i += 1
            self._add_epsilon_transition(prev_end, end_state)
        else:
            end_state = build_type_func(node, start_state)
            if is_operator:
                end_state = self._handle_operators(prev_start_state, start_state, end_state, node["operator"])
        return end_state

    def _build_concatenation_enfa(self, node: dict, start_state: int) -> int:
        prev_state = start_state

        for sub_node in node["contents"]:
            new_state = self._create_state()
            sub_end_state = self._build_enfa(sub_node, new_state)
            self._add_epsilon_transition(prev_state, new_state)
            prev_state = sub_end_state

        new_state = self._create_state()
        self._add_epsilon_transition(prev_state, new_state)
        return new_state

    def _build_alternative_enfa(self, node: dict, start_state: int) -> int:
        end_state = self._create_state()

        for sub_node in node["contents"]:
            new_state = self._create_state()
            self._add_epsilon_transition(start_state, new_state)
            self._add_epsilon_transition(self._build_enfa(sub_node, new_state), end_state)
        return end_state

    def _build_symbol_enfa(self, node: dict, start_state: int) -> int:
        new_state = self._create_state()
        self._add_symbol_transition(start_state, new_state, node["value"])
        return new_state

    def _handle_operators(self, prev_start_state: int, start_state: int, end_state: int, symbol: str) -> int:
        self._add_epsilon_transition(prev_start_state, start_state)
        new_end_state = self._create_state()
        self._add_epsilon_transition(end_state, new_end_state)

        if symbol != (0, 1):
            self._add_epsilon_transition(end_state, start_state)

        if symbol == "*":
            self._add_epsilon_transition(prev_start_state, new_end_state)
        return new_end_state

    def _create_state(self) -> int:
        new_state = len(self.states)
        self.states.add(new_state)
        return new_state

    def _add_epsilon_transition(self, source_state: int, target_state: int) -> None:
        if (source_state, "") not in self.transitions:
            self.transitions[(source_state, "")] = set()

        self.transitions[(source_state, "")].add(target_state)

    def _add_symbol_transition(self, source_state: int, target_state: int, symbol: str) -> None:
        if (source_state, symbol) not in self.transitions:
            self.transitions[(source_state, symbol)] = set()

        self.transitions[(source_state, symbol)].add(target_state)


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
