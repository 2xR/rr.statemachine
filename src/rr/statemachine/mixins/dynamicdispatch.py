from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals


class DynamicDispatchMixin(object):
    """Useful for state machines using strings to represent states. This mixin should appear in
    the list of base classes before the StateMachine class. Handlers are dynamically dispatched
    to different methods according to the states and symbols involved.

    For example, for a machine in state 'a' receiving symbol 's' as input and moving into state
    'b', the following handlers would be called (if they exist and are callable):
        exit_a()
        transition_a_s_b()
        enter_b()
    """

    def enter_handler(self, state):
        handler = getattr(self, "enter_handler_{}".format(state), None)
        if callable(handler):
            return handler()

    def exit_handler(self, state):
        handler = getattr(self, "exit_handler_{}".format(state), None)
        if callable(handler):
            return handler()

    def transition_handler(self, transition):
        handler = getattr(self, "transition_handler_{}_{}_{}".format(*transition), None)
        if callable(handler):
            return handler()
