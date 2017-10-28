from rr.statemachine import FiniteStateAutomaton, DynamicDispatchMixin


class Bar(DynamicDispatchMixin, FiniteStateAutomaton):

    initial_state = "a"
    transition_graph = FiniteStateAutomaton.TransitionGraph([
        ("a", "x", "b"),
        ("b", "y", "a"),
        ("b", "z", "b"),
    ])
    transition_handler_name = "on_transition_{0.source}_{0.target}"

    def on_enter(self, state, *args, **kwargs):
        print(">>> {} {} {}".format(state, args, kwargs))

    def on_transition_b_b(self):
        print("loop b")

    def on_exit_b(self):
        print("b >>>")


b = Bar()
b.start()
b.input("x")
b.input("y")
b.input("x")
b.input("z")
