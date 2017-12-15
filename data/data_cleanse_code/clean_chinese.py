f1 = open("chinese.all","w")

with open("convo_transcript_1000.txt") as f:
	for line in f.readlines():
		line = line.lstrip()
		try: 
			int(line.split("   ")[0])
		except:
			f1.write(line)
f1.close()

