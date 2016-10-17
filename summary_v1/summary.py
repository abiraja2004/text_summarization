from __future__ import absolute_import
from __future__ import division, print_function, unicode_literals

from sumy.parsers.html import HtmlParser
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer as Summarizer
from sumy.summarizers.text_rank import TextRankSummarizer as TextRankSummarizer
from sumy.summarizers.kl import KLSummarizer as KL
from sumy.summarizers.lex_rank import LexRankSummarizer as LRS
from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words
import sumy.evaluation.rouge as Rogue
import sumy.evaluation.coselection as Coselection


LANGUAGE = "english"
SENTENCES_COUNT = 5


if __name__ == "__main__":
    #nltk.download()
    #url = "http://www.zsstritezuct.estranky.cz/clanky/predmety/cteni/jak-naucit-dite-spravne-cist.html"
    #parser = HtmlParser.from_url(url, Tokenizer(LANGUAGE))
    # or for plain text files
    parser = PlaintextParser.from_file("g.txt", Tokenizer(LANGUAGE))
    stemmer = Stemmer(LANGUAGE)

    #summarizer = Summarizer(stemmer)
    print("Text rank:")
    summarizer = TextRankSummarizer(stemmer)
    summarizer.stop_words = get_stop_words(LANGUAGE)

    summary = []
    for sentence in summarizer(parser.document, SENTENCES_COUNT):
        summary.append(sentence)
        print(sentence)

    print("ROGUE 1: " + str(Rogue.rouge_1(summary, parser.document.sentences)))
    print("ROGUE 2: " + str(Rogue.rouge_2(summary, parser.document.sentences)))
    print("ROGUE 3: " + str(Rogue.rouge_n(summary, parser.document.sentences,3)))
    #print("Recall: " + str(Coselection.recall(summary, parser.document.sentences)))
    #print("Precision: " + str(Coselection.precision(summary, parser.document.sentences)))
    #print("F-score: " + str(Coselection.f_score(summary, parser.document.sentences, 0.5)))


    print("=============================================================")
    print("LSA:")
    summarizer = Summarizer(stemmer)
    summarizer.stop_words = get_stop_words(LANGUAGE)

    summary = []
    for sentence in summarizer(parser.document, SENTENCES_COUNT):
        summary.append(sentence)
        print(sentence)

    print("ROGUE 1: " + str(Rogue.rouge_1(summary, parser.document.sentences)))
    print("ROGUE 2: " + str(Rogue.rouge_2(summary, parser.document.sentences)))
    print("ROGUE 3: " + str(Rogue.rouge_n(summary, parser.document.sentences,3)))
    #print("Recall: " + str(Coselection.recall(summary, parser.document.sentences)))
    #print("Precision: " + str(Coselection.precision(summary, parser.document.sentences)))
    #print("F-score: " + str(Coselection.f_score(summary, parser.document.sentences, 0.5)))

    print("=============================================================")
    print("KL:")
    summarizer = KL(stemmer)
    summarizer.stop_words = get_stop_words(LANGUAGE)

    summary = []
    for sentence in summarizer(parser.document, SENTENCES_COUNT):
        summary.append(sentence)
        print(sentence)

    print("ROGUE 1: " + str(Rogue.rouge_1(summary, parser.document.sentences)))
    print("ROGUE 2: " + str(Rogue.rouge_2(summary, parser.document.sentences)))
    print("ROGUE 3: " + str(Rogue.rouge_n(summary, parser.document.sentences,3)))

    print("=============================================================")
    print("LexRank Summary:")
    summarizer = LRS(stemmer)
    summarizer.stop_words = get_stop_words(LANGUAGE)

    summary = []
    for sentence in summarizer(parser.document, SENTENCES_COUNT):
        summary.append(sentence)
        print(sentence)

    print("ROGUE 1: " + str(Rogue.rouge_1(summary, parser.document.sentences)))
    print("ROGUE 2: " + str(Rogue.rouge_2(summary, parser.document.sentences)))
    print("ROGUE 3: " + str(Rogue.rouge_n(summary, parser.document.sentences,3)))

