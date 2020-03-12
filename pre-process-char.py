
def load_doc(filename):
    file = open(filename, 'r')
    # read all text
    text = file.read()
    # close the file
    file.close()
    return text

raw_text = load_doc('data/shakespeare.txt')
tokens = raw_text.split()
raw_text = ' '.join(tokens)
# Remove number of sonnet
raw_text = ''.join([i for i in raw_text if not i.isdigit()])
raw_text = raw_text.lower()

length = 40
sequences = list()
for i in range(length, len(raw_text)):
	# select sequence of tokens
	seq = raw_text[i-length:i+1]
	# store
	sequences.append(seq)

# save tokens to file, one dialog per line
def save_doc(lines, filename):
	data = '\n'.join(lines)
	file = open(filename, 'w')
	file.write(data)
	file.close()

# save sequences to file
out_filename = 'data/char_sequences.txt'
save_doc(sequences, out_filename)