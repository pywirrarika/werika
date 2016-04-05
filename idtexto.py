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
import numpy as np

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

        if word in confusion:
            p = 0

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
        pass
        
 
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
    lastn = 0
    nextn = 2
    first = 0
    total = len(chain)
    words = []
    tmp = [] 
    threshold = 0.01

    while now < total-2:
        now += 1
        if chain[now-1][0] > threshold:
            lastn = 1
        else:
            lastn = 0
        if chain[now+1][0] > threshold:
            nextn = 1
        else:
            nextn = 0
        
        if (chain[now][0] > threshold) and nextn and lastn:
            if not first:
                tmp.append(chain[now - 1])
                tmp.append(chain[now])
                tmp.append(chain[now + 1])
                first = 1
            else:
                tmp.append(chain[now + 1])
        elif first:
            tmp.append(chain[now + 1])
            first = 0
            tmp2 = []
            for wt in tmp:
                if wt[0] > threshold and wt[0]:
                    tmp2.append(wt)
            words.append((list(tmp2)))
            tmp = []

    i = 0
    j = 0
    inphrase = 0

    for p in words:
        for w in p:
            print(w[1], end=" ")
        print("")

    print("Total number of phrases:", str(len(words)))

