import collections
import pathlib
import re

from rr.statemachine import MarkovChain

word_re = re.compile(r"\w+([-']\w*)*")
punctuation_re = re.compile(r"[.,:;!?\"]")
token_re = re.compile("({})|({})".format(word_re.pattern, punctuation_re.pattern))


def tokenize(text):
    return [match.group(0) for match in token_re.finditer(text.lower())]


def assemble(tokens):
    return " ".join(tokens)


class TextGenerator(MarkovChain):

    def __init__(self, text=None, memory=1):
        if text is None:
            sample_file = pathlib.Path(__file__).parent / "sample_text.txt"
            if sample_file.exists():
                text = sample_file.read_text()

        tokens = tokenize(text)
        arcs = collections.defaultdict(collections.Counter)
        history = collections.deque(maxlen=memory)
        for token in tokens:
            arcs[tuple(history)][token] += 1
            history.append(token)

        MarkovChain.__init__(self, transition_graph=MarkovChain.TransitionGraph(
            (hist, count, target)
            for hist, hist_arcs in arcs.items()
            for target, count in hist_arcs.items()
        ))
        self.text = text
        self.tokens = tokens
        self.output = []

    def on_enter(self, state, *args, **kwargs):
        self.output.append(state)

    def sentence(self):
        while True:
            self.step()
            if self.state in [".", "!", "?"]:
                return self.flush()

    def sentences(self, n):
        return "\n".join(self.sentence() for _ in range(n))

    def flush(self):
        text = assemble(self.output)
        del self.output[:]
        return text
