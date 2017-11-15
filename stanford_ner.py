import os
import sys
import numpy as np
from nltk.tag.stanford import StanfordNERTagger
from nltk.internals import find_jars_within_path

def tagger():
	stanford_dir = '/Users/wobabashifbj/Documents/natural_language_pro/project/final/stanford/stanford-ner-2015-12-09/'
	jarfile = stanford_dir + 'stanford-ner.jar'
	modelfile = stanford_dir + 'classifiers/english.all.3class.distsim.crf.ser.gz'
	st = StanfordNERTagger(model_filename=modelfile, path_to_jar=jarfile)#, encoding='utf-8')
#	s = word_tokenize('Rami Eid is studying at Stony Brook University in NY')
	stanford_dir = st._stanford_jar.rpartition('/')[0]
	stanford_jars = find_jars_within_path(stanford_dir)
	st._stanford_jar = ':'.join(stanford_jars)
	return st