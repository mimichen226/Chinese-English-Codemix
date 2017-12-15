import re
import os

f1 = open("align.processed", "w")
for filename in os.listdir("./wa_align"):
	if filename.endswith(".wa"):
		with open("./wa_align/{}".format(filename)) as f:
			for line in f.readlines():
				f1.write("{}\n".format(re.sub("[\(\[].*?[\)\]]", "", line.rstrip())))
f1.close()
