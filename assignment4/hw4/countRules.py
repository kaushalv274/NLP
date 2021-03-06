#!/usr/bin/env python

import sys, fileinput
import tree
from collections import defaultdict
import math
import json

d = defaultdict(lambda : defaultdict(float))
rev_d = defaultdict(lambda : defaultdict(float))
for line in fileinput.input():
	t = tree.Tree.from_str(line)
	k =  list(t.bottomup())

	for ele in k:
		if len(ele.children)>0:
			stt = ''
			for k in ele.children:
				if len(stt)>0:
					stt = stt + ' ' + k.label
				else:
					stt = stt + k.label
			d[ele.label][stt] += 1

rules = 0
max_rule = 0
max_rule_left = ''
max_rule_right = ''
for key,value in d.iteritems():
	rules += len(value.keys())
	cnt = 0
	for k,v in value.iteritems():
		cnt += v
		if max_rule < v:
			max_rule = v
			max_rule_right = k
			max_rule_left = key
	for k in value:
		value[k] = math.log10(value[k]/cnt)
		rev_d[k][key] = value[k]
print rules
print max_rule
print max_rule_left
print max_rule_right
json.dump(d,open("d.text",'w'))
json.dump(rev_d,open("rd.text",'w'))