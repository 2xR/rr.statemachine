import bisect
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
        history, weight, target = transition
        if not isinstance(history, tuple):
            raise TypeError("history must be a tuple of states")
        if weight <= 0:
            raise ValueError("transition weight must be positive")
        total_weight = self.total_weight[history] + weight
        self.arcs[history].append((total_weight, target))
        self.total_weight[history] = total_weight

    def target(self, history, rng):
        if not isinstance(history, tuple):
            raise TypeError("history must be a tuple of states")
        arcs = self.arcs[history]
        x = rng.random() * self.total_weight[history]
        i = bisect.bisect_left(arcs, (x, None))
        _, target = arcs[i]
        return target


class MarkovChain(TransitionGraphDrivenMixin, StateMachine):
    """In a Markov chain, the target state of a transition depends not on an input symbol,
    but on a weight assigned to each outgoing arc. The target state is randomly selected with
    each target state having a probability proportional to its weight.

    This class supports Markov chains with arbitrary finite memory. Memory size is automatically
    computed as the longest number of prior states in the transition graph.
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
        memory = max(len(h) for h in self.transition_graph.arcs.keys())
        self._history = collections.deque(maxlen=memory)
        if rng is not None:
            self.rng = rng

    def step(self, n=1):
        """Advance the Markov chain `n` steps.

        Call this method on Markov chains instead of using `input()`. Markov chains any ignore
        input symbols, and instead base their transitions on recent state(s) and the RNG.
        """
        for _ in range(n):
            self.input(None)

    def _enter(self, state, args, kwargs):
        self._history.append(state)
        return super()._enter(state, args, kwargs)

    def target(self, source, symbol):
        """The transition target is obtained from the transition graph, and does not depend on
        any input symbol. Instead, the transition graph uses the chain's recent history (which
        includes the current state) and its RNG to obtain the next state.
        """
        return self.transition_graph.target(tuple(self._history), self.rng)
