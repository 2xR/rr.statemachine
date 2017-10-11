import collections

from .statemachine import StateMachine
from .transitiongraph import TransitionGraph, TransitionGraphDrivenMixin


class FiniteStateAutomatonTransitionGraph(TransitionGraph):

    def __init__(self, transitions=()):
        self.arcs = collections.defaultdict(dict)
        self.update(transitions)

    def add(self, transition):
        source, symbol, target = transition
        self.arcs[source][symbol] = target

    def target(self, source, symbol):
        return self.arcs[source][symbol]


class FiniteStateAutomaton(TransitionGraphDrivenMixin, StateMachine):

    # Provide access to the transition graph class that should be used when constructing the
    # class or instance's transition graph.
    TransitionGraph = FiniteStateAutomatonTransitionGraph

    def __init__(self, initial_state=None, transition_graph=None):
        TransitionGraphDrivenMixin.__init__(self, transition_graph)
        StateMachine.__init__(self, initial_state)
