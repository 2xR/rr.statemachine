from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from . import mixins
from .finitestateautomaton import FiniteStateAutomaton
from .markovchain import MarkovChain
from .statemachine import StateMachine

__version__ = "0.2.0"
__author__ = "Rui Rei"
__copyright__ = "Copyright 2017 {author}".format(author=__author__)
__license__ = "MIT"


def _dd_example():

    class Bar(mixins.DynamicDispatchMixin, FiniteStateAutomaton):

        initial_state = "a"
        transitions = [
            ("a", "x", "b"),
            ("b", "y", "a"),
            ("b", "z", "b"),
        ]

        def enter_handler(self, state):
            print(">>> {}".format(state))

        def transition_handler_b_z_b(self):
            print("loop")

        def exit_handler_b(self):
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
        transitions = [
            ("bar", "f", "foo"),
            ("bar", "s", "spam"),
            ("foo", "b", "bar"),
            ("spam", "h", "ham"),
            ("spam", "f", "foo"),
        ]

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


def _mc_example(text):
    """Call this function with some text to get a Markov chain generated from the words in the
    text. `start()` the chain and then call `step()` on it to get a stream of words (based on the
    input text) printed to stdout.
    """
    import collections
    import string

    trans_table = str.maketrans("", "", string.punctuation)
    words = text.translate(trans_table).lower().split()
    arcs = collections.defaultdict(collections.Counter)
    for i in range(1, len(words)):
        curr_word = words[i]
        next_word = words[(i+1) % len(words)]
        arcs[curr_word][next_word] += 1

    chain = MarkovChain(
        initial_state=words[0],
        transitions=[
            (source, count, target)
            for source, source_arcs in arcs.items()
            for target, count in source_arcs.items()
        ],
    )
    chain.enter_handler = print
    chain.text = text
    chain.words = words
    return chain
