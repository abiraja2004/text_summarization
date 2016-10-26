#!/bin/python2
import pickle
import codecs
#import ftfy
import re
from collections import Counter
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
import sys

def process_doc(path_to_doc, doc_name):
    # title authors abstract body journal_key
    f = codecs.open(path_to_doc+doc_name, "r", "utf-8")
    doc = f.read().splitlines()
    f.close()
    preprocessed_doc = {'ti': process_data([doc[0]]),
                'au': process_authors([doc[1]]),
                'ab': process_data([doc[2]]),
                'bo': process_data([doc[3]]),
                'jk': [doc[4]]}
    save_in_vw_format(path_to_doc, preprocessed_doc)

def process_data(data):
    # tmp = [ftfy.fix_text(i, normalization='NFKC') for i in data]
    tmp = [re.sub('-', '', s) for s in data]
    tmp = [re.sub(r'''[^0-9a-zA-Z]+''', ' ', s) for s in tmp]
    tmp = [re.sub(' [0-9]+', ' ', s) for s in tmp]
    tmp = [re.sub(r' [a-zA-Z] ', ' ', s) for s in tmp]
    tmp = [re.sub(r' [ ]+', ' ', s) for s in tmp]
    stop = set(stopwords.words('english'))
    ans = ['' for i in tmp]
    c = -1
    wnl = WordNetLemmatizer()
    for t in tmp:
        c +=1
        for w in t.split(' '):
            if w != '':
                w = w.lower()
                if w not in stop:
                    ans[c] += wnl.lemmatize(w)+' '
    return ans

def process_authors(data):
    authors = [re.sub('[^0-9a-zA-Z ;]+', '', str(s)) for s in data]
    authors = [i.lower().split('; ') for i in authors]
    authors = [' '.join([au.replace(' ', '_') for au in au_text]) for au_text in authors]
    return authors

def save_in_vw_format(path_to_doc, data):
    counts = {'ab': [], 'au': [], 'ti': [], 'bo': [], 'jk': []}

    for key in counts.keys():
        temp = data[key]
        temp_c = ["" for i in range(len(temp))]
        for i in range(len(temp)):
            temp_c[i] = ' '.join([j[0] + u":" + str(j[1]) for j in Counter(temp[i][:-1].split(' ')).items()])
        counts[key] = temp_c[:]

    data = []
    data.append(u'doc' + unicode(-1)
                + u' |@abstract ' + counts['ab'][0]
                + u' |@title ' + counts['ti'][0]
                + u' |@authors ' + counts['au'][0]
                + u' |@body ' + counts['bo'][0]
                + u' |@journal_key ' + counts['jk'][0]
                + '\n')

    f = codecs.open(path_to_doc+"one_temp_doc.vw", "w", "utf-8")
    for text in [i.replace(':1', '') for i in data]:
        f.write(text)
    f.close()

if __name__ == '__main__':
    process_doc('C:\Users\Dmitry\Documents\\', 'doc12978.txt')