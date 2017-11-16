import os
import sys
import numpy as np
from nltk.tree import Tree
import copy
import stanford_parser
import stanford_ner
from nltk import word_tokenize, pos_tag
import sent_info
import pattern_q


parser = stanford_parser.parser()
tagger = stanford_ner.tagger()

wh_tag = ['how_many', 'how', 'why', 'which', 'whose', 'who_whom', 'where', 'when', 'what']


def has_netags(tree, target_index, netags, target_tags):


#	for i in range(len(netags)):
#		if (netags[i][1] in target_tags):
#			return True
#	return False
#	print(tree[:target_index])
#	try:
	try:
		tree_tmp = tree[:target_index][0]
		ne_start = len(tree_tmp.leaves())
	except:
		ne_start = 0
 #		tree_tmp = Tree(())
 	
	try:
		tree_part = tree[target_index]
		ne_len = len(tree_part.leaves())
	except:
		return False
	for i in range(ne_start, ne_start + ne_len):
		if (netags[i][1] in target_tags):
			return True
	return False

def has_deeper_netags(tree, target_index_list, netags, target_tags):
	tree_tmp = tree
	ne_start = 0
	for index in target_index_list:
		ne_start += nword(tree_tmp[:index])
		tree_tmp = tree_tmp[index]

	for i in range(ne_start, ne_start + nword(tree_tmp)):
		if (netags[i][1] in target_tags):
			return True
	return False


def has_pos_tags(tree, target_index_list, target_tags):
	tree_tmp = tree
	for index in target_index_list:
		tree_tmp = tree_tmp[index]
	for i in range(nword(tree_tmp)):
		try:
			if (tree_tmp[i].label() in target_tags):
				return tree_tmp[i]
		except:
			return False
	return False


def nword(t):
  if (len(t) == 0):
    return 0
  tree = t[0]
  try:
  	return len(tree.leaves())
  except:
  	return 0



#questions and answers based on NER tags

def find_who_whom(tree, netags, answer_or_ask):
	np = tree[0]
	vp = tree[1]
#	print(len(vp))
	out = []
	if (has_netags(tree, 0, netags, ['PERSON'])):
		tree_tmp = copy.deepcopy(tree)
		del tree_tmp[0]
		if (answer_or_ask):
			out.append((tree[0], tree_tmp))
		else:
			out.append(('Who', tree_tmp))
	iperson = 1
	try:
#		print(vp[iperson])
		vp[iperson]

	except:
		return out
	if (vp[iperson].label() == 'NP'):
		if (has_deeper_netags(tree, [1, iperson], netags, ['PERSON'])):
			tree_tmp = copy.deepcopy(tree)
			if (answer_or_ask):
				head_tmp = vp[iperson]
			else:
				head_tmp = 'Who'
			del tree_tmp[1, iperson]
			out.append((head_tmp, tree_tmp))
	
#		print(vp[iperson])
	while(True):
		try:
			vp[iperson]
#				print(vp[iperson])
		except:
			return out
		if (vp[iperson].label() == 'PP'):
			PP = vp[iperson]
#			print(PP)
			preposition = PP[0]
#			print(preposition)
			obj = PP[1]
#			print(obj)
			if (preposition.label() in ['TO', 'IN'] and has_deeper_netags(tree, [1, iperson, 1], netags, ['PERSON'])):
				tree_tmp = copy.deepcopy(tree)
				if (answer_or_ask):
					head_tmp = vp[1, iperson]
#					print(head_tmp)
				else:
					head_tmp = preposition + ' whom'
				del tree_tmp[1, iperson]
				out.append((head_tmp, tree_tmp))
			break
		iperson += 1
	return out


def find_where(tree, netags, answer_or_ask):
	np = tree[0]
	vp = tree[1]
	out = []
	if (has_netags(tree, 0, netags, ['LOCATION'])):
		tree_tmp = copy.deepcopy(tree)
		del tree_tmp[0]
		if (answer_or_ask):
			out.append((tree[0], tree_tmp))
		else:
			out.append(('Where', tree_tmp))
	ilocation = 1
	try:
#		print(vp[iperson])
		vp[ilocation]

	except:
		return out
	if (vp[ilocation].label() == 'NP'):
		if (has_deeper_netags(tree, [1, ilocation], netags, ['LOCATION'])):
			tree_tmp = copy.deepcopy(tree)
			if (answer_or_ask):
				head_tmp = vp[ilocation]
			else:
				head_tmp = 'Where'
			del tree_tmp[1, ilocation]
			out.append((head_tmp, tree_tmp))
	
#		print(vp[iperson])
	while(True):
		try:
			vp[ilocation]
#				print(vp[iperson])
		except:
			return out
		if (vp[ilocation].label() == 'PP'):
			PP = vp[ilocation]
#			print(PP)
			preposition = PP[0]
#			print(preposition)
			obj = PP[1]
#			print(obj)
			if (preposition.label() in ['TO', 'IN'] and has_deeper_netags(tree, [1, ilocation, 1], netags, ['LOCATION'])):
				tree_tmp = copy.deepcopy(tree)
				if (answer_or_ask):
					head_tmp = vp[ilocation, 1]
#					print(head_tmp)
				else:
					head_tmp = 'where'
				del tree_tmp[1, ilocation, 1]
				out.append((head_tmp, tree_tmp))
			break
		ilocation += 1
	return out

def find_when(tree, netags, answer_or_ask):
	np = tree[0]
	vp = tree[1]
	out = []
	if (has_netags(tree, 0, netags, ['TIME', 'DATE'])):
		tree_tmp = copy.deepcopy(tree)
		del tree_tmp[0]
		if (answer_or_ask):
			out.append((tree[0], tree_tmp))
		else:
			out.append(('When', tree_tmp))
	itime = 1
	try:
#		print(vp[iperson])
		vp[itime]

	except:
		return out
	if (vp[itime].label() == 'NP'):
		if (has_deeper_netags(tree, [1, itime], netags, ['TIME', 'DATE'])):
			tree_tmp = copy.deepcopy(tree)
			if (answer_or_ask):
				head_tmp = vp[itime]
			else:
				head_tmp = 'When'
			del tree_tmp[1, itime]
			out.append((head_tmp, tree_tmp))
	
#		print(vp[iperson])
	while(True):
		try:
			vp[itime]
#				print(vp[iperson])
		except:
			return out
		if (vp[itime].label() == 'PP'):
			PP = vp[itime]
#			print(PP)
			preposition = PP[0]
#			print(preposition)
			obj = PP[1]
#			print(obj)
			if (preposition.label() in ['TO', 'IN'] and has_deeper_netags(tree, [1, itime, 1], netags, ['DATE', 'TIME'])):
				tree_tmp = copy.deepcopy(tree)
				if (answer_or_ask):
					head_tmp = vp[itime, 1]
#					print(head_tmp)
				else:
					head_tmp = 'when'
				del tree_tmp[1, itime, 1]
				out.append((head_tmp, tree_tmp))
			break
		itime += 1
	return out



# questions and answers does not have NER tags

def find_how_many(tree, answer_or_ask):
	np = tree[0]
	vp = tree[1]
	out = []
	number = has_pos_tags(tree, [0], ['CD'])
	if (number):
		tree_tmp = copy.deepcopy(tree)
		del tree_tmp[0]
		noun_tmp = tree[0, -1]
		if (answer_or_ask):
			head_tmp = number[0] + ' ' + noun_tmp[0]
			out.append((head_tmp, tree_tmp))
		else:
			head_tmp = 'How many ' + noun_tmp[0]
			out.append((head_tmp, tree_tmp))
	iitem = 1

	while(True):
		try:
			vp[iitem]
#				print(vp[iperson])
		except:
			return out
		number = has_pos_tags(tree, [1, iitem], ['CD'])
		if (number):
			tree_tmp = copy.deepcopy(tree)
			del tree_tmp[1, iitem]
			noun_tmp = tree[1, iitem, -1]
			if (answer_or_ask):
#				print(number, noun_tmp)
				head_tmp = number[0] + ' ' + noun_tmp[0]
				out.append((head_tmp, tree_tmp))
			else:
				head_tmp = 'How many ' + noun_tmp[0] 
			out.append((head_tmp, tree_tmp))
			break
		iitem += 1
	return out

def find_why(tree, answer_or_ask):
	out = []
	vp = tree[1]
	iitem = 1
	while(True):
		try:
			vp[iitem]
#				print(vp[iperson])
		except:
			return out
		if (vp[iitem].label() == 'SBAR'):
			if (vp[iitem, 0].label() == 'IN' and vp[iitem, 0, 0].lower() == 'because'):
				tree_tmp = copy.deepcopy(tree)
				del tree_tmp[1, iitem]
				reason_tmp = tree[1, iitem]
				if (answer_or_ask):
#				print(number, noun_tmp)
					head_tmp = reason_tmp
					out.append((head_tmp, tree_tmp))
				else:
					head_tmp = 'Why '
				out.append((head_tmp, tree_tmp))
				break
		iitem += 1
	return out

def find_how(tree, answer_or_ask):
	out = []
	vp = tree[1]
	iitem = 1
	while(True):
		try:
			vp[iitem]
#				print(vp[iperson])
		except:
			return out
		if (vp[iitem].label() == 'ADVP'):
			if (vp[iitem, 0].label() == 'RB'):
				tree_tmp = copy.deepcopy(tree)
				del tree_tmp[1, iitem]
				how_tmp = tree[1, iitem]
				if (answer_or_ask):
#				print(number, noun_tmp)
					head_tmp = how_tmp
					out.append((head_tmp, tree_tmp))
				else:
					head_tmp = 'How '
				out.append((head_tmp, tree_tmp))
				break
		iitem += 1
	return out

def find_which(tree, answer_or_ask):
	out = []
	np = tree[0]
	vp = tree[1]
	if (np[0].label() == 'DT' and np[-1].label().startswith('NN')):
		tree_tmp = copy.deepcopy(tree)
		del tree_tmp[0]
		noun_tmp = tree[0, -1][0]
		if (answer_or_ask):
			head_tmp = np
			out.append((head_tmp, tree_tmp))
		else:
			head_tmp = 'Which ' + noun_tmp[0]
			out.append((head_tmp, tree_tmp))
	iitem = 1

	while(True):
		try:
			vp[iitem]
#				print(vp[iperson])
		except:
			return out
		if (vp[iitem].label() == 'NP' and vp[iitem, 0].label() == 'DT' and vp[iitem, -1].label().startswith('NN')):
			tree_tmp = copy.deepcopy(tree)
			del tree_tmp[1, iitem]
			noun_tmp = tree[1, iitem, -1]
			if (answer_or_ask):
#				print(number, noun_tmp)
				head_tmp = tree[1, iitem]
				out.append((head_tmp, tree_tmp))
			else:
				head_tmp = 'Which ' + noun_tmp[0] 
			out.append((head_tmp, tree_tmp))
			break
		if (vp[iitem].label() == 'PP' and vp[iitem, 0].label() in ['TO', 'IN'] and vp[iitem, -1].label() == 'NP'):
			if (vp[iitem, -1, 0].label() == 'DT' and vp[iitem, -1, -1].label().startswith('NN')):
				tree_tmp = copy.deepcopy(tree)
				del tree_tmp[1, iitem, -1]
				noun_tmp = tree[1, iitem, -1, -1]
				if (answer_or_ask):
#				print(number, noun_tmp)
					head_tmp = tree[1, iitem, -1]
					out.append((head_tmp, tree_tmp))
				else:
					head_tmp = 'Which ' + noun_tmp[0] 
				out.append((head_tmp, tree_tmp))
				break
		iitem += 1
	return out

def find_whose(tree, answer_or_ask):
	out = []
	np = tree[0]
	vp = tree[1]
	if (np[0].label() == 'PRP$' and np[-1].label().startswith('NN')):
		tree_tmp = copy.deepcopy(tree)
		del tree_tmp[0]
		noun_tmp = tree[0, -1][0]
		if (answer_or_ask):
			head_tmp = np
			out.append((head_tmp, tree_tmp))
		else:
			head_tmp = 'Whose ' + noun_tmp[0]
			out.append((head_tmp, tree_tmp))
	iitem = 1
	while(True):
		try:
			vp[iitem]
#				print(vp[iperson])
		except:
			return out
		if (vp[iitem].label() == 'NP' and vp[iitem, 0].label() == 'PRP$' and vp[iitem, -1].label().startswith('NN')):
			tree_tmp = copy.deepcopy(tree)
			del tree_tmp[1, iitem]
			noun_tmp = tree[1, iitem, -1]
			if (answer_or_ask):
#				print(number, noun_tmp)
				head_tmp = tree[1, iitem]
				out.append((head_tmp, tree_tmp))
			else:
				head_tmp = 'Whose ' + noun_tmp[0] 
			out.append((head_tmp, tree_tmp))
			break
		if (vp[iitem].label() == 'PP' and vp[iitem, 0].label() in ['TO', 'IN'] and vp[iitem, -1].label() == 'NP'):
			if (vp[iitem, -1, 0].label() == 'PRP$' and vp[iitem, -1, -1].label().startswith('NN')):
				tree_tmp = copy.deepcopy(tree)
				del tree_tmp[1, iitem, -1]
				noun_tmp = tree[1, iitem, -1, -1]
				if (answer_or_ask):
#				print(number, noun_tmp)
					head_tmp = tree[1, iitem, -1]
					out.append((head_tmp, tree_tmp))
				else:
					head_tmp = 'Whose ' + noun_tmp[0] 
				out.append((head_tmp, tree_tmp))
				break
		iitem += 1
	return out

def find_what(tree, answer_or_ask):
	np = tree[0]
	vp = tree[1]
	out = []
	if (np.label() == 'NP'):
		tree_tmp = copy.deepcopy(tree)
		del tree_tmp[0]
		if (answer_or_ask):
			head_tmp = np
			out.append((head_tmp, tree_tmp))
		else:
			head_tmp = 'What'
			out.append((head_tmp, tree_tmp))
	iitem = 1

	while(True):
		try:
			vp[iitem]
#				print(vp[iperson])
		except:
			return out
		if (vp[iitem].label() == 'NP'):
			tree_tmp = copy.deepcopy(tree)
			del tree_tmp[1, iitem]
			if (answer_or_ask):
#				print(number, noun_tmp)
				head_tmp = tree[1, iitem]
				out.append((head_tmp, tree_tmp))
			else:
				head_tmp = 'What'
			out.append((head_tmp, tree_tmp))
			break
		iitem += 1
	return out



#find questions or answer

def find_a_wh(qtype, best_asent, bin_q):
	atree = parser.parse(best_asent.split())
	tags = tagger.tag(word_tokenize(best_asent))




	atree = sent_info.Get_tree(atree)
#	print(atree)
	np_index = 0
	while (atree[np_index].label() != 'NP'):
		np_index += 1
	np = atree[np_index]
	vp_index = np_index + 1
	while (atree[vp_index].label() != 'VP' and vp_index < len(atree)):
		vp_index += 1
	vp = atree[vp_index]
	if (atree[vp_index].label() != 'VP'):
		return best_asent

#	find_wh.has_netags(atree, vp_index, tags, ['PERSON'])

	
#	print(some)
	if (qtype == 'who_whom'):
		some_who_whom = find_who_whom(atree, tags, True)
		if (len(some_who_whom) > 0):
			print(pattern_q.tree_to_string(some_who_whom[0][0]))
#		print(some[0][0])
	if (qtype == 'where'):
		some_where = find_where(atree, tags, True)
		if (len(some_where) > 0):
			print(pattern_q.tree_to_string(some_where[0][0]))

	
	if (qtype == 'when'):
		some_when = find_when(atree, tags, True)
		if (len(some_when) > 0):
			print(pattern_q.tree_to_string(some_when[0][0]))

	
	if (qtype == 'how_many'):
		some_how_many = find_how_many(atree, True)
		if (len(some_how_many) > 0):
			print(some_how_many[0][0])

def find_q_wh(qtype, best_asent):
	atree = parser.parse(best_asent.split())
	tags = tagger.tag(word_tokenize(best_asent))




	atree = sent_info.Get_tree(atree)
#	print(atree)
	np_index = 0
	while (atree[np_index].label() != 'NP'):
		np_index += 1
	np = atree[np_index]
	vp_index = np_index + 1
	while (atree[vp_index].label() != 'VP' and vp_index < len(atree)):
		vp_index += 1
	vp = atree[vp_index]
	if (atree[vp_index].label() != 'VP'):
		return best_asent

#	find_wh.has_netags(atree, vp_index, tags, ['PERSON'])

	
#	print(some)
	if (qtype == 'who_whom'):
		some_who_whom = find_who_whom(atree, tags, False)
		if (len(some_who_whom) > 0):
			print(some_who_whom[0][0] + ' ' + pattern_q.sent_to_bin_q(some_who_whom[0][1]))
#			print(qtype, some_who_whom)
#		print(some[0][0])
	if (qtype == 'where'):
		some_where = find_where(atree, tags, False)
		if (len(some_where) > 0):
			print(some_where[0][0] + ' ' + pattern_q.sent_to_bin_q(some_where[0][1]))
#			print(qtype, some_where)

	
	if (qtype == 'when'):
		some_when = find_when(atree, tags, False)
		if (len(some_when) > 0):
			print(some_when[0][0] + ' ' + pattern_q.sent_to_bin_q(some_when[0][1]))
#			print(qtype, some_when)

	
	if (qtype == 'how_many'):
		some_how_many = find_how_many(atree, False)
		if (len(some_how_many) > 0):
			print(some_how_many[0][0] + ' ' + pattern_q.sent_to_bin_q(some_how_many[0][1]))
#			print(qtype, some_how_many)


