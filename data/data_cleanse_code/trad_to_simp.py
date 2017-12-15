simp_to_trad = {}
with open("cedict.txt") as f:
	for line in f.readlines():
		trad, simp = line.rstrip().split()[:2]
		simp_to_trad[trad] = simp
f1 = open("simp_chinese.dev", "w")
with open("chinese.dev") as f:
	for line in f.readlines():
		sent_arr = line.rstrip().split()
		new = []
		for w in sent_arr:
			if w in simp_to_trad.keys():
				new.append(simp_to_trad[w])
			else:
				new.append(w)
		f1.write("{}\n".format("  ".join(new)))
f1.close()
