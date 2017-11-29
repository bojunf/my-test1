import numpy as np
import os
import sys
import nltk
import io
import stanford_parser
import stanford_ner


parser = stanford_parser.parser()
tagger = stanford_ner.tagger()


def Get_sent(fname): # parse file that one line has one sentence
	sentence = []
	with open(fname, 'r') as f:
		for line in f.readlines():
			s = nltk.word_tokenize(line)
			if (len(s) > 40):
				continue
			if (len(s) == 0):
				continue
			sentence.append(" ".join(s))

#	if (len(sentence) > 10):
#		sentence = sentence[:10]

	return sentence


def Get_sent_msal(fname): # parse file that one line has multiple sentence
	sentence = []
	with io.open(fname, 'r', encoding="utf-8") as f:
		for line in f.readlines():
			sent_tmp = nltk.sent_tokenize(line)
			for s in sent_tmp:
				sentence.append(s)
			
#			line = line.decode('UTF-8')
			# s = nltk.word_tokenize(line)
			# if (s == []):
			# 	continue
			# sent_tmp = []
			# for ele in s:
			# 	if (ele != '.'):
			# 		sent_tmp.append(ele)
			# 	else:
			# 		sent_tmp.append(ele)
			# 		if (len(sent_tmp) > 50):
			# 			continue
			# 		if (len(sent_tmp) == 0):
			# 			continue
			# 		sentence.append(" ".join(sent_tmp))
			# 		sent_tmp = []

#	if (len(sentence) > 10):
#		sentence = sentence[:10]

	return sentence


def Get_sent_msal_q(fname): # parse file that one line has multiple sentence
	sentence = []
	with open(fname, 'r') as f:
		for line in f.readlines():
			sent_tmp = nltk.sent_tokenize(line)
			for s in sent_tmp:
				sentence.append(s + ' .')
			
#			line = line.decode('UTF-8')
			# s = nltk.word_tokenize(line)
			# if (s == []):
			# 	continue
			# sent_tmp = []
			# for ele in s:
			# 	if (ele != '.'):
			# 		sent_tmp.append(ele)
			# 	else:
			# 		sent_tmp.append(ele)
			# 		if (len(sent_tmp) > 50):
			# 			continue
			# 		if (len(sent_tmp) == 0):
			# 			continue
			# 		sentence.append(" ".join(sent_tmp))
			# 		sent_tmp = []

#	if (len(sentence) > 10):
#		sentence = sentence[:10]

	return sentence

def Get_q(q_file):
	quest = []
	with open(q_file, 'r') as f:
		for line in f.readlines():
			arr = line.strip()
			arr = arr.split()
#			if (len(arr) > 40):
#				continue
			if (len(arr) == 0):
				continue
			quest.append(" ".join(arr))
	return quest



def Get_person(fname):
	dic_ne = {}
	dic_nnp = {}
	dic_nnps = {}
	with io.open(fname, 'r', encoding = 'utf-8') as f:
		for line in f.readlines():
			s = nltk.word_tokenize(line)
			if (s == []):
				continue
			tags = tagger.tag(s)
			pos = nltk.pos_tag(s)
			for tag in tags:
				if (tag[1] == "PERSON"):
					if (tag[0] not in dic_ne):
						dic_ne[tag[0]] = 1
					else:
						dic_ne[tag[0]] += 1

			for tag in pos:
				if (tag[1] == "NNP"):
					if (tag[0] not in dic_nnp):
						dic_nnp[tag[0]] = 1
					else:
						dic_nnp[tag[0]] += 1
				if (tag[1] == "NNPS"):
					if (tag[0] not in dic_nnps):
						dic_nnps[tag[0]] = 1
					else:
						dic_nnps[tag[0]] += 1

	maxcntname = 0
	maxcntnnp = 0
	maxcntnnps = 0
	for key in dic_ne:
		if (dic_ne[key] > maxcntname):
			maxcntname = dic_ne[key]
			maxname = key
	for key in dic_nnp:
		if (dic_nnp[key] > maxcntnnp):
			maxnnp = key
			maxcntnnp = dic_nnp[key]
	for key in dic_nnps:
		if (dic_nnps[key] > maxcntnnps):
			maxnnps = key
			maxcntnnps = dic_nnps[key]

	return maxname.encode('utf-8'), maxnnp.encode('utf-8'), maxnnps.encode('utf-8')






