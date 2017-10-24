class TransitionGraph:
    """An object defining a graph that can be used to drive the transitions of a state machine."""

    def update(self, transitions):
        for transition in transitions:
            self.add(transition)

    def add(self, transition):
        raise NotImplementedError()

    def target(self, source, symbol):
        raise NotImplementedError()


class TransitionGraphDrivenMixin:
    """A mixin for state machine classes that uses a `TransitionGraph` object to obtain the
    target state in its `target()` method. The transition graph can be defined at class or
    instance level.
    """

    # Redefine this in subclasses to provide a class-level transition graph that is used as a
    # default when no transition graph is provided to __init__().
    transition_graph = None

    def __init__(self, transition_graph=None):
        if transition_graph is not None:
            self.transition_graph = transition_graph
        if not isinstance(self.transition_graph, TransitionGraph):
            raise TypeError("transition graph expected")

    def target(self, state, symbol):
        return self.transition_graph.target(state, symbol)
