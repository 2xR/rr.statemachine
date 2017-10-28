from rr.statemachine import FiniteStateAutomaton


class Foo(FiniteStateAutomaton):

    initial_state = "bar"
    transition_graph = FiniteStateAutomaton.TransitionGraph([
        ("bar", "f", "foo"),
        ("bar", "s", "spam"),
        ("foo", "b", "bar"),
        ("spam", "h", "ham"),
        ("spam", "f", "foo"),
    ])

    def on_transition(self, transition):
        print("T {}".format(transition))

    def on_enter(self, state, *args, **kwargs):
        print("> {} {} {}".format(state, args, kwargs))

    def on_exit(self, state):
        print("< {}".format(state))


f = Foo()
f.start()
f.input("f")
f.input("b")
f.input("s")
f.input("h")
