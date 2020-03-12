import nltk
nltk.download('punkt')
nltk.download('cmudict')
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import cmudict


d_pronoun = cmudict.dict()
tokenizer = RegexpTokenizer('\w[\w|\'|-]*\w|\w')

f = open('data/shakespeare.txt')
line_tokens = []
for line in f:
    line = line.strip()
    if (line.isdigit()):
        continue
    if (len(line) > 0):
        line = line.lower()
        tokens = tokenizer.tokenize(line)
        if len(tokens) > 1:
            line_tokens.append(tokens)

