import collections
import random

from .statemachine import StateMachine
from .transitiongraph import TransitionGraph, TransitionGraphDrivenMixin


class MarkovChainTransitionGraph(TransitionGraph):

    def __init__(self, transitions=()):
        self.arcs = collections.defaultdict(list)
        self.total_weight = collections.defaultdict(float)
        self.update(transitions)

    def add(self, transition):
        source, weight, target = transition
        self.arcs[source].append((weight, target))
        self.total_weight[source] += weight

    def target(self, source, rng):
        x = rng.random() * self.total_weight[source]
        y = 0
        for weight, target in self.arcs[source]:
            y += weight
            if x <= y:
                return target
        raise RuntimeError("oh boy, how embarrassing...")


class MarkovChain(TransitionGraphDrivenMixin, StateMachine):
    """In a Markov chain, the target state of a transition depends not on an input symbol,
    but on a weight assigned to each outgoing arc. The target state is randomly selected with
    each target state having a probability proportional to its weight.
    """

    # Provide access to the transition graph class that should be used when constructing the
    # class or instance's transition graph.
    TransitionGraph = MarkovChainTransitionGraph

    # Default pseudo-random number generator used when triggering transitions. Can be overridden
    # at instance level. By default it uses the random module.
    rng = random

    def __init__(self, initial_state=None, transition_graph=None, rng=None):
        TransitionGraphDrivenMixin.__init__(self, transition_graph)
        StateMachine.__init__(self, initial_state)
        if rng is not None:
            self.rng = rng

    def step(self, n=1):
        """Advance the Markov chain `n` steps.

        Call this method on Markov chains instead of using `input()`.

        Implementation detail (should be irrelevant for users): the chain's RNG is used as input
        symbol regardless of current state. This way it gets passed on to the transition graph's
        `target()` method, allowing it to use the RNG's services (another possibility would be to
        pass a uniform random number between 0 and 1 as input).
        """
        for _ in range(n):
            self.input(self.rng)
