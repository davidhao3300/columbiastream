import string

sent_filename = "output.txt"
sent_dict = dict()
sent_reader = open(sent_filename)
for inline in sent_reader:
    # Get the word.
	row = inline.split()
	#print row

	word = row[0]
    # Strip its punctuation.
	for punctuation in string.punctuation:
        # Remove all the special punctuations 
        # (string.punctuation=!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~)
		word = word.replace(punctuation, " ")
    # Get the sentiment value.
	value = float(row[1])
    # Set the key-value pair in the dictionary.
	sent_dict[word] = value;

print sent_dict