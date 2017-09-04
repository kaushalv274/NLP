#!/usr/bin/env python
import argparse
import sys
import codecs
if sys.version_info[0] == 2:
  from itertools import izip
else:
  izip = zip
from collections import defaultdict as dd
import re
import os.path
import gzip
import tempfile
import shutil
import atexit

# Use word_tokenize to split raw text into words
from string import punctuation

import nltk
from nltk.tokenize import word_tokenize

scriptdir = os.path.dirname(os.path.abspath(__file__))

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

def addonoffarg(parser, arg, dest=None, default=True, help="TODO"):
  ''' add the switches --arg and --no-arg that set parser.arg to true/false, respectively'''
  group = parser.add_mutually_exclusive_group()
  dest = arg if dest is None else dest
  group.add_argument('--%s' % arg, dest=dest, action='store_true', default=default, help=help)
  group.add_argument('--no-%s' % arg, dest=dest, action='store_false', default=default, help="See --%s" % arg)



class LimerickDetector:

    def __init__(self):
        """
        Initializes the object to have a pronunciation dictionary available
        """
        self._pronunciations = nltk.corpus.cmudict.dict()


    def num_syllables(self, word):
        """
        Returns the number of syllables in a word.  If there's more than one
        pronunciation, take the shorter one.  If there is no entry in the
        dictionary, return 1.
        """
        prondict = self._pronunciations
        if word in prondict:
            syll_cnt = []
            vowels = {'a','e','i','o','u','A','E','I','O','U'}
            syll_list = prondict[word]
            # Count syllables in each list here.
            for item in syll_list:
                cnt = 0;
                for ph in item:
                    if ph[0] in vowels:
                        cnt += 1
                syll_cnt.append(cnt)
            return min(syll_cnt)
        else:
            return 1
        # TODO: provide an implementation!


    def rhym_help(self, a, b):
        vowels = {'a','e','i','o','u','A','E','I','O','U'}
        a_suf = []
        b_suf = []
        for idx,val in enumerate(a):
            if val[0] in vowels:
                a_suf = a[idx:]
                break
        for idx,val in enumerate(b):
            if val[0] in vowels:
                b_suf = b[idx:]
                break
        #print(a_suf)
        #print(b_suf)
        a_str = "".join(a_suf)
        b_str = "".join(b_suf)

        if a_str.endswith(b_str) or b_str.endswith(a_str):
            return True

        return False


    def rhymes(self, a, b):
        """
        Returns True if two words (represented as lower-case strings) rhyme,
        False otherwise.
        """
        prondict = self._pronunciations
        if a in prondict and b in prondict:
            for phoa in prondict[a]:
                for phob in prondict[b]:
                    #print(phoa," kaushal ",phob)
                    is_rhyme = self.rhym_help(phoa,phob)
                    if is_rhyme:
                        return True
        # TODO: provide an implementation!

        return False


    def is_limerick(self, text):
        """
        Takes text where lines are separated by newline characters.  Returns
        True if the text is a limerick, False otherwise.

        A limerick is defined as a poem with the form AABBA, where the A lines
        rhyme with each other, the B lines rhyme with each other, and the A lines do not
        rhyme with the B lines.


        Additionally, the following syllable constraints should be observed:
          * No two A lines should differ in their number of syllables by more than two.
          * The B lines should differ in their number of syllables by no more than two.
          * Each of the B lines should have fewer syllables than each of the A lines.
          * No line should have fewer than 4 syllables

        (English professors may disagree with this definition, but that's what
        we're using here.)

        """
        lines = text.split('\n')
        length = len(lines)
        if not lines[length-1].strip():
            del lines[length-1]
            length -= 1
        if not lines[0].strip():
            length -= 1
            del lines[0]
        print(length)
        if(length != 5):
            return False

        a = [lines[0], lines[1], lines[4]]
        b = [lines[2], lines[3]]

        a_syl_cnt = []
        b_syl_cnt = []
        a_last = []
        b_last = []
        punct = {',','!','.','?',';',':','"',"'"}
        for item in a:
            tokens = nltk.tokenize.word_tokenize(item.lower())
            syl_cnt = 0
            lw = ""
            for token in tokens:
                if token not in punct:
                    syl_cnt += self.num_syllables(token)
                    lw = token
            a_last.append(lw)
            a_syl_cnt.append(syl_cnt)

        for item in b:
            tokens = nltk.tokenize.word_tokenize(item.lower())
            syl_cnt = 0
            lw = ""
            for token in tokens:
                if token not in punct:
                    syl_cnt += self.num_syllables(token)
                    lw = token
            b_syl_cnt.append(syl_cnt)
            b_last.append(lw)

        print(a_syl_cnt,"a_syl_cnt  ",a_last," a_last")
        print(b_syl_cnt,"b_syl_cnt  ",b_last," b_last")
        
        min_a = 1000000;
        for i in range(0,2):
            for j in range(i+1,3):
                min_a = min(min_a,a_syl_cnt[i],a_syl_cnt[j])
                if a_syl_cnt[i] <4 or a_syl_cnt[j]<4 or abs(a_syl_cnt[i]-a_syl_cnt[j])>2:
                    return False
                if not self.rhymes(a_last[i], a_last[j]):
                    return False
        # TODO: provide an implementation!

        if b_syl_cnt[0] <4 or b_syl_cnt[1]<4 or abs(b_syl_cnt[0]-b_syl_cnt[1])>2 or max(b_syl_cnt[0],b_syl_cnt[1])>min_a:
            return False

        if not self.rhymes( b_last[0], b_last[1]):
            return False
        for item_a in a_last:
            for item_b in b_last:
                if self.rhymes( item_a, item_b):
                    return False

        return True


# The code below should not need to be modified
def main():
  parser = argparse.ArgumentParser(description="limerick detector. Given a file containing a poem, indicate whether that poem is a limerick or not",
                                   formatter_class=argparse.ArgumentDefaultsHelpFormatter)
  addonoffarg(parser, 'debug', help="debug mode", default=False)
  parser.add_argument("--infile", "-i", nargs='?', type=argparse.FileType('r'), default=sys.stdin, help="input file")
  parser.add_argument("--outfile", "-o", nargs='?', type=argparse.FileType('w'), default=sys.stdout, help="output file")




  try:
    args = parser.parse_args()
  except IOError as msg:
    parser.error(str(msg))

  infile = prepfile(args.infile, 'r')
  outfile = prepfile(args.outfile, 'w')

  ld = LimerickDetector()
  lines = ''.join(infile.readlines())
  outfile.write("{}\n-----------\n{}\n".format(lines.strip(), ld.is_limerick(lines)))

if __name__ == '__main__':
  main()
