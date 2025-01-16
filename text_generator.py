from nltk import WhitespaceTokenizer, ngrams
from collections import Counter
from random import choice, choices
import regex as re


class TextGenerator:
    def __init__(self, corpus):
        self.corpus = corpus
        self.tokens = self.tokenize()
        self.trigrams = self.make_trigrams()
        self.markov = {}

    def tokenize(self):
        tokenizer = WhitespaceTokenizer()
        return tokenizer.tokenize(self.corpus)

    def make_trigrams(self):
        tgrms = ngrams(self.tokens, 3)
        return [(t[0] + ' ' + t[1], t[2]) for t in tgrms]

    def set_markov(self):
        for trigram in self.trigrams:
            head = trigram[0]
            tail = trigram[1]
            if head not in self.markov:
                self.markov[head] = []
            self.markov[head].append(tail)

        for head in self.markov.keys():
            self.markov[head] = dict(sorted(Counter(self.markov[head]).items(), key=lambda x: -x[1]))

    def get_proper_head(self):
        while True:
            curr_head = choice(list(self.markov.keys()))
            if re.match(r"^[A-Z]\w*[^\.\?!]\w*[^\.\?!]$", curr_head):
                return curr_head

    def get_pseudo(self):
        for i in range(10):
            curr_head = self.get_proper_head()
            curr_sent = [*curr_head.split(" ")]
            while True:
                prob_tails = list(self.markov[curr_head].keys())
                weights = list(self.markov[curr_head].values())
                first_part_of_head, second_part_of_head = curr_head.split(" ")
                tail = choices(prob_tails, weights=weights)[0]
                curr_sent.append(tail)
                curr_head = second_part_of_head + ' ' + tail
                if len(curr_sent) >= 5 and re.match(r".*[\.\?!]$", curr_head):
                    break

            print(" ".join(curr_sent))


path = input()
with open(f"./{path}", "r", encoding="utf-8") as f:
    data = f.read()
    gen = TextGenerator(data)

gen.set_markov()
gen.get_pseudo()
