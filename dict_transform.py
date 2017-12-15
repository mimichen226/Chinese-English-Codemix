import json

ec_dict = {}
with open("cedict.txt") as f:
	for line in f.readlines():
		line = line.rstrip()
		arry = line.split("/")
		eng_arry = arry[1:]
		simp = arry[0].split(" ")[1]
		for eng in eng_arry:
			chinese_list = ec_dict.get(eng, [])
			chinese_list.append(simp)
			ec_dict[eng] = chinese_list
with open('ecdict.json', 'w') as outfile:
	json.dump(ec_dict, outfile)
