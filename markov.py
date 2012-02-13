#!/usr/bin/env python
from argparse import ArgumentParser, FileType
from os.path import isfile, abspath
from sys import exit, stdout
from re import split, compile
from random import choice

def argparser():
	desc = "Generates pseudo-random sentences using a body of work."
	parser = ArgumentParser(description=desc)
	parser.add_argument("--input", type=FileType("r"), default="-",
						help="Path to the source material to generate from")
	parser.add_argument("--output", default=stdout, type=FileType("w"),
						help="The output file. Defaults to stdout")
	parser.add_argument("--length", default=10, type=int,
						help="The number of sentences to generate")
	parser.add_argument("--size", default=25, type=int,
						help="The length of each sentences to generate")

	return parser

def srcparse(src):
	punctuation = compile(r'[*.?!,":;-]')
	word_list = split('\s+', punctuation.sub("", src).lower())
	word_endings = {} 

	if len(word_list) < 3:
		print "Source material must contain at least %s words" % group_size
		exit(1)

	for i in range(len(word_list) - 2):
		w1 = word_list[i]
		w2 = word_list[i + 1]
		w3 = word_list[i + 2]
		key = (w1, w2)

		# Generate doubles
		if w1 in word_endings:
			word_endings[w1].append(w2)
		else:
			word_endings[w1] = [w2]

		# Generate triples
		if key in word_endings:
			word_endings[key].append(w3)
		else:
			word_endings[key] = [w3]

	return word_list, word_endings

def punctuate(sentence):
	# See if the sentence contains any interrogative words
	return " ".join(sentence).capitalize() + choice([".", "?", "!"])

def generate(words, endings, sentences=10, sentence_size=25):
	output, sentence = [], []
	w1, w2 = None, None
	iterations = 0

	while sentences > 0:
		end_sentence = False

		if w1 is None:
			w1 = choice(words)
			w2 = choice(endings[w1])

		sentence.append(w1)

		key = (w1, w2)

		iterations += 1

		if key in endings:
			if iterations >= sentence_size and len(endings[key]) == 1:
				end_sentence = True
				w2 = choice(endings[w1])
			else:
				w1, w2 = w2, choice(endings[key])
		else:
			end_sentence = True

		if end_sentence:
			if w2 is not None:
				sentence.append(w2)
			output.append(punctuate(sentence))
			w1, w2, sentence, iterations = None, None, [], 0
			sentences -= 1

	return " ".join(output)

def main():
	args = argparser().parse_args()
	words, endings = srcparse(args.input.read())
	args.output.write(generate(words, endings, args.length, args.size) + "\n")

if __name__ == "__main__":
	main()

