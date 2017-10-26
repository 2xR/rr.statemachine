class DynamicDispatchMixin:
    """A mixin which adds dynamic dispatch of state machine events --- enter state, exit state,
    and transition --- to different methods according to the states (and input symbol) involved.
    These methods are looked up and, if they're callable, are called with the positional and
    keyword arguments that accompany the input symbol (passed to `.input()`).

    Note that usage of this mixin makes sense only when states and symbols are representable as
    strings, as the name of the method to which an event is dispatched is built from a format
    string that, by default, uses the state or transition symbol.

    As an example, for a machine in state 'a' receiving symbol 's' as input and moving into state
    'b', the following handlers would be called (if they exist and are callable):

        on_exit_a()
        on_transition_a_s_b()
        on_enter_b()

    The names of the methods to which these events are dispatched can be customized by redefining
    the format strings `enter_handler_name`, `exit_handler_name` and `transition_handler_name`.
    """

    enter_handler_name = "on_enter_{0}"
    exit_handler_name = "on_exit_{0}"
    transition_handler_name = "on_transition_{0.source}_{0.input.symbol}_{0.target}"

    def on_enter(self, state, *args, **kwargs):
        handler = getattr(self, self.enter_handler_name.format(state), None)
        return handler(*args, **kwargs) if callable(handler) else None

    def on_exit(self, state):
        handler = getattr(self, self.exit_handler_name.format(state), None)
        return handler() if callable(handler) else None

    def on_transition(self, transition):
        handler = getattr(self, self.transition_handler_name.format(transition), None)
        return handler() if callable(handler) else None
