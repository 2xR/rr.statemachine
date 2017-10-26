import collections


Input = collections.namedtuple("Input", ["symbol", "args", "kwargs"])
Transition = collections.namedtuple("Transition", ["source", "input", "target"])


class StateMachine:

    initial_state = None  # can be defined as class attribute or instance attribute/property

    def __init__(self, initial_state=None):
        if initial_state is not None:
            self.initial_state = initial_state  # override initial state directly on instance
        self._state = None  # current state (None means undefined/uninitialized)
        self._transition = None  # ongoing transition
        self._input = collections.deque()  # unprocessed input queue

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
        states, and the input that triggered the transition.
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

    def start(self, *args, **kwargs):
        """Start the machine by entering its initial state."""
        if self.started:
            raise RuntimeError("state machine has already been started")
        if self.initial_state is None:
            raise ValueError("undefined initial state")
        self._enter(self.initial_state, args, kwargs)

    def input(self, symbol, *args, **kwargs):
        """Feed a `symbol` into the state machine to trigger a state transition."""
        if not self.started:
            raise RuntimeError("state machine must be started")
        self._input.append(Input(symbol, args, kwargs))
        self._resolve()

    def _resolve(self):
        """Resolve pending transitions, *i.e.* process queued inputs.

        Pending inputs are kept in a FIFO queue to ensure that enter/exit/transition handlers
        are executed in the correct order.
        """
        if self.transitioning:
            return  # we're already in the midst of resolving transitions
        while len(self._input) > 0:
            source = self._state
            input = self._input.popleft()
            # Set the transition to indicate that we're transitioning. This way, if a weird
            # `.target()` method inputs any symbols into the state machine, `._resolve()` will
            # return immediately. However, the actual transition target is still unknown at this
            # point, so it is set to `None`.
            self._transition = Transition(source, input, None)
            target = self.target(source, input.symbol)
            if target is None:
                raise ValueError("undefined target state")
            transition = Transition(source, input, target)
            self._transition = transition
            self._exit(source)
            self.on_transition(transition)
            self._enter(target, input.args, input.kwargs)
        self._transition = None

    def _enter(self, state, args, kwargs):
        self._state = state
        self.on_enter(state, *args, **kwargs)

    def _exit(self, state):
        self.on_exit(state)
        self._state = None

    def target(self, state, symbol):
        """Given a state and an input symbol, return the machine's next state."""
        raise NotImplementedError()

    def on_enter(self, state, *args, **kwargs):
        """Perform actions associated with the event of entering the argument `state`."""
        pass

    def on_exit(self, state):
        """Perform actions associated with the event of leaving the argument `state`."""
        pass

    def on_transition(self, transition):
        """Perform actions associated with the argument `transition`.

        Note that this occurs between the exit handler of the source state and the enter handler
        of the target state, and the machine's `state` is undefined (None) at this stage. The
        states involved in the transition can be accessed through the `source` and `target`
        attributes of `transition`, and the symbol that triggered the transition can be obtained
        through the `symbol` attribute.
        """
        pass
