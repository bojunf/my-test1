import os
import sys
import numpy as np
from nltk.parse.stanford import StanfordParser


def parser():
	return StanfordParser(model_path='edu/stanford/nlp/models/lexparser/englishPCFG.ser.gz')