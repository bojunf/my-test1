import numpy as np
import os
import sys



def Get_tree(itert): # remove the start symbol
	for t in itert:
		x = t[0]

	return x


def Get_nNoun(tree):
	nn = 0
#	tree = Get_tree(tree_iter)
	if (len(tree) > 1): # not a leaf
		for i in range(len(tree)): # loop over every child
			nn += Get_nNoun(tree[i]) # recursively count noun of every subtree
		return nn
	else:
		if ('NN' in str(tree)): # is a leaf
#			print(tree.label())
			return 1
		else:
			return 0
#		return
#			print(tree[i])
#			if ('NN' in tree[i]):
#				print(tree[i])
#			nn += Get_nNoun(tree[i])
#	else:
#		if ('NN' in tree):
#			return 1
#		else:
#			return 0
	#return nn
	