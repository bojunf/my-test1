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
import get_wh_q
import pattern_q
import find_wh
import sort_q

wh_tag = ['how_many', 'how', 'why', 'which', 'whose', 'who_whom', 'where', 'when', 'what']

fname = str(sys.argv[1])
N = int(sys.argv[2])

parser = stanford_parser.parser()
tagger = stanford_ner.tagger()

sentence = parse_article.Get_sent_msal(fname)



txtfile = fname.split('/')[-1]
#print(txtfile)
#sys.exit(0)


#for s in sentence:
#	print(len(s))
parse_trees = []
for s in sentence:
#	print(s)
	t = parser.parse(s.split())
	t = sent_info.Get_tree(t)
	parse_trees.append(t)
#	print(t)

transform = pattern_s.extract_stem(parse_trees)

#for s in transform:
#	print(len(s))
#sys.exit(0)


trans_trees = []
for s in transform:
#	print(s)
	t = parser.parse(s.split())
	t = sent_info.Get_tree(t)
	trans_trees.append(t)


##sample easy question
##easy_tree = pattern.find_easyp(parse_trees)
##for tree in easy_tree:
##	sent, ans = gen_q.gen_bin_normp(tree)	
##	sent, ans = gen_q.gen_bin_easyp(tree)
##	print(sent, ans)

#sample norm bin question
#some_tree = pattern.find_normp(trans_trees)
#for tree in trans_trees:
#	print(tree)
#	sent, ans = gen_q.gen_bin_normp(tree)
#	print(sent, ans)

#print(trans_trees[-1])
#print(gen_q.change_verb(trans_trees[-1]))
#print(trans_trees[-1])



#question_wh = []
#question_binary = []

for tree in trans_trees:
	if (len(tree) <= 1):
		continue
	sent = gen_q.tree_to_string(tree)
#	sent_for_tag = word_tokenize(sent)
#	tags = tagger.tag(sent_for_tag)
#	for qtype in wh_tag:
	find_wh.find_q_wh(sent, 'q-' + txtfile)

sort_q.sort('q-' + txtfile, N)






