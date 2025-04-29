#postifx regex to an NFA using Thompson's algorithm.
from typing import Dict, Set, List, Tuple

EPSILON = 'ε'

class State:
    def __init__(self):
        self.transitions: Dict[str, Set[int]] = {}
        self.is_accepting = False
    
    def add_transition(self, symbol: str, state: int):
        if symbol not in self.transitions:
            self.transitions[symbol] = set()
        self.transitions[symbol].add(state)

class NFA:
    def __init__(self):
        self.states: List[State] = []
        self.start_state = 0
        self.accepting_states: Set[int] = set()
    
    def add_state(self) -> int:
        self.states.append(State())
        return len(self.states) - 1
    
    def mark_accepting(self, state: int):
        self.states[state].is_accepting = True
        self.accepting_states.add(state)
    
    def add_transition(self, from_state: int, symbol: str, to_state: int):
        self.states[from_state].add_transition(symbol, to_state)

def thompson_construction(postfix: str) -> NFA:
    # build the NFA from the postfix expression using Thompson's algorithm
    stack = []
    
    for c in postfix:
        if c.isalnum():
            nfa = NFA()
            start = nfa.add_state()
            end = nfa.add_state()
            nfa.add_transition(start, c, end)
            nfa.mark_accepting(end)
            stack.append((nfa, start, end))
        
        elif c == '.':  # concatenation
            # reverse order of the stack
            nfa2, start2, end2 = stack.pop()
            nfa1, start1, end1 = stack.pop()
            
            nfa = NFA()
            
            # add all states from nfa1
            numbers_of_states_nfa1 = len(nfa.states)
            for _ in range(len(nfa1.states)):
                nfa.add_state()
            for i, state in enumerate(nfa1.states):
                for symbol, destinations in state.transitions.items():
                    for dest in destinations:
                        nfa.add_transition(numbers_of_states_nfa1 + i, symbol, numbers_of_states_nfa1 + dest)
            
            # add all states from nfa2
            numbers_of_states_nfa2 = len(nfa.states)
            for _ in range(len(nfa2.states)):
                nfa.add_state()
            for i, state in enumerate(nfa2.states):
                for symbol, destinations in state.transitions.items():
                    for dest in destinations:
                        nfa.add_transition(numbers_of_states_nfa2 + i, symbol, numbers_of_states_nfa2 + dest)
            
            # add epsilon transition from end1 to start2
            nfa.add_transition(numbers_of_states_nfa1 + end1, EPSILON, numbers_of_states_nfa2 + start2)
            
            # mark the end state of nfa2 as accepting
            nfa.mark_accepting(numbers_of_states_nfa2 + end2)
            
            # push the new NFA onto the stack
            stack.append((nfa, numbers_of_states_nfa1 + start1, numbers_of_states_nfa2 + end2))
        
        elif c == '|':  # alternation
            # reverse order of the stack

            nfa2, start2, end2 = stack.pop()
            nfa1, start1, end1 = stack.pop()
            
            nfa = NFA()
            
            # add a new start state and end state
            new_start = nfa.add_state()
            new_end = nfa.add_state()
            
            # add all states and transitions from nfa1
            numbers_of_states_nfa1 = len(nfa.states)
            for _ in range(len(nfa1.states)):
                nfa.add_state()
            for i, state in enumerate(nfa1.states):
                for symbol, destinations in state.transitions.items():
                    for dest in destinations:
                        nfa.add_transition(numbers_of_states_nfa1 + i, symbol, numbers_of_states_nfa1 + dest)
            
            # add all states and transitions from nfa2
            numbers_of_states_nfa2 = len(nfa.states)
            for _ in range(len(nfa2.states)):
                nfa.add_state()
            for i, state in enumerate(nfa2.states):
                for symbol, destinations in state.transitions.items():
                    for dest in destinations:
                        nfa.add_transition(numbers_of_states_nfa2 + i, symbol, numbers_of_states_nfa2 + dest)
            
            # add epsilon transitions from new start to both nfa1 and nfa2 start
            nfa.add_transition(new_start, EPSILON, numbers_of_states_nfa1 + start1)
            nfa.add_transition(new_start, EPSILON, numbers_of_states_nfa2 + start2)
            
            # add epsilon transitions from both nfa1 and nfa2 end to new end
            nfa.add_transition(numbers_of_states_nfa1 + end1, EPSILON, new_end)
            nfa.add_transition(numbers_of_states_nfa2 + end2, EPSILON, new_end)
            
            # mark the new end state as accepting
            nfa.mark_accepting(new_end)
            
            # push the new NFA onto the stack
            stack.append((nfa, new_start, new_end))
        
        elif c == '*':  # kleene star ( > 0 )
            nfa1, start1, end1 = stack.pop()
            
            nfa = NFA()
            
            new_start = nfa.add_state()
            new_end = nfa.add_state()
            
            # add all states and transitions from nfa1
            offset = len(nfa.states)
            for _ in range(len(nfa1.states)):
                nfa.add_state()
            for i, state in enumerate(nfa1.states):
                for symbol, destinations in state.transitions.items():
                    for dest in destinations:
                        nfa.add_transition(offset + i, symbol, offset + dest)
            
            # add epsilon transition from new start to new end (zero occurrence)
            nfa.add_transition(new_start, EPSILON, new_end)
            
            # add epsilon transition from new start to nfa1 start
            nfa.add_transition(new_start, EPSILON, offset + start1)
            
            # add epsilon transition from nfa1 end to new end
            nfa.add_transition(offset + end1, EPSILON, new_end)
            
            # add epsilon transition from nfa1 end to nfa1 start (closure)
            nfa.add_transition(offset + end1, EPSILON, offset + start1)
            
            # mark the new end state as accepting
            nfa.mark_accepting(new_end)
            
            # push the new NFA onto the stack
            stack.append((nfa, new_start, new_end))
        
        elif c == '+':  # plus operator (one or more)
            nfa1, start1, end1 = stack.pop()
            
            nfa = NFA()
            
            new_start = nfa.add_state()
            new_end = nfa.add_state()
            
            offset = len(nfa.states)
            for _ in range(len(nfa1.states)):
                nfa.add_state()
            for i, state in enumerate(nfa1.states):
                for symbol, destinations in state.transitions.items():
                    for dest in destinations:
                        nfa.add_transition(offset + i, symbol, offset + dest)
            
            # add epsilon transition from new start to nfa1 start
            nfa.add_transition(new_start, EPSILON, offset + start1)
            
            # add epsilon transition from nfa1 end to new end
            nfa.add_transition(offset + end1, EPSILON, new_end)
            
            # add epsilon transition from nfa1 end to nfa1 start (closure)
            nfa.add_transition(offset + end1, EPSILON, offset + start1)
            
            # mark the new end state as accepting
            nfa.mark_accepting(new_end)
            
            # push the new NFA onto the stack
            stack.append((nfa, new_start, new_end))
        
        elif c == '?':  # Optional operator (zero or one)
            nfa1, start1, end1 = stack.pop()
            
            nfa = NFA()
            
            # add a new start state and end state
            new_start = nfa.add_state()
            new_end = nfa.add_state()
            
            # add all states and transitions from nfa1
            offset = len(nfa.states)
            for _ in range(len(nfa1.states)):
                nfa.add_state()
            for i, state in enumerate(nfa1.states):
                for symbol, destinations in state.transitions.items():
                    for dest in destinations:
                        nfa.add_transition(offset + i, symbol, offset + dest)
            
            # add epsilon transition from new start to nfa1 start
            nfa.add_transition(new_start, EPSILON, offset + start1)
            
            # add epsilon transition from nfa1 end to new end
            nfa.add_transition(offset + end1, EPSILON, new_end)
            
            # add epsilon transition from new start to new end (zero occurrence)
            nfa.add_transition(new_start, EPSILON, new_end)
            
            # mark the new end state as accepting
            nfa.mark_accepting(new_end)
            
            # push the new NFA onto the stack
            stack.append((nfa, new_start, new_end))
    
    if len(stack) != 1:
        raise ValueError("Invalid postfix expression: too many operands")
    
    return stack[0][0]

def print_nfa(nfa: NFA):
    print("NFA States:", len(nfa.states))
    print("Start State:", nfa.start_state)
    print("Accepting States:", nfa.accepting_states)
    
    print("Transitions:")
    for i, state in enumerate(nfa.states):
        for symbol, destinations in state.transitions.items():
            for dest in destinations:
                print(f"  {i} --({symbol})--> {dest}")

if __name__ == "__main__":
    from regex_to_postfix import regex_to_postfix
    
    test_expressions = [
        "a*",
        "(ab)*",
        "a(b|c)*"
    ]
    
    for expr in test_expressions:
        print(f"\nRegular Expression: {expr}")
        postfix = regex_to_postfix(expr)
        print(f"Postfix: {postfix}")
        nfa = thompson_construction(postfix)
        print_nfa(nfa)