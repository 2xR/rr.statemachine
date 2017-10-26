from .finitestateautomaton import FiniteStateAutomaton
from .markovchain import MarkovChain
from .statemachine import StateMachine
from .dynamicdispatch import DynamicDispatchMixin

__version__ = "0.4.0"
__author__ = "Rui Rei"
__copyright__ = "Copyright 2017 {author}".format(author=__author__)
__license__ = "MIT"


def _dd_example():

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
    return b


def _fsa_example():

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

        def on_enter(self, state):
            print("> {}".format(state))

        def on_exit(self, state):
            print("< {}".format(state))

    f = Foo()
    f.start()
    f.input("f")
    f.input("b")
    f.input("s")
    f.input("h")
    return f


def _mc_example(text=None, memory=1):
    """Call this function with some text to get a Markov chain generated from the words in the
    text. `start()` the chain and then call `step()` on it to get a stream of words (based on the
    input text) printed to stdout.
    """
    import collections
    import pathlib
    import string

    if text is None:
        sample_file = pathlib.Path(__file__).parents[3] / "sample_text.txt"
        if sample_file.exists():
            text = sample_file.read_text()

    trans_table = str.maketrans("", "", string.punctuation)
    words = text.translate(trans_table).lower().split()
    arcs = collections.defaultdict(collections.Counter)
    history = collections.deque(maxlen=memory)
    for i in range(len(words)):
        history.append(words[i])
        next_word = words[(i+1) % len(words)]
        arcs[tuple(history)][next_word] += 1

    chain = MarkovChain(
        initial_state=words[0],
        transition_graph=MarkovChain.TransitionGraph(
            (hist, count, target)
            for hist, hist_arcs in arcs.items()
            for target, count in hist_arcs.items()
        ),
    )
    chain.text = text
    chain.words = words
    chain.output = []
    chain.on_enter = chain.output.append
    chain.print = lambda: print(" ".join(chain.output))
    return chain
