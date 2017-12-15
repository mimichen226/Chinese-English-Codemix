import pickle
import requests
import json
import enchant
import argparse

ALPHA = {'a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z',\
		'A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z'}

def check_if_english(word):
	return set(list(word)).issubset(ALPHA)

def wikiCheck(eng_arr):
	#eng_arr = ["Backstreet", "Boys"]
	eng_arr = " ".join(eng_arr).title().split() # titlize the words
	r = requests.get("https://en.wikipedia.org/w/api.php?action=query&format=json&prop=langlinks&titles={}&lllang=zh".format("%20".join(eng_arr)))
	resp = json.loads(r.content)
	for pg_id in resp['query']['pages']:
		try:
			print(resp['query']['pages'][pg_id]['langlinks'])
			return resp['query']['pages'][pg_id]['langlinks'][0]["*"]
		except: 
			return -1

if __name__ == "__main__":
	argparser = argparse.ArgumentParser()
	argparser.add_argument('inp', metavar='input', help='input file')
	argparser.add_argument('output', metavar='output', help='output file')
	args = argparser.parse_args()

	prob_ecdict = pickle.load( open("prob_ecdict.pickle", "rb"))
	f1 = open(args.output, "w")

	translated = 0
	english = 0

	with open(args.inp) as f:
		for line in f.readlines():
			sent_arr = line.rstrip().split()
			new = []
			eng_sub = []
			for word in sent_arr:
				# English word
				if check_if_english(word):
					english += 1
					# Known Eng word -- pick best probability
					if word in prob_ecdict.keys() or word.title() in prob_ecdict.keys():
						new = new + eng_sub
						eng_sub = []

					if word in prob_ecdict.keys():
						poss_tran = sorted(prob_ecdict[word].items(), key=lambda item: (item[1], item[0]))
						top_tran = poss_tran[len(poss_tran) - 1][0]
						if top_tran != "NULL":
							new.append(top_tran)
						translated += 1
					elif word.title() in prob_ecdict.keys():
						poss_tran = sorted(prob_ecdict[word.title()].items(), key=lambda item: (item[1], item[0]))
						top_tran = poss_tran[len(poss_tran) - 1][0]
						if top_tran != "NULL":
							new.append(top_tran)
						translated += 1
					# Unknown Eng word -- try translating the sub group with Wikipedia
					else:
						eng_sub.append(word)
						wiki = wikiCheck(eng_sub)
						if wiki != -1: 
							translated += 1
							new.append(wiki)
							eng_sub = []
				# Chinese word
				else: 
					new = new + eng_sub + [word]
					eng_sub = []
			print("  ".join(new))
			f1.write("{}\n".format("  ".join(new)))
	f1.close()
	print("Found {} English words; Translated {} English words to Chinese".format(english, translated))
	print("{:.2f}% translated".format(float(translated)/ english* 100))


