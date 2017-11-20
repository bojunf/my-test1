import os
import sys
import numpy as np
import nltk
from nltk.corpus import treebank
from nltk.parse.stanford import StanfordParser
from nltk.tag.stanford import StanfordPOSTagger, StanfordNERTagger
from nltk.tree import Tree
import parse_article
import sent_info
import pattern
import gen_q
from nltk import word_tokenize, pos_tag
from nltk.internals import find_jars_within_path

#nltk.internals.config_java(options='-xmx2G')


#st = StanfordNERTagger("/Users/wobabashifbj/Documents/natural_language_pro/project/final/stanford/stanford-ner-2015-12-09/classifiers/english.all.3class.distsim.crf.ser.gz")


stanford_dir = '/Users/wobabashifbj/Documents/natural_language_pro/project/final/stanford/stanford-ner-2015-12-09/'
jarfile = stanford_dir + 'stanford-ner.jar'
modelfile = stanford_dir + 'classifiers/english.all.3class.distsim.crf.ser.gz'
st = StanfordNERTagger(model_filename=modelfile, path_to_jar=jarfile)#, encoding='utf-8')
s = word_tokenize('Rami Eid is studying at Stony Brook University in NY')

#print(st._stanford_jar)
stanford_dir = st._stanford_jar.rpartition('/')[0]
stanford_jars = find_jars_within_path(stanford_dir)
#print(":".join(stanford_jars))
st._stanford_jar = ':'.join(stanford_jars)
s = st.tag(s)
for i in s:
	print(i, i[0], i[1])

#print(s)

#st = StanfordNERTagger(model_filename='edu/stanford/nlp/models/lexparser/english.all.3class.distsim.crf.ser.gz')



#s = pos_tag(word_tokenize('Rami Davis is studying at Stony Brook University in NY'))
