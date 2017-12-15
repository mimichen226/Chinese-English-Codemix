import json
import cer
import argparse

argparser = argparse.ArgumentParser()
argparser.add_argument('inp', metavar='input', help='input file')
argparser.add_argument('output', metavar='output', help='output file')
args = argparser.parse_args()

ALPHA = {'a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z',\
		'A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z'}

def check_if_english(word):
	return set(list(word)).issubset(ALPHA)

# Get English to Chinese dictionary
with open("ecdict.json") as f:
	ecdict = json.load(f)

mixed = []
#with open("./data/mixed.dev") as f2:
with open(args.inp) as f2:
	for line in f2.readlines():
		mixed.append(line.rstrip())

# Go through every line in the test data
data = []

f = open(args.output, "w")
english = 0
translated = 0
for i in range(len(mixed)):
	words = []
	# Go through every word in the line
	for word in mixed[i].split():
		# Check if the word is English
		#if check_if_english(word):
		if check_if_english(word):
			english += 1
			# Translate into Chinese if possible
			if word in ecdict.keys():
				word = ecdict[word][0]
				translated += 1
		words.append(word)
	print("{}".format("  ".join(words)))
	f.write("  ".join(words)+"\n")
f.close()
print("Found {} English words; Translated {} English words to Chinese".format(english, translated))
print("{:.2f}% translated".format(float(translated)/ english* 100))
