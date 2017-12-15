import pickle
import requests
import json
from collections import deque
import argparse


ALPHA = {'a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z',\
		'A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z'}

def check_if_english(word):
	return set(list(word)).issubset(ALPHA)

def wikiCheck(eng_arr):
	eng_arr = " ".join(eng_arr).title().split() # titlize the words
	r = requests.get("https://en.wikipedia.org/w/api.php?action=query&format=json&prop=langlinks&titles={}&lllang=zh".format("%20".join(eng_arr)))
	resp = json.loads(r.content.decode('utf-8'))
	for pg_id in resp['query']['pages']:
		try:
			print(resp['query']['pages'][pg_id]['langlinks'])
			return resp['query']['pages'][pg_id]['langlinks'][0]["*"]
		except: 
			return -1

def groupingCheck(group, ecdict):
	# Check if the grouping of 2 is in our dictionary 
	chinese_translation = None
	chinese_translation_count = 0
	# Not titlized in our EC dict
	if group in ecdict.keys():
		poss_tran = sorted(ecdict[group].items(), key=lambda item: (item[1], item[0]))
		top_tran = poss_tran[len(poss_tran) - 1][0]
		if ecdict[group][top_tran] > chinese_translation_count:
			chinese_translation = top_tran
			chinese_translation_count = ecdict[group][top_tran]
	# Titlized in our EC dict
	group = group.title()
	if group in ecdict.keys():
		poss_tran = sorted(ecdict[group].items(), key=lambda item: (item[1], item[0]))
		top_tran = poss_tran[len(poss_tran) - 1][0]
		if ecdict[group][top_tran] > chinese_translation_count:
			chinese_translation = top_tran
			chinese_translation_count = ecdict[group][top_tran]
	# Titleized in Wikipedia 
	else:
		wiki = wikiCheck(group.split())
		if wiki != -1:
			ecdict[group] = {wiki: 1}
			if ecdict[group][wiki] > chinese_translation_count:
				chinese_translation = wiki
				chinese_translation_count = 1
	return chinese_translation_count, chinese_translation, ecdict 

def singleWordCheck(sub_word, ecdict):
	# Check for single word
	Sub_word = sub_word.title()
	chinese_translation = None
	chinese_translation_count = 0
	# Known Eng word -- pick best probability
	if sub_word in ecdict.keys():
		poss_tran = sorted(ecdict[sub_word].items(), key=lambda item: (item[1], item[0]))
		top_tran = poss_tran[len(poss_tran) - 1][0]
		if ecdict[sub_word][top_tran] > chinese_translation_count:
			chinese_translation = top_tran
			chinese_translation_count = ecdict[sub_word][top_tran]
	elif Sub_word in ecdict.keys():
		poss_tran = sorted(ecdict[Sub_word].items(), key=lambda item: (item[1], item[0]))
		top_tran = poss_tran[len(poss_tran) - 1][0]
		if ecdict[Sub_word][top_tran] > chinese_translation_count:
			chinese_translation = top_tran
			chinese_translation_count = ecdict[Sub_word][top_tran]
	# Unknown Eng word -- try translating the sub group with Wikipedia
	else:
		wiki = wikiCheck(Sub_word)
		if wiki != -1: 
			ecdict[Sub_word] = {wiki: 1}
			if ecdict[Sub_word][wiki] > chinese_translation_count:
				chinese_translation = wiki
				chinese_translation_count = ecdict[Sub_word][wiki]
	return chinese_translation_count, chinese_translation, ecdict

if __name__ == "__main__":
	argparser = argparse.ArgumentParser()
	argparser.add_argument('inp', metavar='input', help='input file')
	argparser.add_argument('output', metavar='output', help='output file')
	args = argparser.parse_args()

	ecdict = pickle.load( open("ecdict.pickle", "rb"))
	f1 = open(args.output, "w")

	translated = 0
	english = 0

	with open(args.inp) as f:
		sent_index = 0
		for line in f.readlines():
			sent_arr = line.rstrip().split()
			new = []
			eng_sub = deque()
			for word in sent_arr:
				# English word
				if check_if_english(word):
					english += 1
					eng_sub.append(word)
					length_of_eng = 0

					# Groupings of 2
					if len(eng_sub) == 1:
						continue
							
					group = " ".join(list(eng_sub))
					group_count, group_trans, ecdict = groupingCheck(group, ecdict)
					sub_word = eng_sub.popleft()
					single_count, single_trans, ecdict = singleWordCheck(sub_word, ecdict)

					# No possible translation
					if not single_count and not group_count: 
						new.append(sub_word)
					# Grouping translation wins 
					elif group_count >= single_count:
						new.append(group_trans)
						translated += 2  # because grouping of size 2
						eng_sub.popleft()
					# Single word translation wins
					else: 
						if single_trans != "NULL":
							new.append(single_trans)
						translated += 1
				
				# Chinese word
				else:
					# Clear out the eng_sub
					while eng_sub:
						if len(list(eng_sub)) > 1:
							group = " ".join(list(eng_sub))
							group_count, group_trans, ecdict = groupingCheck(group, ecdict)
							sub_word = eng_sub.popleft()
							single_count, single_trans, ecdict = singleWordCheck(sub_word, ecdict)

							# No possible translation
							if not single_count and not group_count: 
								new.append(sub_word)
							# Grouping translation wins 
							elif group_count >= single_count:
								new.append(group_trans)
								translated += 2  # because grouping of size 2
								eng_sub.popleft()
							# Single word translation wins
							else: 
								if single_trans != "NULL":
									new.append(single_trans)
								translated += 1

						# Just one word in eng_sub
						else:
							sub_word = eng_sub.popleft()
							single_count, single_trans, ecdict = singleWordCheck(sub_word, ecdict)
							if single_count: 
								new.append(single_trans)
								translated += 1
							else:
								new.append(sub_word)
					# Append the Chinese word
					new.append(word) 

			# At the end of a sentence -- clear out the eng_sub
			while eng_sub:
				if len(list(eng_sub)) > 1:
					group = " ".join(list(eng_sub))
					group_count, group_trans, ecdict = groupingCheck(group, ecdict)
					sub_word = eng_sub.popleft()
					single_count, single_trans, ecdict = singleWordCheck(sub_word, ecdict)


					# No possible translation
					if not single_count and not group_count: 
						new.append(sub_word)
					# Grouping translation wins 
					elif group_count >= single_count:
						new.append(group_trans)
						translated += 2  # because grouping of size 2
						eng_sub.popleft()
					# Single word translation wins
					else: 
						if single_trans != "NULL":
							new.append(single_trans)
						translated += 1

				# Just one word in eng_sub
				else:
					sub_word = eng_sub.popleft()
					single_count, single_trans, ecdict = singleWordCheck(sub_word, ecdict)
					if single_count: 
						new.append(single_trans)
						translated += 1
					else:
						new.append(sub_word)

			print("{}\t{}".format(sent_index, "  ".join(new)))
			f1.write("{}\n".format("  ".join(new)))
			sent_index += 1
	f1.close()
	print("Found {} English words; Translated {} English words to Chinese".format(english, translated))
	print("{:.2f}% translated".format(float(translated)/ english* 100))

pickle.dump(ecdict, open("updated_ecdict.pickle", "wb"))
