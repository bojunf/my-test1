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




def find_a_bin(best_asent, bin_q):
	nega = ["not", "n't"]
	tmpa = word_tokenize(best_asent)
	ans = 'Yes'
	for i in tmpa:
		if (i in nega):
			return 'No'
	return ans




file_name = str(sys.argv[1])
q_file = str(sys.argv[2])

parser = stanford_parser.parser()
tagger = stanford_ner.tagger()

sentence = parse_article.Get_sent_msal(file_name)

sentence_r = find_a.lemma_verb(sentence)
idf = find_a.cal_idf(sentence_r)

quest = parse_article.Get_q(q_file)

quest_trees = []

for q in quest:
	t = parser.parse(q.split())
	t = sent_info.Get_tree(t)
#	print(t)
	quest_trees.append(t)

for i in range(len(quest_trees)):
	qt, qtree = pattern_q.q_type(quest_trees[i])
	if (qt == 'who'):
		qt = 'who_whom'
#	print(qt)
#	print(qtree)
	if (qt is None):
#		print(sentence[i])
		continue
	try:
		q_to_s = pattern_q.bin_q_to_sent(qtree)
	except:
		q_to_s = pattern_q.tree_to_string(qtree)
	
	best_sent = find_a.best_match(q_to_s, sentence_r, idf)
	answer = sentence[best_sent]
#	print(q_to_s)
	print(quest[i], answer)



	find_a_wh(qt, answer, q_to_s)










