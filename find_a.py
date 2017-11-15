import re, numpy
from collections import Counter, defaultdict
from nltk.corpus import wordnet
from nltk import word_tokenize, pos_tag
from nltk.stem.wordnet import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()

WORD = re.compile(r'\w+')

def best_match(quest, sentences, idf_sentences):

    best_sent = -1
    best_cos = -1.0

    quest_words = word_tokenize(quest)
    quest_weight = defaultdict(dict)
    quest_tf = cal_tf(quest_words)
#    print(quest_words)
#    print(idf_sentences)
    for word in quest_words:
#        print(word)
#        print(quest_weight[word], quest_tf[word], idf_sentences[word])
        try:
            quest_weight[word] = quest_tf[word] * idf_sentences[word]
        except:
            try:
                wordr = word[0].upper() + word[1:]
                quest_weight[wordr] = quest_tf[wordr] * idf_sentences[wordr]
            except:
                pass

    for i in range(len(sentences)):
        sentence = sentences[i]
        sent_words = word_tokenize(sentence)
        sent_tf = cal_tf(sent_words)
        sent_weight = defaultdict(dict)
        for word in sent_words:
            try:
                sent_weight[word] = sent_tf[word] * idf_sentences[word]
            except:
                pass

        cosine = get_cosine_vec(quest_weight, sent_weight)
#        print(sentences[i],cosine)
        if (cosine > best_cos):
            best_cos = cosine
            best_sent = i
    return best_sent
     

def get_cosine_vec(quest, sent):
    nsum = 0.0
    for i in quest:
        if (i in sent):
            nsum += quest[i] * sent[i]

    dsum1 = 0.0
    dsum2 = 0.0
    for i in quest:
        dsum1 += quest[i] * quest[i]
    for j in sent:
        dsum2 += sent[j] * sent[j]
    return nsum / numpy.sqrt(dsum1) #* dsum2)
 #   return nsum / (numpy.sqrt(dsum1) * numpy.sqrt(dsum2))


def get_cosine_text(text1, text2):
    vec1 = text_to_vector(text1)
    vec2 = text_to_vector(text2)
    intersection = set(vec1.keys()) & set(vec2.keys())
    numerator = sum([vec1[x] * vec2[x] for x in intersection])

    sum1 = sum([vec1[x]**2 for x in vec1.keys()])
    sum2 = sum([vec2[x]**2 for x in vec2.keys()])
    denominator = math.sqrt(sum1) * math.sqrt(sum2)

    if not denominator:
       return 0.0
    else:
       return float(numerator) / denominator

def text_to_vector(text):
    words = WORD.findall(text)
    return Counter(words)


def cal_idf(sentences):
    N = len(sentences)
    cdf = Counter()
    for sentence in sentences:
        seen = []
        sentence = word_tokenize(sentence)
        for word in sentence:
            if (word not in seen):
                cdf[word] += 1
                seen.append(word)

    idf = defaultdict(dict)
    for word in cdf:
        idf[word] = numpy.log(N/float(cdf[word]))
    return idf


def cal_tf(word_list):
    tf = Counter()
    for word in word_list:
        tf[word] += 1
    return tf

def lemma_verb(sentences): # because pattern.en is not available for python3
    lemma_sentences = []
    for sentence in sentences:
        tmp_s = []
        sentence = word_tokenize(sentence)
        for word in sentence:
            tmp_s.append(lemmatizer.lemmatize(word, 'v'))
        tmp = " ".join(tmp_s)
        lemma_sentences.append(tmp)
    return lemma_sentences