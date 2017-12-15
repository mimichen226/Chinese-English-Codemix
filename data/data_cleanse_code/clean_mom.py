f1 = open("cleaned_chinese.dev", "w")
with open("chinese.dev") as f:
	for line in f.readlines():
		line = line.rstrip().lstrip()
		if line:
			try:
				int(line.split()[0])
			except:
				f1.write("{}\n".format(line))
f1.close()
