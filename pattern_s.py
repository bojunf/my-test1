import numpy as np
import os
import sys
import gen_q
from nltk.tree import Tree
from pattern_q import *
import copy

easyp = ['NP', 'VP']

def find_easyp(parse_trees): # match sentence with easyp
	match = []
	for tree in parse_trees:
		if (len(tree) <= 1): # leaf
			continue
#		print(tree[0].label(), tree[1].label)
		tmp_p = []
		for i in range(2): # tree structure starts with NP, VP
#		for i in range(len(tree)):
			tmp_p.append(str(tree[i].label())) 

		if (tmp_p == easyp): # add match
			match.append(tree)
	return match

def find_normp(parse_trees):
	match = []
	for tree in parse_trees:
		if (len(tree) <= 1): # leaf
			continue
#		print(tree[0].label(), tree[1].label)
		tmp_p = []
		for i in range(len(tree)): # tree structure starts with NP, VP
#		for i in range(len(tree)):
			tmp_p.append(str(tree[i].label())) 

		if (easyp[0] in tmp_p and easyp[1] in tmp_p): # add match
			match.append(tree)
	return match

def extract_stem(parse_trees):
	transform = []
	for tree in parse_trees:
		if (len(tree) <= 1):
			continue
		tmp_p = []
		flag_np = False
		for i in range(len(tree)):
			if (str(tree[i].label()) == 'NP' and not flag_np):
				tmp_p.append(gen_q.tree_to_string(tree[i]))
				flag_np = True
			if (str(tree[i].label()) == 'VP' and flag_np):
				tmp_p.append(gen_q.tree_to_string(tree[i]))
				transform.append(" ".join(tmp_p).replace('-LRB-', '(').replace('-RRB-', ')').replace('-lrb-', '(').replace('-rrb-', ')'))
				continue
	return transform



