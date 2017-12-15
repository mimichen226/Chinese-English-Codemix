f1 = open("mixed.all", "w")
with open("convo_transcript_numbered.txt") as f:
	for line in f.readlines():
		line = line.lstrip()
		line = line.rstrip()
		print line
		if line:
			f1.write("{}\n".format(line.split("\t")[4]))
f1.close()

		
