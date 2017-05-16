import copy

from context import conlanger

words = []
with open('input.txt', 'r') as f:
    for line in f:
        words.append(conlanger.core.Word(lexeme=line[:-1]))

with open('rules.txt', 'r') as f:
    parsed_words = conlanger.sce.apply_ruleset(copy.deepcopy(words), f.read(), debug=True)

for word_in, word_out in zip(words, parsed_words):
    print(f"{word_in} → {word_out}")
