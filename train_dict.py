import math
import json
import pickle 

# Assign every translation in the English to Chinese dictionary an initial weight of 10
ecdict = {}
with open("ecdict.json") as f:
	ecdict_init = json.load(f)

ecdict_init.pop("") 	# don't need translations from NULL to a Chinese word

for key, values in ecdict_init.items():
	ecdict[key] = {}
	for v in values:
		ecdict[key][v] = 10

# Train the dictionary on parallel English and Chinese texts
chin = []
eng = []
align = []
with open("./data/chinese.train") as f_chin:
	for line in f_chin.readlines():
		chin.append(line.rstrip())
with open("./data/english.train") as f_eng: 
	for line in f_eng.readlines():
		eng.append(line.rstrip())

with open("./data/align.train") as f_align:
	for line in f_align.readlines():
		align.append(line.rstrip())

word_count = 0
for sent_index in range(len(align)):
	chin_sent = chin[sent_index].split()
	eng_sent = eng[sent_index].split()
	alignments = align[sent_index].split()
	if alignments[0] == "rejected":
		continue
	for a in alignments:
		# Align the indicies
		c, e = a.split("-")
		if not e:
			continue
		e_list = [] 
		for blah in e.split(","):
			try: 
				if int(blah) != 1:
					e_list.append(int(blah))
			except:
				e_list.append(None)
		c_list = []
		for blah in c.split(","):
			try:
				c_list.append(int(blah))
			except:
				c_list.append(None)
		# Make the English/ Chinese word from indices
		eng_word_list = []
		chin_word_list = []
		if c_list[0] == None:
			for i in e_list: 
				eng_word_list.append(eng_sent[i - 1])
			#print("NULL <--> {}".format(" ".join(eng_word)))
			chin_word_list.append("NULL")
		else:
			for i in c_list:
				chin_word_list.append(chin_sent[i - 1])
			for i in e_list:
				eng_word_list.append(eng_sent[i - 1])
			#print("{} <--> {}".format("".join(chin_word), " ".join(eng_word)))
		eng_word = " ".join(eng_word_list)
		chin_word = "".join(chin_word_list)
		if eng_word in ecdict.keys():
			ecdict[eng_word][chin_word] = ecdict[eng_word].get(chin_word, 0) + 1
		else:
			ecdict[eng_word] = {chin_word: 1}
		word_count += 1
pickle.dump(ecdict, open("ecdict.pickle", "wb"))
# Normalize the dictionary
prob_ecdict = {}
for key,value in ecdict.items():
	prob_ecdict[key] = {}
	total = 0
	for v, count in value.items():
		total += count
	for v, count in value.items():
		prob_ecdict[key][v] = math.log(float(count) / total)

pickle.dump(prob_ecdict, open("prob_ecdict.pickle", "wb"))
print("Total word pairs in training data: {}".format(word_count))
