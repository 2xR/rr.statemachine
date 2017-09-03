from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import collections

from .statemachine import StateMachine, Transition


class FiniteStateAutomatonTransitionGraph(object):

    def __init__(self, transitions=()):
        self.arcs = collections.defaultdict(dict)
        for transition in transitions:
            self.add(transition)

    def add(self, transition):
        source, symbol, target = transition
        self.arcs[source][symbol] = target

    def target(self, source, symbol):
        return self.arcs[source][symbol]


class FiniteStateAutomaton(StateMachine):

    # The transition graph class to be used when constructing the instance's transition graph.
    # This can be overriden by subclasses to use different transition graph implementations
    # (see, for example, MarkovChain).
    TransitionGraph = FiniteStateAutomatonTransitionGraph
    Transition = Transition  # (source, symbol, target) named tuples
    transitions = None  # iterable of `Transition`s (defined at class or instance level)

    def __init__(self, initial_state=None, transitions=None):
        StateMachine.__init__(self, initial_state)
        if transitions is None:
            transitions = self.transitions
        self._transition_graph = self.TransitionGraph(transitions)

    def transition_target(self, state, symbol):
        return self._transition_graph.target(state, symbol)
