#!/usr/bin/env python

import sys, fileinput
import tree
from collections import defaultdict
from nltk.tokenize import TreebankWordTokenizer
import json
from tree import Node
from tree import Tree
import timeit
import numpy as np
import matplotlib.pyplot as plt
import math

def func(sen_size,time):
	d = json.load(open("d.text"))
	rev_d = json.load(open("rd.text"))
	kTOKENIZER = TreebankWordTokenizer()

	for line in fileinput.input():
		tokens = kTOKENIZER.tokenize(line)


		n = len(tokens)
		#d  //Dictionary which contains production rule A -> BC and A -> literal and their log probability
		#rev_d  // This dictionary contains reverse production rules. BC -> A and literal -> A with probability

		dd = [[defaultdict(float) for _ in range(n)] for _ in range(n)]
		back = [[defaultdict(float) for _ in range(n)] for _ in range(n)]
		for index,token in enumerate(tokens):
			if token not in rev_d:
				tokens[index] = '<unk>'

		start_time = timeit.default_timer()         
		for index,token in enumerate(tokens):
			j = index
			temp_dict = rev_d[token]
			for k,v in temp_dict.iteritems():
				dd[j][j][k] = v
				back[j][j][k] = token
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
										back[i][j][key] = str(k) + ' '+ B + ' ' + C
									elif dd[i][j][key] < (value + dd[i][k][B] + dd[k+1][j][C]):
										dd[i][j][key] = value + dd[i][k][B] + dd[k+1][j][C]
										back[i][j][key] = str(k) + ' '+ B + ' ' + C 

		# for i in range(n+1):
		# 	for j in range(n+1):
		elapsed =  timeit.default_timer() - start_time
		time.append(elapsed*1000000)
		sen_size.append(n)
		maxi = -100000000
		top_word = ''
		for k,v in dd[0][n-1].iteritems():
			if v > maxi:
				top_word = k
		#print back[0][n-1]
		if len(top_word) > 0:
			rr = Node(top_word,[])
			printpath(back,top_word,0,n-1,rr)
			t = Tree(rr)
			t.restore_unit()
			t.unbinarize()
			#out_file.write(t.__str__()+'\n')
			print t.__str__()
		else:
			#out_file.write('\n')
			print

def printpath(d,A,i,j,p):
	#print d
	st = d[i][j][A].split(' ')
	if len(st)==3:
		k = int(st[0])
		B = st[1]
		C = st[2]
		#print A, ' ->', B, C
		left = Node(B,[])
		right = Node(C,[])
		p.insert_child(0,left)
		p.insert_child(1,right)
		printpath(d,B,i,k,left)
		printpath(d,C,k+1,j,right)
	else:
		#print A , ' ->' , st[0]
		terminal = Node(st[0],[])
		p.insert_child(0,terminal)

def plot(sen_size,time):
	x = np.log(np.array(sen_size))
	y = np.log(np.array(time))
	plt.plot(x,y,'ro')
	plt.axis([0,5,0,10])
	plt.show()

sen_size = []
time = []
func(sen_size,time)
plot(sen_size,time)
