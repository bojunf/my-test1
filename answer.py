import os
import sys
import numpy as np
import nltk
import parse_article
import sent_info
import pattern_s
import gen_q
import stanford_parser
import stanford_ner
from nltk import word_tokenize, pos_tag
import pattern_q
import find_a
import find_wh




#def find_a_bin(best_asent, bin_q):
#	nega = ["not", "n't"]
#	tmpa = word_tokenize(best_asent)
#	ans = 'Yes'
#	for i in tmpa:
#		if (i in nega):
#			return 'No'
#	return ans




file_name = str(sys.argv[1])
q_file = str(sys.argv[2])

parser = stanford_parser.parser()
tagger = stanford_ner.tagger()

sentence = parse_article.Get_sent_msal(file_name)

sentence_r = find_a.lemma_verb(sentence)
idf = find_a.cal_idf(sentence_r)
maxname, maxnnp, maxnnps = parse_article.Get_person(file_name)
print(maxname, maxnnp, maxnnps)
sys.exit(0)

txtfile = file_name.split('/')[-1]


quest = parse_article.Get_q(q_file)

quest_trees = []

for q in quest:
	q = q.decode('utf-8')
	t = parser.parse(q.split())
	t = sent_info.Get_tree(t)
#	print(t)
	quest_trees.append(t)

for i in range(len(quest_trees)):
	qt, qtree = pattern_q.q_type(quest_trees[i])
	if (qt == 'who' or qt == 'whom'):
		qt = 'who_whom'
#	print(qt)
#	print(quest_trees[i])
#	print(qt)
#	print(qtree)
	if (qt is None):
#		print(sentence[i])
		print(quest[i])
		print('\n')
		continue
	try:
		q_to_s = pattern_q.bin_q_to_sent(qtree)
	except:
		q_to_s = pattern_q.tree_to_string(qtree)
	
	best_sent = find_a.best_match(q_to_s, sentence_r, idf)
	answer = sentence[best_sent]
#	answer = answer.encode('utf-8')
#	print(q_to_s)
#	print(quest[i], answer)
	print(quest[i])

#	answer_trans = pattern_s.extract_stem([answer])
#	answer_trans = answer_trans[0]
	find_wh.find_a_wh(qt, answer, q_to_s, 'a-' + txtfile, maxname, maxnnp, maxnnps, quest[i])
	print('\n')










