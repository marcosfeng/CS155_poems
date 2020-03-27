import json
from pathlib import Path
import re

import inflect
import numpy as np
import pandas as pd

root_path = Path('../..')
input_path = root_path / 'input'
dictionary_path = input_path / 'dictionaries'
poem_path = input_path / 'poems'
raw_path = poem_path / 'data'

all_haikus = []

# Load the file
df = pd.read_csv(str('data/shakespeare2.txt'), sep = "/n")

df['number'] = (df.index+1)%15
df = df[df['number'] != 0]
df.reset_index(drop=True, inplace=True)
df['sonnet'] = (df.index)//14
df = df.pivot(index='sonnet', columns='number', values='1')
all_haikus.append(df)
df.head()

all_haikus = pd.concat(all_haikus, sort=False)

all_haikus['hash'] = (all_haikus[1] + all_haikus[2] + all_haikus[3] +
                      all_haikus[4] + all_haikus[5] + all_haikus[6] +
                      all_haikus[7] + all_haikus[8] + all_haikus[9] +
                      all_haikus[10] + all_haikus[11] + all_haikus[12] +
                      all_haikus[13] + all_haikus[14]).str.replace(r'[^A-Za-z]', '').str.upper()

#all_haikus

# Load Phonemes

# Standard Dict
WORDS = {}
f = open('dict/cmudictdict.txt', "r")
for line in f.readlines():
    word, phonemes = line.strip().split(' ', 1)
    word = re.match(r'([^\(\)]*)(\(\d\))*', word).groups()[0]
    phonemes = phonemes.split(' ')
    syllables = sum([re.match(r'.*\d', p) is not None for p in phonemes])
    if word not in WORDS:
        WORDS[word] = []
    WORDS[word].append({
        'phonemes': phonemes,
        'syllables': syllables
    })
f.close()

# Load custom phonemes
CUSTOM_WORDS = {}
vowels = ['AA', 'AE', 'AH', 'AO', 'AW', 'AX', 'AXR', 'AY', 'EH', 'ER', 'EY', 'IH', 'IX', 'IY', 'OW', 'OY', 'UH', 'UW',
          'UX']
f = open('dict/customdict.txt', "r")
for line in f.readlines():
    try:
        word, phonemes = line.strip().split('\t', 1)
    except:
        print(line)
        continue
    word = re.match(r'([^\(\)]*)(\(\d\))*', word).groups()[0].lower()
    phonemes = phonemes.split(' ')
    syllables = sum([(p in vowels) for p in phonemes])

    if word not in CUSTOM_WORDS:
        CUSTOM_WORDS[word] = []
    CUSTOM_WORDS[word].append({
        'phonemes': phonemes,
        'syllables': syllables
    })
f.close()

inflect_engine = inflect.engine()

# Dictionary of words not found, must go get the phonemes
# http://www.speech.cs.cmu.edu/tools/lextool.html
NOT_FOUND = set()


def get_words(line):
    """
    Get a list of the words in a line
    """
    line = line.lower()
    # Replace numeric words with the words written out
    ws = []
    for word in line.split(' '):
        if re.search(r'\d', word):
            x = inflect_engine.number_to_words(word).replace('-', ' ')
            ws = ws + x.split(' ')
        else:
            ws.append(word)

    line = ' '.join(ws)

    words = []
    for word in line.split(' '):
        word = re.match(r'[\'"]*([\w\']*)[\'"]*(.*)', word).groups()[0]
        word = word.replace('_', '')
        words.append(word)

    return words


def count_non_standard_words(line):
    """
    Count the number of words on the line that don't appear in the default CMU Dictionary.
    """
    count = 0
    for word in get_words(line):
        if word and (word not in WORDS):
            count += 1
    return count


def get_syllable_count(line):
    """
    Get the possible syllable counts for the line
    """
    counts = [0]
    return_none = False
    for word in get_words(line):
        try:
            if word:
                if (word not in WORDS) and (word not in CUSTOM_WORDS):
                    word = word.strip('\'')

                if word in WORDS:
                    syllables = set(p['syllables'] for p in WORDS[word])
                else:
                    syllables = set(p['syllables'] for p in CUSTOM_WORDS[word])
                # print(syllables)
                new_counts = []
                for c in counts:
                    for s in syllables:
                        new_counts.append(c + s)

                counts = new_counts
        except:
            NOT_FOUND.add(word)
            return_none = True

    if return_none:
        return None

    return ','.join([str(i) for i in set(counts)])


# Remove haikus with lots of unknown words
# Likely either non-english or just lots of typos
all_haikus['unknown_word_count'] = np.sum([all_haikus[i+1].apply(count_non_standard_words) for i in range(14)], axis=0)
all_haikus = all_haikus[all_haikus['unknown_word_count'] < 3].copy()

for i in range(14):
    all_haikus['%s_syllables' % i] = all_haikus[i].apply(get_syllable_count)

# print("Unknown Words: ", len(NOT_FOUND))
'''
with open('unrecognized_words.txt', 'w') as f:
    for w in NOT_FOUND:
        f.write(w)
        f.write('\n')
'''
all_haikus