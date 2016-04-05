#Copyright (c) Jesús Manuel Mager Hois 2016
#
#Permission is hereby granted, free of charge, to any person obtaining a
#copy of this software and associated documentation files (the
#    "Software"), to deal in the Software without restriction, including
#without limitation the rights to use, copy, modify, merge, publish,
#distribute, sublicense, and/or sell copies of the Software, and to
#permit persons to whom the Software is furnished to do so, subject to
#the following conditions:
#
#The above copyright notice and this permission notice shall be included
#in all copies or substantial portions of the Software.
#
#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
#OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
#MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. 
#IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
#CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
#TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
#SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.


import sys
import pickle as pk
import sys

import nltk
from nltk import word_tokenize
from nltk.util import ngrams

import wixanlp as wixa


def eval_pair(lm, pair):
    """ Get probability of a pair of words """ 
    try:
        p = lm[pair[0]][pair[1]]
    except KeyError:
        p = 0
    return p

def eval_text(lm, text):
    tokens = word_tokenize(text)
    chain = []
    for word in tokens:
        w = list(word.lower())

        # Dividing in 2-grams
        bgs = ngrams(w, 4)
        w = []
        for bg in bgs:
            w.append(bg[0]+bg[1])
            w.append(bg[2]+bg[3])

        p = 0
        i = 0
        for i in range(len(w)-1):
            p = float(p) + eval_pair(lm, (w[i], w[i+1]))
        p = float(p) / float(i+1)

        #If the word exists in the common word list, then p = .5
        # .5 is an arbitrary value
        if word in common:
            p = 0.2

        chain.append((p, word))
    return chain

if __name__ == "__main__":

    if len(sys.argv) != 2:
        print("Usage: python3 idtext.py filename.txt")
        sys.exit(1)
    filename = sys.argv[1]
    print(filename)
    
 
    confusion = 0
    try:
        f=open("confusion.pickle", "rb")
        confusion = pk.load(f)
    except OSError:
        confusion = {} 
    # Load the common word list
    with open("common.pickle", "rb") as f:
        common = pk.load(f)
    # Load the language model 
    with open("lm.pickle", "rb") as f:
        lm = pk.load(f)

    txt = open(filename, 'r')
    txt = txt.read()
    txt = wixa.norm(txt, prepare=0)

    chain = eval_text(lm, txt)

    now = 0
    first = 0
    total = len(chain)
    words = []
    threshold = 0.01
    print(common)
    while now < total:
        if chain[now][0] > threshold and len(chain[now][1]) > 3:
            if chain[now][0] in common:
                continue
            words.append(chain[now])
        now += 1


    tconfusion = []
    for w in words:
        tconfusion.append(w[1])
    confusion = confusion.union(set(tconfusion))
    with open("confusion.pickle", "wb") as f:
        pk.dump(confusion, f)
    print(confusion)

    print("Total number of confusion words:", str(len(confusion)))

