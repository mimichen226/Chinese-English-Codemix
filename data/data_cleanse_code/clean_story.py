#f1 = open("little_horse.all", "w")
with open("little_horse_story.chinese") as f:
	for line in f.readlines():
		line = line.lstrip()
		line = line.rstrip()
		a = "".join(line.split("<wbr>"))
		b = "".join(a.split("<x-mspot style=\"\">"))
		c = "".join(b.split("<x-mspot>"))
		d = "  ".join(c.split("</x-mspot>"))
		print d

#		if line:
			#f1.write("{}\n".format(line.split("\t")[4]))
#f1.close()

		
