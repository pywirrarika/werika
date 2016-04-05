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



import nltk
from nltk.util import ngrams
import string
import re
import pickle as pk
def norm(F, prepare=1):
    data = F.lower()
    data = re.sub(r'(.)\1+', r'\1', data)
    data = re.sub("\d+|\"|!|-|\*", "", data)
    data = re.sub(",|[(]|[)]|[.]|[\]]|[\[]|[:]|[;]", " ",data)
    data = data.replace("á", "a")
    data = data.replace("é", "e")
    data = data.replace("í", "i")
    data = data.replace("ó", "o")
    data = data.replace("ú", "u")


    if prepare:
        data = data.replace("v", "w")
        data = data.replace("c", "k")
        data = data.replace("qu", "k")
        data = data.replace("q", "k")
        data = data.replace("ü", "+")
        data = data.replace("j", "h")
        data = data.replace("ts", "ch")
    return data

def token(data):
    tokens = nltk.word_tokenize(data)
    text = nltk.Text(tokens)
    return text

def load():
    F = open("nuevo.txt", "r")
    f = F.read()
    data = norm(f)
    text = token(data)
    return text 

def get_model(text):
    lmodel = {}
    for word in text:
        if len(word) <= 1:
            continue
        word = word.lower()
        bgs = ngrams(word, 4)
        for bg in bgs:
            bg = [bg[0]+bg[1], bg[2]+bg[3]]

            if bg[0] in lmodel.keys():
                if bg[1] in lmodel[bg[0]].keys():
                    lmodel[bg[0]][bg[1]] = lmodel[bg[0]][bg[1]] + 1
                else:
                    lmodel[bg[0]][bg[1]] = 1 

            else:
                lmodel[bg[0]] = {bg[1]:1} 
    for fl in lmodel.keys():
        total=0
        for ll in lmodel[fl].keys():
            total = lmodel[fl][ll] + total

        for ll in lmodel[fl].keys():
            lmodel[fl][ll] =  float(lmodel[fl][ll]) / float(total)
   
    return lmodel

if __name__ == "__main__":
    text = load()
    fdist = nltk.probability.FreqDist(text)
    commont = fdist.most_common(300)
    common = [c[0] for c in commont]
    with open("common.pickle", "wb") as f:
        pk.dump(common, f)

    txt = load()
    lm = get_model(txt)
    print(lm)
    with open("lm.pickle", "wb") as f:
        pk.dump(lm, f)





