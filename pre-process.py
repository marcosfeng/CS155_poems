import pandas as pd
import matplotlib.pyplot as plt
import time

import re
import nltk
import spacy
import keras


corpus = open('data/shakespeare.txt').read()

print(corpus)
