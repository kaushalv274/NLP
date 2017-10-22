#!/usr/bin/env python
import distsim
from collections import defaultdict
word_to_vec_dict = distsim.load_word2vec("nyt_word2vec.4k")
start = 0
cnt = 0
scores = defaultdict(float)
with open('word-test.v3.txt') as f:
	for line in f:
		if line[0] == ':' and start == 1:
			#start of new block
			for key, val in scores.items():
				print key, val/cnt
			scores.clear()
			cnt = 0
		words = line.strip().split(' ')
		if len(words) ==4:
			start = 1
			cnt += 1
			dict1 = word_to_vec_dict[words[0]]
			dict2 = word_to_vec_dict[words[1]]
			dict3 = word_to_vec_dict[words[3]]
			exclude = set([words[0],words[1],words[3]])
			ret = distsim.show_nearest(word_to_vec_dict,
                           dict1-dict2+dict3,
                           exclude,
                           distsim.cossim_dense)
			names  = [item[0] for item in ret]
			if words[2] in names:
				ind = names.index(words[2])
			else:
				ind = 20
			if ind == 0:
				scores[10] += 1
				scores[1] +=1
				scores[5] +=1
			elif ind <= 4:
				scores[10] += 1
				scores[5] += 1
			elif ind <= 9:
				scores[10] += 1
	for key, val in scores.items():
		print key, val/cnt
