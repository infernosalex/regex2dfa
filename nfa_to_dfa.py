from typing import Dict, Set, List, Tuple, FrozenSet
from nfa_builder import NFA, EPSILON
from graphviz import Digraph

class DFAState:
    def __init__(self, nfa_states: Set[int]):
        self.nfa_states = nfa_states
        self.transitions: Dict[str, int] = {}
        self.is_accepting = False

class DFA:
    def __init__(self):
        self.states: List[DFAState] = []
        self.start_state = 0
        self.accepting_states: Set[int] = set()
        self.alphabet: Set[str] = set()
    
    def add_state(self, nfa_states: Set[int]) -> int:
        self.states.append(DFAState(nfa_states))
        return len(self.states) - 1
    
    def mark_accepting(self, state: int):
        self.states[state].is_accepting = True
        self.accepting_states.add(state)
    
    def add_transition(self, from_state: int, symbol: str, to_state: int):
        self.states[from_state].transitions[symbol] = to_state
        self.alphabet.add(symbol)

def epsilon_closure(nfa: NFA, states: Set[int]) -> Set[int]:
    #epsilon closure of a set of states in the NFA

    # start with the given states
    closure = set(states)
    stack = list(states)
    
    # While states to process
    while stack:
        state = stack.pop()
        
        # follow epsilon transitions
        if EPSILON in nfa.states[state].transitions:
            for next_state in nfa.states[state].transitions[EPSILON]:
                if next_state not in closure:
                    closure.add(next_state)
                    stack.append(next_state)
    
    return closure

def move(nfa: NFA, states: Set[int], symbol: str) -> Set[int]:
    # compute the set of states reachable from the given states on the given symbol
    
    result = set()
    
    for state in states:
        if symbol in nfa.states[state].transitions:
            result.update(nfa.states[state].transitions[symbol])
    
    return result

def subset_construction(nfa: NFA) -> DFA:
    dfa = DFA()
    
    # find all symbols in the NFA (excluding epsilon)
    alphabet = set()
    for state in nfa.states:
        for symbol in state.transitions:
            if symbol != EPSILON:
                alphabet.add(symbol)
    
    # compute epsilon closure of start state
    start_closure = epsilon_closure(nfa, {nfa.start_state})
    
    # create start state in DFA
    dfa.add_state(start_closure)
    
    # check if start state is accepting
    for state in start_closure:
        if state in nfa.accepting_states:
            dfa.mark_accepting(0)
            break
    
    # queue of DFA states to process
    unmarked_states = [0]
    
    # map NFA state sets to DFA states
    state_map = {frozenset(start_closure): 0}
    
    while unmarked_states:
        current_state = unmarked_states.pop(0)
        current_nfa_states = dfa.states[current_state].nfa_states
        
        for symbol in alphabet:
            # find all states reachable on symbol from current states
            next_states = move(nfa, current_nfa_states, symbol)
            
            # apply epsilon closure
            next_closure = epsilon_closure(nfa, next_states)
            
            if not next_closure:  # if no states reachable, continue
                continue
            
            # convert to frozenset for dictionary key 
            next_frozenset = frozenset(next_closure)
            
            # if this is a new set of NFA states, add a new DFA state
            if next_frozenset not in state_map:
                new_state = dfa.add_state(next_closure)
                state_map[next_frozenset] = new_state
                unmarked_states.append(new_state)
                
                # check if this new state is accepting
                for nfa_state in next_closure:
                    if nfa_state in nfa.accepting_states:
                        dfa.mark_accepting(new_state)
                        break
            
            # add transition in DFA
            dfa.add_transition(current_state, symbol, state_map[next_frozenset])
    
    return dfa

def print_dfa(dfa: DFA):
    print("DFA States:", len(dfa.states))
    print("Start State:", dfa.start_state)
    print("Accepting States:", dfa.accepting_states)
    print("Alphabet:", dfa.alphabet)
    
    print("Transitions:")
    for i, state in enumerate(dfa.states):
        for symbol, dest in state.transitions.items():
            print(f"  {i} --({symbol})--> {dest}")
        if not state.transitions:
            print(f"  {i} -- No outgoing transitions --")

def simulate_dfa(dfa: DFA, input_string: str) -> bool:
    # simulate a DFA on an input string
    
    current_state = dfa.start_state
    
    for char in input_string:
        if char not in dfa.alphabet:
            return False  # invalid input symbol
        
        if char in dfa.states[current_state].transitions:
            current_state = dfa.states[current_state].transitions[char]
        else:
            return False  # no valid transition
    
    # check if final state is accepting
    return current_state in dfa.accepting_states

if __name__ == "__main__":
    from regex_to_postfix import regex_to_postfix
    from nfa_builder import thompson_construction
    
    test_expressions = [
        "a*",
        "(ab)*",
        "a(b|c)*"
    ]
    
    for expr in test_expressions:
        print(f"\nRegular Expression: {expr}")
        postfix = regex_to_postfix(expr)
        print(f"Postfix: {postfix}")
        
        print("\nNFA:")
        nfa = thompson_construction(postfix)
        
        print("\nDFA:")
        dfa = subset_construction(nfa)
        print_dfa(dfa)
        
        test_strings = ["", "a", "ab", "abc", "aba"]
        for test in test_strings:
            result = simulate_dfa(dfa, test)
            print(f"String '{test}' acceptance: {result}")