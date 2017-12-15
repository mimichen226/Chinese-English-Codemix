import re
import os

f1 = open("english.train", "w")
for filename in os.listdir("./eng"):
	if filename.endswith(".tkn"):
		with open("./eng/{}".format(filename)) as f:
			for line in f.readlines():
				f1.write("{}\n".format(line.rstrip()))
f1.close()

