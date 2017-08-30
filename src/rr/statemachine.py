from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import collections


__version__ = "0.1.0"
__author__ = "Rui Rei"
__copyright__ = "Copyright 2017 {author}".format(author=__author__)
__license__ = "MIT"


Transition = collections.namedtuple("Transition", ["state", "args", "kwargs"])


class StateMachine(object):

    initial_state = None  # can be defined as class attribute or instance attribute/property

    def __init__(self, initial_state=None):
        if initial_state is not None:
            self.initial_state = initial_state  # starting state
        self._state = None  # current state
        self._ongoing_transition = None  # current transition
        self._pending_transitions = collections.deque()  # pending transitions

    def __str__(self):
        return "{}({!r})".format(type(self).__name__, self._state)

    def __repr__(self):
        return "<{} @{:x}>".format(str(self), id(self))

    @property
    def state(self):
        return self._state

    @property
    def transitioning(self):
        return self._ongoing_transition is not None

    @property
    def started(self):
        return self.state is not None or self.transitioning

    def start(self, *args, **kwargs):
        if self.started:
            raise ValueError("state machine has already been started")
        self._state = self.initial_state
        self.enter_action(self._state, *args, **kwargs)

    def input(self, symbol, *args, **kwargs):
        target_state = self.transition(self._state, symbol)
        self._pending_transitions.append(Transition(target_state, args, kwargs))
        self._resolve()

    def _resolve(self):
        """Resolve pending transitions. Pending transitions are kept in a FIFO queue in order to
        ensure that all transitions are resolved in the correct order.
        """
        if self._ongoing_transition is not None:
            return  # we're already in the midst of resolving transitions
        while len(self._pending_transitions) > 0:
            transition = self._pending_transitions.popleft()
            self._ongoing_transition = transition
            self.exit_action(self._state)
            self._state = transition.state
            self.enter_action(self._state, *transition.args, **transition.kwargs)
        self._ongoing_transition = None

    def transition(self, state, symbol):
        """Given the current state and an input symbol, return the state the machine should
        transition into.
        """
        raise NotImplementedError()

    def enter_action(self, state, *args, **kwargs):
        """Perform an action associated with the event of entering the argument `state`."""
        pass

    def exit_action(self, state):
        """Perform an action associated with the event of leaving the argument `state`."""
        pass


def _example():

    class Foo(StateMachine):

        initial_state = "bar"
        transition_map = {
            "bar": {
                "f": "foo",
                "s": "spam",
            },
            "foo": {
                "b": "bar",
            },
            "spam": {
                "h": "ham",
                "f": "foo",
            },
        }

        def transition(self, state, symbol):
            return self.transition_map[state][symbol]

        def enter_action(self, state, *args, **kwargs):
            print("Entering state {} with {} and {}".format(state, args, kwargs))

        def exit_action(self, state):
            print("Leaving state {}".format(state))

    f = Foo()
    f.start()
    f.input("f")
    f.input("b")
    f.input("s")
    f.input("h")
    return f
