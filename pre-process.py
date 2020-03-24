import re

def load_doc(filename):
    file = open(filename, 'r')
    # read all text
    text = file.read()
    # close the file
    file.close()
    return text

raw_text = load_doc('data/shakespeare.txt')
tokens = re.split("\s", raw_text)
raw_text = ' '.join(tokens)
# Remove number of sonnet
raw_text = ''.join([i for i in raw_text if not i.isdigit()])
raw_text = raw_text.lower()
raw_text = re.split("\s", raw_text)
while("" in raw_text) :
    raw_text.remove("")

length = 40
sequences = list()
for i in range(length, len(raw_text)):
	# select sequence of tokens
	seq = raw_text[i-length:i]
	# store
	sequences.append(seq)


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

