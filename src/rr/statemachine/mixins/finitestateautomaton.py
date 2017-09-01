from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import collections
import copy


class FiniteStateAutomatonMixin(object):

    class TransitionGraph(object):
        def __init__(self):
            self._transitions = collections.defaultdict(dict)

        def add(self, source, symbol, target):
            self._transitions[source][symbol] = target

        def get(self, source, symbol):
            return self._transitions[source][symbol]

        def copy(self):
            return copy.deepcopy(self)

    transition_graph = TransitionGraph()

    def transition_target(self, state, symbol):
        return self.transition_graph.get(state, symbol)
