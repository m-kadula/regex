"""Automata for representing regular expressions"""

from typing import Self
from pickle import dumps, loads
from regex.parser import parse



class ENFA:
    def __init__(self, states: set[int] = None,
                 transitions: dict[(int, str), set[int]] = None,
                 start_state: int | None = None,
                 end_state: int | None = None):
        self.states = states.copy() if states is not None else set()
        self.transitions = transitions.copy() if transitions is not None else dict()
        self.start_state = start_state
        self.end_state = end_state

    def __repr__(self):
        return f"{self.__class__.__name__}(\n    states={self.states},\n    transitions={self.transitions}," \
               f"\n    start_state={self.start_state},\n    end_state={self.end_state}\n)"

    @classmethod
    def get_enfa(cls, regex_input: str) -> Self:
        parsed_regex = parse(regex_input)
        enfa_instance = cls()
        enfa_instance.start_state = enfa_instance._create_state()
        enfa_instance.end_state = enfa_instance._build_enfa(parsed_regex.root.repr(),
                                                            enfa_instance.start_state)
        return enfa_instance

    def _build_enfa(self, node: dict, start_state: int) -> int:
        is_operator = False  # flag for handling '*', '?', '+'
        is_range = False  # flag for handling range - {x,y}
        prev_start_state: int | None = None  # if '*', '?', '+' allows jump over sub-automaton

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

        if node["operator"] != (0, 1):  # creates a loop in the automaton
            self._add_epsilon_transition(end_state, start_state)

        if node["operator"] == "*" or node["operator"] == (0, 1):  # allows to skip the sub-automaton
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
    def __init__(self, states: set[int] = None,
                 transitions: dict[(int, str), set[int]] = None,
                 start_state: int | None = None,
                 end_states: set[int] = None):
        self.states = states.copy() if states is not None else set()
        self.transitions = transitions.copy() if transitions is not None else dict()
        self.start_state = start_state
        self.end_states = end_states.copy() if states is not None else set()

    def __repr__(self):
        return f"{self.__class__.__name__}(\n    states={self.states},\n    transitions={self.transitions}," \
               f"\n    start_state={self.start_state},\n    end_states={self.end_states}\n)"

    def get_alphabet(self) -> frozenset[str]:
        return frozenset(letter for _, letter in self.transitions.keys())

    def transition(self, states: frozenset[int], letter: str) -> frozenset[int]:
        out = set()
        for state in states:
            if (state, letter) not in self.transitions:
                continue
            out.update(self.transitions[(state, letter)])
        return frozenset(out)

    @classmethod
    def get_nfa(cls, enfa: ENFA) -> Self:
        nfa_instance = cls()
        nfa_instance.states = enfa.states.copy()
        nfa_instance.start_state = enfa.start_state

        e_closures = nfa_instance._compute_e_closures(nfa_instance.states, enfa.transitions)
        nfa_instance.end_states = nfa_instance._compute_end_states(nfa_instance.states, e_closures, enfa.end_state)
        nfa_instance.transitions = nfa_instance._compute_transitions(
            nfa_instance.states,
            e_closures,
            enfa.transitions
        )
        nfa_instance._remove_unreachable_states()
        return nfa_instance

    @staticmethod
    def _compute_e_closures(states: set[int], transitions: dict[(int, str), set[int]]) -> dict[int, set[int]]:
        e_closures: dict[int, set[int]] = {}

        for current_state in states:
            if current_state not in e_closures:
                closure = set()
                stack = [current_state]
                while stack:
                    state = stack.pop()
                    if state not in closure:
                        closure.add(state)
                        stack.extend(transitions.get((state, ''), set()))
                e_closures[current_state] = closure
        return e_closures

    @staticmethod
    def _compute_end_states(states: set[int], e_closures: dict[int, set[int]], end_state: int) -> set[int]:
        end_states = set()
        for state in states:
            if end_state in e_closures[state]:
                end_states.add(state)
        return end_states

    @staticmethod
    def _compute_transitions(states: set[int], e_closures: dict[int, set[int]],
                             transitions: dict[(int, str), set[int]]) -> dict[(int, str), set[int]]:
        nfa_transitions = {}
        for state in states:
            for symbol in set(k[1] for k in transitions.keys() if k[1] != ""):
                next_states = set()
                for current_state in e_closures[state]:
                    next_states.update(transitions.get((current_state, symbol), set()))
                if next_states:
                    nfa_transitions[(state, symbol)] = set().union(*[e_closures[s] for s in next_states])
        return nfa_transitions

    def _remove_unreachable_states(self):
        reachable_states = set()
        stack = [self.start_state]

        while stack:
            current_state = stack.pop()
            reachable_states.add(current_state)

            for symbol in set(k[1] for k in self.transitions.keys() if k[0] == current_state):
                for next_state in self.transitions.get((current_state, symbol), set()):
                    if next_state not in reachable_states:
                        stack.append(next_state)

        unreachable_states = self.states - reachable_states
        self.states -= unreachable_states
        self.end_states -= unreachable_states
        self.transitions = {
            k: v - unreachable_states for k, v in self.transitions.items()
            if k[0] not in unreachable_states
        }


class DFA:

    def __init__(self, states: frozenset[int] = None,
                 alphabet: frozenset[str] = None,
                 transitions: dict[(int, str), int] = None,
                 start_state: int = None,
                 end_states: frozenset[int] = None,
                 sink_state: int | None = None):
        self.states = states if states is not None else frozenset()
        self.alphabet = alphabet if alphabet is not None else frozenset()
        self.transitions = transitions.copy() if transitions is not None else dict()
        self.start_state = start_state
        self.end_states = end_states if states is not None else frozenset()
        self.sink_state = sink_state

    def __repr__(self):
        return f"{self.__class__.__name__}(\n    states={self.states},\n    alphabet={self.alphabet},\n    " \
               f"transitions={self.transitions},\n    start_state={self.start_state},\n    " \
               f"end_states={self.end_states}\n    sink_state={self.sink_state}\n)"

    def serialize(self) -> bytes:
        return dumps(self)

    @classmethod
    def unpack(cls, contents: bytes) -> Self:
        return loads(contents)

    def match_all(self, text: str) -> bool:
        current_state = self.start_state
        for letter in text:
            if letter not in self.alphabet:
                return False
            current_state = self.transitions[(current_state, letter)]
            if current_state == self.sink_state:
                return False
        return current_state in self.end_states

    def detect_sinkhole(self) -> bool:
        for state in self.states.difference(self.end_states):
            if all(self.transitions[(state, letter)] == state for letter in self.alphabet):
                self.sink_state = state
                return True
        return False

    @classmethod
    def get_dfa(cls, nfa: NFA) -> Self:
        alphabet = nfa.get_alphabet()
        transitions: dict[(frozenset[int], str), frozenset[int]] = dict()

        upcoming_states: set[frozenset[int]] = {frozenset([nfa.start_state])}
        determined_states: dict[frozenset[int], int] = dict()

        state_index = 0

        while len(upcoming_states) > 0:
            current_state = upcoming_states.pop()
            determined_states[current_state] = state_index
            state_index += 1

            for letter in alphabet:
                after_transition = nfa.transition(current_state, letter)
                transitions[(current_state, letter)] = after_transition
                if after_transition not in determined_states:
                    upcoming_states.add(after_transition)

        transitions_integers: dict[(int, str), int] = dict()
        end_states: set[int] = set()

        for state in determined_states:
            if nfa.end_states.intersection(state) != set():
                end_states.add(determined_states[state])
            for letter in alphabet:
                transitions_integers[(determined_states[state], letter)] = \
                    determined_states[transitions[(state, letter)]]

        assert determined_states[frozenset([nfa.start_state])] == 0
        return cls(
            states=frozenset(range(state_index)),
            alphabet=alphabet,
            transitions=transitions_integers,
            start_state=0,
            end_states=frozenset(end_states)
        )

    def _is_in_relation(self, abstract_classes: frozenset[frozenset[int]], a: int, b: int) -> bool:
        for letter in self.alphabet:
            subset = {self.transitions[(a, letter)], self.transitions[(b, letter)]}
            if not any(subset.issubset(i) for i in abstract_classes):
                return False
        return True

    def _relax_relations(self,
                         relation: frozenset[int],
                         abstract_classes: frozenset[frozenset[int]]) -> frozenset[frozenset[int]]:
        in_relation: dict[int, set[int]] = {i: {i} for i in relation}
        not_checked: dict[int, set[int]] = {i: set(relation.difference({i})) for i in relation}
        nonempty = set(relation)

        while len(nonempty) > 0:
            a = nonempty.pop()
            if len(not_checked[a]) == 0:
                continue
            nonempty.add(a)
            b = not_checked[a].pop()
            if a not in not_checked[b]:
                continue
            not_checked[a].add(b)

            if self._is_in_relation(abstract_classes, a, b):
                new_relation = in_relation[a].union(in_relation[b])
                new_unchecked = not_checked[a].intersection(not_checked[b])

                for item in new_relation:
                    in_relation[item] = new_relation.copy()
                    not_checked[item] = new_unchecked.copy()

            else:
                new_unchecked = not_checked[a].difference({b})
                for item in in_relation[a]:
                    not_checked[item] = new_unchecked.copy()
                new_unchecked = not_checked[b].difference({a})
                for item in in_relation[b]:
                    not_checked[item] = new_unchecked.copy()

        return frozenset(frozenset(s) for s in in_relation.values())

    def minimalize(self) -> Self:
        abstract_classes = frozenset({self.states.difference(self.end_states), self.end_states})
        while True:
            upcoming = set()
            for element in abstract_classes:
                upcoming.update(self._relax_relations(element, abstract_classes))
            if abstract_classes == frozenset(upcoming):
                break
            else:
                abstract_classes = frozenset(upcoming)

        enumerated: dict[int, int] = dict()
        for i, s in enumerate(abstract_classes):
            for element in s:
                enumerated[element] = i
        states: set[int] = set()
        transitions: dict[(int, str), int] = dict()
        end_states: set[int] = set()
        start_state = enumerated[self.start_state]

        for s in enumerated:
            states.add(enumerated[s])
            if s in self.end_states:
                end_states.add(enumerated[s])
            for letter in self.alphabet:
                transitions[(enumerated[s], letter)] = enumerated[self.transitions[(s, letter)]]

        return self.__class__(
            states=frozenset(states),
            alphabet=self.alphabet,
            transitions=transitions,
            start_state=start_state,
            end_states=frozenset(end_states)
        )
