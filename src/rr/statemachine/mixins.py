from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals


class DynamicDispatchMixin(object):
    """A mixin which adds dynamic dispatch of state machine events --- enter state, exit state,
    and transition --- to different methods according to the states (and transition symbol)
    involved. These methods are looked up and, if they're callable, are called without any
    arguments. Note that usage of this mixin makes sense only when states are represented as
    strings.

    As an example, for a machine in state 'a' receiving symbol 's' as input and moving into state
    'b', the following handlers would be called (if they exist and are callable):

        exit_a()
        transition_a_s_b()
        enter_b()

    The names of the methods to which these events are dispatched can be configured by defining
    the class/instance attributes `enter_handler_format`, `exit_handler_format` and
    `transition_handler_format`.
    """

    enter_handler_format = "enter_handler_{0}"
    exit_handler_format = "exit_handler_{0}"
    transition_handler_format = "transition_handler_{0.source}_{0.symbol}_{0.target}"

    def enter_handler(self, state):
        handler = getattr(self, self.enter_handler_format.format(state), None)
        return handler() if callable(handler) else None

    def exit_handler(self, state):
        handler = getattr(self, self.exit_handler_format.format(state), None)
        return handler() if callable(handler) else None

    def transition_handler(self, transition):
        handler = getattr(self, self.transition_handler_format.format(transition), None)
        return handler() if callable(handler) else None
