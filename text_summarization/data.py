import pandas
import ftfy
import re
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords


def process(data, name, save=True):
    path = '/home/vladimir/Documents/PyCharmScripts/text_summarization/output/'
    print('work with', name)
    print('ftfy stage')
    tmp = [ftfy.fix_text(i, normalization='NFKC') for i in data]
    print('regexp stage')
    tmp = [re.sub('-', '', s) for s in tmp]
    tmp = [re.sub(r'''[^0-9a-zA-Z.]+''', ' ', s) for s in tmp]
    tmp = [re.sub(' [0-9]+', ' ', s) for s in tmp]
    tmp = [re.sub(r' [a-zA-Z] ', ' ', s) for s in tmp]
    tmp = [re.sub(r' [ ]+', ' ', s) for s in tmp]
    stop = set(stopwords.words('english'))
    ans = ['' for i in tmp]
    c = -1
    wnl = WordNetLemmatizer()
    print('stopwords and WordNetLemmatizer stage')
    for t in tmp:
        c += 1
        if c % 3000 == 0:
            print(c)
        for w in t.split(' '):
            if w != '':
                w = w.lower()
                if w not in stop:
                    ans[c] += wnl.lemmatize(w) + ' '

    if save:
        print('save stage')
        with open(path + name + ".txt", 'w') as f:
            for text in ans:
                f.write(text + '\n')
            f.close()

    return ans


def articles(start, stop):
    data = pandas.read_csv(
        "/home/vladimir/Documents/PyCharmScripts/text_summarization/input/no_spec_topic_articles.csv",
        encoding='ISO-8859-1')

    # process bodies
    bodies = data['body'].iloc[start:stop]
    pattern_delim = re.compile(r'\[.+?\]')
    texts = [pattern_delim.sub('', i) for i in bodies]
    pattern_delim = re.compile(r'\(.+?\)')
    texts = [pattern_delim.sub('', i) for i in texts]
    ans = process(data=texts, name='bodies'+str(stop/1000), save=True)

for i in range(1, 20):
    print i
    start = i*1000
    stop = start + 1000
    articles(start, stop)