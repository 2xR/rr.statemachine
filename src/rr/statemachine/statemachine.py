from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import collections


Transition = collections.namedtuple("Transition", ["source", "symbol", "target"])


class StateMachine(object):

    initial_state = None  # can be defined as class attribute or instance attribute/property

    def __init__(self, initial_state=None):
        if initial_state is not None:
            self.initial_state = initial_state  # override initial state directly on instance
        self._state = None  # current state (NOTE: cannot be None)
        self._transition = None  # ongoing transition
        self._symbols = collections.deque()  # pending symbols

    def __str__(self):
        return "{}({!r})".format(type(self).__name__, self._state)

    def __repr__(self):
        return "<{} @{:x}>".format(str(self), id(self))

    @property
    def state(self):
        """The current state of the state machine. Can be `None` during a transition."""
        return self._state

    @property
    def transition(self):
        """Retrieve the currently ongoing transition. Can be used to obtain source and target
        states, and the symbol that triggered the transition.
        """
        return self._transition

    @property
    def transitioning(self):
        """True iff a transition is currently underway."""
        return self._transition is not None

    @property
    def started(self):
        """True iff the machine has been `start()`ed."""
        return self._state is not None or self._transition is not None

    def start(self, initial_state=None):
        """Start the machine by entering the argument `initial_state`.

        If an initial state argument is not given, it is obtained from the `StateMachine` object.
        This allows us to define a default initial state at instance or class level, and override
        it when calling `start()` if desired.
        """
        if self.started:
            raise ValueError("state machine has already been started")
        if initial_state is None:
            initial_state = self.initial_state
        if initial_state is None:
            raise ValueError("undefined initial state")
        self._state = initial_state
        self.enter_handler(initial_state)

    def input(self, symbol):
        """Feed a `symbol` into the state machine to trigger a transition to a different state."""
        self._symbols.append(symbol)
        self._resolve()

    def _resolve(self):
        """Resolve pending transitions. Pending symbols are kept in a FIFO queue to ensure that
        enter/exit/transition handlers are executed in the correct order.
        """
        if self._transition is not None:
            return  # we're already in the midst of resolving transitions
        while len(self._symbols) > 0:
            source = self._state
            symbol = self._symbols.popleft()
            target = self.transition_target(source, symbol)
            if target is None:
                raise ValueError("undefined target state")
            transition = Transition(source=source, symbol=symbol, target=target)
            self._transition = transition
            self.exit_handler(source)
            self._state = None  # state becomes "undefined" in the middle of the transition
            self.transition_handler(transition)
            self._state = target
            self.enter_handler(target)
        self._transition = None

    def transition_target(self, state, symbol):
        """Given the current state and an input symbol, return the state the machine should
        transition into.
        """
        raise NotImplementedError()

    def transition_handler(self, transition):
        """Perform actions associated with a `transition`.

        Note that this occurs between the exit handler of the source state and the enter handler
        of the target state, and the machine's `state` is undefined (None) at this stage.
        """
        pass

    def enter_handler(self, state):
        """Perform actions associated with the event of entering the argument `state`."""
        pass

    def exit_handler(self, state):
        """Perform actions associated with the event of leaving the argument `state`."""
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

        def transition_target(self, state, symbol):
            return self.transition_map[state][symbol]

        def transition_handler(self, transition):
            print("T {}".format(transition))

        def enter_handler(self, state):
            print("> {}".format(state))

        def exit_handler(self, state):
            print("< {}".format(state))

    f = Foo()
    f.start()
    f.input("f")
    f.input("b")
    f.input("s")
    f.input("h")
    return f
