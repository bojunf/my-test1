import numpy as np
import os
import sys
from nltk.stem.wordnet import WordNetLemmatizer
from nltk import word_tokenize

VB_not_normal = ['is', 'are', 'am', 'was', 'were']
VB_not_normal_change =['do', 'does', 'did'] # not normal verb list
nega = ["not", "n't"] # negative attitude
punc = ['.', '?', '!'] # stop of the sentence
V_tag = ['VB', 'VBD', 'VBZ', 'VBP', 'VBN', 'VBG']


def gen_bin_normp(tree): # generate binary questions based on easyp from pattern
	sent = []
	ans = 'positive' # default answer to question is positive
	for i in range(len(tree)): # loop over every tree
		flag_move = False
		if (tree[i].label() == 'VP'): # VP
			for j in range(len(tree[i])): # loop over every component in VP
#				print(len(tree[i][j]))
				if (len(tree[i][j]) == 1 and tree[i][j].label() in V_tag): # the verb in VP
#					print(tree[i][j][0])
					jref = j
					if (str(tree[i][j][0]) in VB_not_normal or str(tree[i][j][0]) in VB_not_normal_change): # move unnormal verb the the front of sentence
#						print(str(tree[i][j][0]))
						flag_move = True
						w_tmp = tree_to_string(tree[i][j])
						w_tmp = list(w_tmp)
						w_tmp[0] = w_tmp[0].upper() # the first letter should be upper case
						w_tmp = ''.join(w_tmp)
						sent.insert(0, w_tmp)
						continue
					else: # normal verb, add does, did or do the the front of question
						if (tree[i][j].label() == 'VBZ'): 
							sent.insert(0, 'Does')
							word = tree_to_string(tree[i][j])
							word = WordNetLemmatizer().lemmatize(word,'v')
#							print(word)
							sent.append(word)
							continue
						elif (tree[i][j].label() in ['VBD', 'VBN']):
							sent.insert(0, 'Did')
							word = tree_to_string(tree[i][j])
							word = WordNetLemmatizer().lemmatize(word,'v')
#							print(word)
							sent.append(word)
							continue
						else:
							sent.insert(0, 'Do')
				if (len(tree[i][j]) == 1 and tree[i][j].label() == 'MD'):
					w_tmp = tree_to_string(tree[i][j])
					w_tmp = list(w_tmp)
					w_tmp[0] = w_tmp[0].upper() # the first letter should be upper case
					w_tmp = ''.join(w_tmp)
					sent.insert(0, w_tmp)
					continue
				if (flag_move and j == (jref+1)): # if there is a not, the answer to this q should be negative
					if (str(tree[i][j][0]) in nega):
						ans = 'negative'
						flag_move = False
						continue
					else: # if no "not", it's part of question, add to question
						sent.append(tree_to_string(tree[i][j]))
#						ans = 'positive'
						flag_move = False
						continue
				sent.append(tree_to_string(tree[i][j])) # add component back to question
			continue
		sent.append(tree_to_string(tree[i]))
	if(sent[-1] in punc): # add ? to the end
		sent[-1] = '?' 
	sent[1] = sent[1].lower()
	sent = ' '.join(sent).replace('-LRB-', '(').replace('-RRB-', ')')
	return sent, ans


def who_q(tree, tags):
	wq = []
	np = tree[0]
	vp = tree[1]
	tmpnp = np
	while(len(tmpnp[0]) > 1):
		tmpnp = tmpnp[0]
	np_len = len(tmpnp)
#	for i in range(np_len):
#		print(tmpnp[i])
	if (np[0].label() == 'PRP'):
#		np[0] = 'Who '
		ques = ('Who ' + tree_to_string(vp)).replace('-LRB-', '(').replace('-RRB-', ')').replace('-lrb-', '(').replace('-rrb-', ')')
#		ques += ' ?'
		wq.append(ques)
	elif ('PERSON' in t for t in tmpnp[:np_len]):
#		np[0] = 'Who '
		ques = ('Who' + tree_to_string(vp)).replace('-LRB-', '(').replace('-RRB-', ')').replace('-lrb-', '(').replace('-rrb-', ')')
#		ques += ' ?'
		wq.append(ques)

	np_sent = tree_to_string(np)
	np_sent = word_tokenize(np_sent)
	vp_tag = tags[len(np_sent):]

	if (hasTag(vp_tag, 'PERSON')):
		tmp_q = []
		flag_person = False
		for t in vp_tag:
	 		if (not flag_person and t[1] == 'PERSON'):
	 			person = t[0]
	 			prevp = t[1]
	 			flag_person = True
	 		elif (flag_person and t[1] == 'PERSON' and prevp == 'PERSON'):
	 			person += t[0]
	 			prevp = t[1]
	 		else:
	 			flag_person = False
	 			tmp_q.append(t[0])

		#npl = np.leaves()
		ques = tmp_q + np.leaves()

		ques.insert(0, 'Who')
		wq.append(" ".join(ques))
	return wq

def when_q(tree, tags):
	wq = []
	np = tree[0]
	vp = tree[1]
	np_sent = tree_to_string(np)
	np_sent = word_tokenize(np_sent)
	vp_tag = tags[len(np_sent):]
	tmp_q = []
	if (hasTag(vp_tag, 'TIME')):
		flag_time = False
		for t in vp_tag:
			if (not flag_time and t[1] == 'TIME'):
				time = t[0]
				prevt = t[1]
				flag_time = True
				if (decide_pp.lower() in ['in', 'at', 'on']):
					del tmp_q[-1]
			elif (flag_time and t[1] == 'TIME' and prevt == 'Time'):
				time += t[0]
				prevt = t[1]
			else:
				flag_time = False
				tmp_q.append(t[0])
				decide_pp = t[0]

		ques = 'When ' + " ".join(np_sent) + " ".join(tmp_q)
		wq.append(ques)
#	if (hasTag(tags, 'PERSON') or np[0].label() == 'PRP'):
#		print(tags)
	return wq

def change_verb(tree):
	cond = 'normal'
	tmp = tree[1]
	while(len(tmp) > 1):
		print(tmp)
		print(len(tmp))
		for t in tmp:
			if (t.label() == 'VP' or t.label() in V_tag):
				tmp = t
				print(tmp)
				break
#		tmp = tree[0]
	print(tmp.label())
	print(tmp)

	if (tmp.label() in VB_not_normal or tmp.label() in VB_not_normal_change):
		cond = 'move'
		tmp = ''
	elif (tmp.label() in ['VBN', 'VBD']):
		tmp = WordNetLemmatizer().lemmatize(tmp,'v')
		cond = 'past'
	elif (tmp.label() == 'VBZ'):
		word = tree_to_string(tmp)
		tmp = WordNetLemmatizer().lemmatize(word,'v')
		cond = 'third'
	return cond


def hasTag(tags, tag):
	for t in tags:
		if t[1] == tag:
			return True
	return False


def tree_to_string(tree): # convert tree to string
	sent = ' '.join(tree.leaves())
	return sent


