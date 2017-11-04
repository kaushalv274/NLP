#!/bin/python
import nltk
import os
import string

def preprocess_corpus(train_sents):
    """Use the sentences to do whatever preprocessing you think is suitable,
    such as counts, keeping track of rare features/words to remove, matches to lexicons,
    loading files, and so on. Avoid doing any of this in token2features, since
    that will be called on every token of every sentence.

    Of course, this is an optional function.

    Note that you can also call token2features here to aggregate feature counts, etc.
    """
    file_map = dict()
    rootdir = 'data/lexicon'
    for subdir, dirs, files in os.walk(rootdir):
        for f in files:
            filepath = subdir + os.sep + f
            file_map[f] = set(line.strip() for line in open(filepath))
    return file_map

def token2features(sent, i, tags, file_map, add_neighs = True):
    """Compute the features of a token.

    All the features are boolean, i.e. they appear or they do not. For the token,
    you have to return a set of strings that represent the features that *fire*
    for the token. See the code below.

    The token is at position i, and the rest of the sentence is provided as well.
    Try to make this efficient, since it is called on every token.

    One thing to note is that it is only called once per token, i.e. we do not call
    this function in the inner loops of training. So if your training is slow, it's
    not because of how long it's taking to run this code. That said, if your number
    of features is quite large, that will cause slowdowns for sure.

    add_neighs is a parameter that allows us to use this function itself in order to
    recursively add the same features, as computed for the neighbors. Of course, we do
    not want to recurse on the neighbors again, and then it is set to False (see code).
    """
    ftrs = []
    # bias
    ftrs.append("BIAS")
    # position features
    if i == 0:
        ftrs.append("SENT_BEGIN")
    if i == len(sent)-1:
        ftrs.append("SENT_END")

    # the word itself
    word = unicode(sent[i])
    ftrs.append("WORD=" + word)
    ftrs.append("LCASE=" + word.lower())

    # some features of the word
    if word.isalnum():
        ftrs.append("IS_ALNUM")
    if word.isnumeric():
        ftrs.append("IS_NUMERIC")
    if word.isdigit():
        ftrs.append("IS_DIGIT")
    if word.isupper():
        ftrs.append("IS_UPPER")
    if word.islower():
        ftrs.append("IS_LOWER")
    if word[0].isupper():
        ftrs.append("FIRST_UPPER")

    #My Code
    #ftrs.append("LENGTH=" + str(len(word)))
    ftrs.append("POS_TAG=" + tags[i][1])
    ftrs.append("FIRST_THREE" + word[:3])
    ftrs.append("LAST_THREE" + word[-3:])

    puncts = set(string.punctuation)
    punct_cnt = 0
    digit_cnt = 0
    caps_cnt = 0
    for c in word:
        if c in puncts:
            punct_cnt += 1
        if c.isdigit():
            digit_cnt += 1
        if c.islower():
            caps_cnt += 1

    #ftrs.append("WORD_LOC_" + str(i))
    #ftrs.append("PUNCT_CNT_" + str(punct_cnt))
    ftrs.append("DIGIT_CNT_" + str(digit_cnt))
    ftrs.append("CAPS_CNT_" + str(caps_cnt))

    bi_word = ''
    tri_word = ''
    # For bi-words and tri-words
    if i < len(sent)-1:
        bi_word = unicode(sent[i]) + ' ' +unicode(sent[i+1])
    if i < len(sent)-2:
        tri_word = unicode(sent[i]) + ' ' +unicode(sent[i+1]) + ' ' + unicode(sent[i+2])

    if add_neighs:
        for f, values in file_map.iteritems():
            if word in values:
                ftrs.append("WORD_" + f)
            if len(bi_word)>1:
                if bi_word in values:
                    ftrs.append("BI_WORD_" + f)
            if len(tri_word)>2:
                if tri_word in values:
                    ftrs.append("TRI_WORD_" + f)


    # previous/next word feats
    if add_neighs:
        if i > 0:
            for pf in token2features(sent, i-1, tags, file_map, add_neighs = False):		
                ftrs.append("PREV_" + pf)
        if i < len(sent)-1:
            for pf in token2features(sent, i+1, tags, file_map, add_neighs = False):
                ftrs.append("NEXT_" + pf)

    # return it!
    return ftrs

if __name__ == "__main__":
    sents = [
    [ "I", "love", "food", "What", "is", "Los", "Angeles", "I", "am", "Great"]
    ]
    file_map = preprocess_corpus(sents)
    for sent in sents:
        tags = nltk.pos_tag(sent)
        for i in xrange(len(sent)):
            print sent[i], ":", token2features(sent, i, tags, file_map)
