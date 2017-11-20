import numpy as np
import os
import sys
from nltk.tree import Tree
from nltk.stem.wordnet import WordNetLemmatizer
from get_wh import *
import sent_info
lemmatizer = WordNetLemmatizer()


wh_tag = ['how', 'why', 'which', 'whose', 'who', 'where', 'when', 'what']
verb_tags = ['MD', 'VB', 'VBD', 'VBP', 'VBZ']
noun_tags = ['NN', 'NNP', 'NNS']
adj_tags = ['JJ', 'JJR', 'JJS']
adv_tags = ['RB']
number_tags = ['CD']


def q_type(tree):
	if (tree.label() == 'SQ'):
		return 'binary', tree
	elif (tree.label() == 'SBARQ' or tree.label() == 'SBAR'):
		q_list = tree.leaves()
		q_list[0] = q_list[0].lower()
		if (q_list[0] in wh_tag):
			if (q_list[0] == 'how'):
				if(q_list[1] == 'many'):
					q_word = 'how_many'
				else:
					q_word = 'how'
			else:
				q_word = q_list[0]
		else:
			q_word = q_list[0]
		return q_word, tree[1]
	elif (tree.label() == 'PP'):
		tree = tree[1]
#		print(tree)
#		return None, None
		return q_type(tree)
	else:
		return None, None

def bin_q_to_sent(qtree):
	head = qtree[0]
	while isinstance(head[0], Tree):
		head = head[0]
	if (head.label() != 'NNP'):
		head[0] = head[0].lower()

	if len(qtree) < 3:
		return tree_to_string(qtree)
	subject = qtree[1]
	obj = qtree[2]

	if (lemmatizer.lemmatize(head[0], 'v') == 'do'):
		if (is_word_tag(obj[0], verb_tags)):
			head_verb = obj[0]
			return ' '.join([tree_to_string(subject), tree_to_string(obj)])
		else:
			return ' '.join([tree_to_string(subject), head[0], tree_to_string(obj)])

	else:
		return ' '.join([tree_to_string(subject), head[0], tree_to_string(obj)])


def sent_to_bin_q(qtree):
	subject = qtree[0]
#  print(qtree[0])
	try:
		obj = qtree[1]
	except:
		return tree_to_string(qtree)

	if (subject.label() != 'NP' or obj.label() != 'VP'):
		return tree_to_string(qtree)
	core_verb = obj[0]
	if (not is_word_tag(core_verb.label(), verb_tags)):
		return tree_to_string(qtree)

	head = qtree[0]
	while isinstance(head[0], Tree):
		head = head[0]
	if (head.label() != 'NNP'):
		head[0] = head[0].lower()

	if (lemmatizer.lemmatize(core_verb[0], 'v') == 'be'):
		try:
			return ' '.join([core_verb[0], tree_to_string(subject)] + [tree_to_string(o) for o in obj[1:]])
		except:
			return ' '.join([core_verb[0], tree_to_string(subject)])

	else:
		if (core_verb.label() == 'VBD' or core_verb.label() == 'VBN'):
			return ' '.join(['did', tree_to_string(subject), lemmatizer.lemmatize(core_verb[0], 'v')] + [tree_to_string(o) for o in obj[1:]])
		elif (core_verb.label() == 'VBZ'):
			return ' '.join(['does', tree_to_string(subject), lemmatizer.lemmatize(core_verb[0], 'v')] + [tree_to_string(o) for o in obj[1:]])
		else:
			return ' '.join(['do', tree_to_string(subject), lemmatizer.lemmatize(core_verb[0], 'v')] + [tree_to_string(o) for o in obj[1:]])

def tree_to_string(tree): # convert tree to string
	if tree == None:
		return ""
	sent = ' '.join(tree.leaves())
	return sent

def is_word_tag(tlabel, tags):
	for tag in tags:
		if (tlabel.startswith(tag)):
			return True
	return False



