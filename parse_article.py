import numpy as np
import os
import sys
import nltk

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
	with open(fname, 'r') as f:
		for line in f.readlines():
			s = nltk.word_tokenize(line)
			if (s == []):
				continue
			sent_tmp = []
			for ele in s:
				if (ele != '.'):
					sent_tmp.append(ele)
				else:
					sent_tmp.append(ele)
					if (len(sent_tmp) > 40):
						continue
					if (len(sent_tmp) == 0):
						continue
					sentence.append(" ".join(sent_tmp))
					sent_tmp = []

#	if (len(sentence) > 10):
#		sentence = sentence[:10]

	return sentence
def Get_q(q_file):
	quest = []
	with open(q_file, 'r') as f:
		for line in f.readlines():
			arr = line.strip()
			arr = arr.split()
			if (len(arr) > 40):
				continue
			if (len(arr) == 0):
				continue
			quest.append(" ".join(arr))
	return quest