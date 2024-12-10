class State:
    def __init__(self, name, output):
        self.name = name
        self.output = output
        self.transitions = {}

    def add_transition(self, input_symbol, next_state):
        self.transitions[input_symbol] = next_state

    def next_state(self, input_symbol):
        return self.transitions.get(input_symbol, None)

class MooreMachine:
    def __init__(self, states, initial_state):
        self.states = states
        self.current_state = initial_state

    def process(self, inputs):
        outputs = []
        for symbol in inputs:
            outputs.append(self.current_state.output)
            self.current_state = self.current_state.next_state(symbol)
        outputs.append(self.current_state.output)
        return outputs


s1 = State("S1", "0")
s2 = State("S2", "1")

s1.add_transition("a", s2)
s2.add_transition("b", s1)

moore_machine = MooreMachine([s1, s2], s1)
print(moore_machine.process(["a", "b", "a", "b"]))
