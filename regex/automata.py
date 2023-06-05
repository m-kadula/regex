from typing import Self
from regex.parser import parse


class eNFA:
    def __init__(self, states: set[int] = None,
                 transitions: dict[(int, str), set[int]] = None,
                 start_state: int | None = None,
                 end_state: int | None = None):
        self.states = states.copy() if states is not None else set()
        self.transitions = transitions.copy() if transitions is not None else dict()
        self.start_state = start_state
        self.end_state = end_state

    def __repr__(self):
        return f"{self.__class__.__name__}\nstates = {self.states}\ntransitions={self.transitions}\n" \
               f"start_state={self.start_state}\nend_state={self.end_state}"

    @classmethod
    def regex_to_enfa(cls, regex_input: str) -> 'eNFA':
        parsed_regex = parse(regex_input)
        enfa_instance = cls()
        enfa_instance.start_state = enfa_instance._create_state()
        enfa_instance.end_state = enfa_instance._build_enfa(parsed_regex.root.repr(),
                                                            enfa_instance.start_state)
        return enfa_instance

    def _build_enfa(self, node: dict, start_state: int) -> int:
        is_operator = False                         # flag for handling '*', '?', '+'
        is_range = False                            # flag for handling range - {x,y}
        prev_start_state: int | None = None         # if '*', '?', '+' allows jump over sub-automaton

        if node["operator"] is not None:
            if isinstance(node["operator"], tuple) and node["operator"] != (0, 1):
                is_range = True
                is_operator = False
            else:
                prev_start_state = start_state
                start_state = self._create_state()
                is_operator = True

        if node["type"] == "symbol":
            return self._handle_node_type(node, start_state, prev_start_state, is_range,
                                          is_operator, self._build_symbol_enfa)

        elif node["type"] == "alternative":
            return self._handle_node_type(node, start_state, prev_start_state, is_range,
                                          is_operator, self._build_alternative_enfa)

        elif node["type"] == "concatenation":
            return self._handle_node_type(node, start_state, prev_start_state, is_range,
                                          is_operator, self._build_concatenation_enfa)

        elif node["type"] == "special_symbol":
            return self._handle_node_type(node["value"], start_state, prev_start_state, is_range, is_operator,
                                          self._build_special_symbol_enfa)

        else:
            raise ValueError("Invalid node type: " + node["type"])

    def _build_concatenation_enfa(self, node: dict, start_state: int) -> int:
        sub_start_state = start_state

        for sub_node in node["contents"]:
            sub_start_state = self._build_enfa(sub_node, sub_start_state)
        return sub_start_state

    def _build_alternative_enfa(self, node: dict, start_state: int) -> int:
        end_state = self._create_state()

        for sub_node in node["contents"]:
            sub_start_state = self._create_state()
            self._add_epsilon_transition(start_state, sub_start_state)
            self._add_epsilon_transition(self._build_enfa(sub_node, sub_start_state), end_state)
        return end_state

    def _build_symbol_enfa(self, node: dict, start_state: int) -> int:
        next_state = self._create_state()
        self._add_symbol_transition(start_state, next_state, node["value"])
        return next_state

    def _build_special_symbol_enfa(self, symbol: str, start_state: int) -> int:
        next_state = self._create_state()

        if symbol == ".":
            self._add_ascii_range_transitions(start_state, next_state, 0, 127)
            self.transitions.pop((start_state, '\n'))

        elif symbol == "d":
            self._add_ascii_range_transitions(start_state, next_state, 48, 57)

        elif symbol == "D":
            self._add_ascii_range_transitions(start_state, next_state, 0, 128)
            self._remove_ascii_range_transitions(start_state, 48, 57)

        elif symbol == "w":
            self._add_ascii_range_transitions(start_state, next_state, 65, 90)
            self._add_ascii_range_transitions(start_state, next_state, 97, 122)
            self._add_ascii_range_transitions(start_state, next_state, 48, 57)
            self._add_symbol_transition(start_state, next_state, '_')

        elif symbol == "W":
            self._add_ascii_range_transitions(start_state, next_state, 0, 47)
            self._add_ascii_range_transitions(start_state, next_state, 58, 64)
            self._add_ascii_range_transitions(start_state, next_state, 91, 96)
            self._add_ascii_range_transitions(start_state, next_state, 123, 128)
            self.transitions.pop(start_state, '_')

        elif symbol == "s":
            white_space_chars = [chr(32), chr(9), chr(11), chr(10), chr(13), chr(12)]
            for ch in white_space_chars:
                self._add_symbol_transition(start_state, next_state, ch)

        elif symbol == "S":
            white_space_chars = [chr(32), chr(9), chr(11), chr(10), chr(13), chr(12)]
            for ch in map(chr, range(128)):
                if ch not in white_space_chars:
                    self._add_symbol_transition(start_state, next_state, ch)

        else:
            raise ValueError("Invalid value of special symbol: " + symbol)

        return next_state

    def _handle_node_type(self, node: dict, start_state: int, prev_start_state: int, is_range: bool,
                          is_operator: bool, build_type_func) -> int:
        if is_range:
            i = 0
            end_state = self._create_state()
            prev_end_state = start_state

            while i < node["operator"][1]:
                if i >= node["operator"][0]:
                    self._add_epsilon_transition(prev_end_state, end_state)

                prev_end_state = build_type_func(node, prev_end_state)
                i += 1
            self._add_epsilon_transition(prev_end_state, end_state)
            return end_state
        else:
            end_state = build_type_func(node, start_state)
            if is_operator:
                end_state = self._handle_operators(prev_start_state, start_state, end_state, node)
            return end_state

    def _handle_operators(self, prev_start_state: int, start_state: int, end_state: int, node: dict) -> int:
        self._add_epsilon_transition(prev_start_state, start_state)
        new_end_state = self._create_state()
        self._add_epsilon_transition(end_state, new_end_state)

        if node["operator"] != (0, 1):                                  # creates a loop in the automaton
            self._add_epsilon_transition(end_state, start_state)

        if node["operator"] == "*" or node["operator"] == (0, 1):       # allows to skip the sub-automaton
            self._add_epsilon_transition(prev_start_state, new_end_state)
        return new_end_state

    def _create_state(self) -> int:
        new_state = len(self.states)
        self.states.add(new_state)
        return new_state

    def _add_ascii_range_transitions(self, start_state: int, end_state: int, start: int, end: int) -> None:
        for ch in map(chr, range(start, end + 1)):
            self._add_symbol_transition(start_state, end_state, ch)

    def _remove_ascii_range_transitions(self, start_state: int, start: int, end: int) -> None:
        for ch in map(chr, range(start, end + 1)):
            if (start_state, ch) in self.transitions:
                self.transitions.pop((start_state, ch))

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
