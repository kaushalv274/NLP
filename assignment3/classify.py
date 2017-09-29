#!/usr/bin/env python
from collections import defaultdict
from csv import DictReader, DictWriter
import string
import nltk
import codecs
import sys
from nltk.corpus import wordnet as wn
from nltk.tokenize import TreebankWordTokenizer
from collections import Counter

kTOKENIZER = TreebankWordTokenizer()

def morphy_stem(word):
    """
    Simple stemmer
    """
    stem = wn.morphy(word)
    if stem:
        return stem.lower()
    else:
        return word.lower()

class FeatureExtractor:
    def __init__(self):

        None

    def features(self, text):
        d = defaultdict(int)
        st = text.strip().lower()
        #print text
        tt = st.translate(None,string.punctuation)
        tokens = kTOKENIZER.tokenize(tt)
        tags = nltk.pos_tag(tokens)
        #print text

        #print text[-1]
        le = len(tokens)
        d['length'] = le
        d['char_length'] = len(tt)
        for ele in tokens:
            d[ele] +=1
        # for ele in tt:
        #     d[ele] +=1
        # temp = ''.join(tt.split())
        # for idx,ele in enumerate(temp):
        #     if idx < len(temp)-1:
        #         d[temp[idx:idx+2]] += 1

        # for idx,ele in enumerate(tt):
        #     if idx < len(tt)-2:
        #         d[ele[idx:idx+3]] += 1

        #for idx,ele in enumerate(tags):
        #    if idx < len(tags):
        #         d[tags[idx][1]] +=1
            #print ele[1],
            #pass
        #print 
        d['startswith'] = tags[0]
        d['endswith'] = tags[-1]
        # d['len_first_token'] = len(tokens[0])
        d['len_last_token'] = len(tokens[-1])
        # maxi =0
        # max_tag = ''
        # tag_dic = Counter([x[1] for x in tags])
        # for key,value in tag_dic.iteritems():
        #     if value > maxi:
        #         max_tag = key
        #         maxi = value
        # d['max_tag'] = max_tag

        # for ele in tokens:
	       #  d[len(ele)] +=1
        # sum = 0
        # for ele in tokens:
        #     sum += len(ele)
        # d['avg_len'] = sum / len(tokens)
        
        # for idx,ele in enumerate(tokens):
        #     if idx < (len(tokens)-2):
        #         d[morphy_stem(tokens[idx])+' '+morphy_stem(tokens[idx+1])+' '+morphy_stem(tokens[idx+2])] += 1
        for idx,ele in enumerate(tokens):
            if idx < (len(tokens)-1):
                d[morphy_stem(tokens[idx])+' '+morphy_stem(tokens[idx+1])] +=1
        # for idx,ele in enumerate(tokens):
        #     if idx < (len(tokens)-3):
        #         d[morphy_stem(tokens[idx])+' '+morphy_stem(tokens[idx+1])+' '+morphy_stem(tokens[idx+2])+' '+morphy_stem(tokens[idx+3])] +=1
        return d
reader = codecs.getreader('utf8')
writer = codecs.getwriter('utf8')


def prepfile(fh, code):
  if type(fh) is str:
    fh = open(fh, code)
  ret = gzip.open(fh.name, code if code.endswith("t") else code+"t") if fh.name.endswith(".gz") else fh
  if sys.version_info[0] == 2:
    if code.startswith('r'):
      ret = reader(fh)
    elif code.startswith('w'):
      ret = writer(fh)
    else:
      sys.stderr.write("I didn't understand code "+code+"\n")
      sys.exit(1)
  return ret

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument("--trainfile", "-i", nargs='?', type=argparse.FileType('r'), default=sys.stdin, help="input train file")
    parser.add_argument("--testfile", "-t", nargs='?', type=argparse.FileType('r'), default=None, help="input test file")
    parser.add_argument("--outfile", "-o", nargs='?', type=argparse.FileType('w'), default=sys.stdout, help="output file")
    parser.add_argument('--subsample', type=float, default=1.0,
                        help='subsample this fraction of total')
    args = parser.parse_args()
    trainfile = prepfile(args.trainfile, 'r')
    if args.testfile is not None:
        testfile = prepfile(args.testfile, 'r')
    else:
        testfile = None
    outfile = prepfile(args.outfile, 'w')

    # Create feature extractor (you may want to modify this)
    fe = FeatureExtractor()
    
    # Read in training data
    train = DictReader(trainfile, delimiter='\t')
    
    # Split off dev section
    dev_train = []
    dev_test = []
    full_train = []

    for ii in train:
        if args.subsample < 1.0 and int(ii['id']) % 100 > 100 * args.subsample:
            continue
        feat = fe.features(ii['text'])
        #print feat
        if int(ii['id']) % 5 == 0:
            dev_test.append((feat, ii['cat']))
        else:
            dev_train.append((feat, ii['cat']))
        full_train.append((feat, ii['cat']))

    # Train a classifier
    sys.stderr.write("Training classifier ...\n")
    classifier = nltk.classify.NaiveBayesClassifier.train(dev_train)
    #classifier.show_most_informative_features(10)
    right = 0
    total = len(dev_test)
    for ii in dev_test:
        prediction = classifier.classify(ii[0])
        if prediction == ii[1]:
            right += 1
    sys.stderr.write("Accuracy on dev: %f\n" % (float(right) / float(total)))

    if testfile is None:
        sys.stderr.write("No test file passed; stopping.\n")
    else:
        # Retrain on all data
        classifier = nltk.classify.NaiveBayesClassifier.train(dev_train + dev_test)

        # Read in test section
        test = {}
        for ii in DictReader(testfile, delimiter='\t'):
            test[ii['id']] = classifier.classify(fe.features(ii['text']))

        # Write predictions
        o = DictWriter(outfile, ['id', 'pred'])
        o.writeheader()
        for ii in sorted(test):
            o.writerow({'id': ii, 'pred': test[ii]})
