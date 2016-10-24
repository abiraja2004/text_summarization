# import logging
from gensim.summarization import summarize
from gensim.summarization import keywords

path = '/home/vladimir/Documents/PyCharmScripts/text_summarization/output/'


def sum(index):
    # logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

    bodies = []
    f = open(path + 'articles/bodies' + str(index) + '.txt', 'r')
    for line in f:
        bodies.append(line)

    f_summary = open(path + 'summary/summary' + str(index) + '.txt', 'w')
    f_words = open(path + 'keywords/keywords' + str(index) + '.txt', 'w')
    summary = []
    most_value_words = []

    c = -1
    for article in bodies:
        c += 1
        if c % 100 == 0:
            print 'step is ' + str(c)
        # summarization
        summary.append(summarize(article, ratio=0.1))
        # key words from article
        most_value_words.append(keywords(article, words=10))

    for s in summary:
        s = s.replace('\n', ' ')
        f_summary.write(s + '\n')

    for word in most_value_words:
        word = word.replace('\n', ' ')
        f_words.write(word + '\n')

    f.close()
    f_summary.close()
    f_words.close()
    bodies = None
    summary = None
    most_value_words = None


for i in range(1, 21):
    print 'Number of file ' + str(i)
    sum(i)
