import collections


Transition = collections.namedtuple("Transition", ["source", "symbol", "target"])


class StateMachine:

    initial_state = None  # can be defined as class attribute or instance attribute/property

    def __init__(self, initial_state=None):
        if initial_state is not None:
            self.initial_state = initial_state  # override initial state directly on instance
        self._state = None  # current state (None means undefined/uninitialized)
        self._transition = None  # ongoing transition
        self._symbols = collections.deque()  # unprocessed input symbols queue

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
            raise RuntimeError("state machine has already been started")
        if initial_state is None:
            initial_state = self.initial_state
        if initial_state is None:
            raise ValueError("undefined initial state")
        self._state = initial_state
        self.on_enter(initial_state)

    def input(self, symbol):
        """Feed a `symbol` into the state machine to trigger a state transition."""
        if not self.started:
            raise RuntimeError("state machine must be started")
        self._symbols.append(symbol)
        self._resolve()

    def _resolve(self):
        """Resolve pending transitions, *i.e.* process queued input symbols.

        Pending symbols are kept in a FIFO queue to ensure that enter/exit/transition handlers
        are executed in the correct order.
        """
        if self.transitioning:
            return  # we're already in the midst of resolving transitions
        while len(self._symbols) > 0:
            source = self._state
            symbol = self._symbols.popleft()
            target = self.target(source, symbol)
            if target is None:
                raise ValueError("undefined target state")
            transition = Transition(source=source, symbol=symbol, target=target)
            self._transition = transition
            self.on_exit(source)
            self._state = None  # state becomes "undefined" in the middle of the transition
            self.on_transition(transition)
            self._state = target
            self.on_enter(target)
        self._transition = None

    def target(self, state, symbol):
        """Given a state and an input symbol, return the machine's next state."""
        raise NotImplementedError()

    def on_enter(self, state):
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
