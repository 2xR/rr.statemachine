from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import collections
import random

from .finitestateautomaton import FiniteStateAutomaton


class MarkovChainTransitionGraph(object):

    def __init__(self, transitions=()):
        self.arcs = collections.defaultdict(list)
        self.total_weight = collections.defaultdict(float)
        for transition in transitions:
            self.add(transition)

    def add(self, transition):
        source, weight, target = transition
        self.arcs[source].append((weight, target))
        self.total_weight[source] += weight

    def target(self, source, rng=random):
        x = rng.uniform(0, self.total_weight[source])
        y = 0
        for weight, target in self.arcs[source]:
            y += weight
            if x <= y:
                return target
        raise RuntimeError("oh boy, how embarrassing...")


class MarkovChain(FiniteStateAutomaton):
    """In a Markov chain, the target state of a transition depends not on an input symbol,
    but on a weight assigned to each outgoing arc. The target state is randomly selected with
    each target state having a probability proportional to its weight.
    """

    TransitionGraph = MarkovChainTransitionGraph  # override the TransitionGraph implementation
    Transition = collections.namedtuple("MarkovChainTransition", ["source", "weight", "target"])

    def __init__(self, initial_state=None, transitions=None, rng=random):
        FiniteStateAutomaton.__init__(self, initial_state, transitions)
        self._rng = rng

    def step(self, n=1):
        """Advance the Markov chain `n` steps.

        Call this method on Markov chains instead of `input()`.

        Implementation detail (should be irrelevant for users): the chain's RNG is used as input
        symbol regardless of current state. This way it gets passed on to the transition graph's
        `target()` method, allowing it to use the RNG.
        """
        for _ in range(n):
            self.input(self._rng)
