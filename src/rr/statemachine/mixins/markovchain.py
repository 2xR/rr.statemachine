from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import collections
import copy
import random


class MarkovChainMixin(object):
    """This mixin allows the state machine to behave like a Markov chain, in the sense that
    transitions can be taken independently of symbol. The target state depends not on an input
    symbol, but on a probability assigned to each outgoing arc.
    """

    def step(self):
        return self.input(None)

    def transition_function(self, state, symbol):
        if symbol is not None:
            raise ValueError("expecting no symbol")
        return self.transition_graph.get(state)


class MarkovChainTransitionGraph(object):

    def __init__(self, rng=random):
        self.transitions = collections.defaultdict(list)
        self.rng = rng

    def add(self, source, target, weight=1):
        self.transitions[source].append((target, weight))

    def get(self, source):
        source_transitions = self.transitions[source]
        total_weight = sum(w for _, w in source_transitions)
        x = self.rng.uniform(0, total_weight)
        y = 0
        for target, weight in source_transitions:
            y += weight
            if x <= y:
                return target
        raise RuntimeError("oh boy, how embarrassing...")

    def copy(self):
        return copy.deepcopy(self)
