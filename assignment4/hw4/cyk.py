#!/usr/bin/env python

import sys, fileinput
import tree
from collections import defaultdict
from nltk.tokenize import TreebankWordTokenizer
import json

d = json.load(open("d.txt"))
rev_d = json.load(open("rd.txt"))
kTOKENIZER = TreebankWordTokenizer()

for line in fileinput.input():
	tokens = kTOKENIZER.tokenize(line)

	'''
	Play with tokens here
	'''
	n = len(tokens)
	#d  //Dictionary which contains production rule A -> BC and A -> literal and their log probability
	#rev_d  // This dictionary contains reverse production rules. BC -> A and literal -> A with probability

	dd = [[defaultdict(float) for _ in range(n)] for _ in range(n)]

	for index,token in enumerate(tokens):
		if token not in rev_d:
			tokens[index] = '<unk>'

	for index,token in enumerate(tokens):
		j = index
		temp_dict = rev_d[token]
		print token
		for k,v in temp_dict.iteritems():
			dd[j][j][k] = v
		for i in range(j-1,-1,-1):
			for k in range(i,j):
				left_b = dd[i][k].keys()
				right_b = dd[k+1][j].keys()
				# print left_b , i,j,k
				# print right_b, i, j, k
				for B in left_b:
					for C in right_b:
						r_side = B + ' '+ C
						if r_side in rev_d:
							for key,value in rev_d[r_side].iteritems():
								if key not in dd[i][j]:
									dd[i][j][key] = value + dd[i][k][B] + dd[k+1][j][C]
								elif dd[i][j][key] < (value + dd[i][k][B] + dd[k+1][j][C]):
									dd[i][j][key] = value + dd[i][k][B] + dd[k+1][j][C]

	# for i in range(n+1):
	# 	for j in range(n+1):
	print dd[0][n-1]