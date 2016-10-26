from __future__ import absolute_import
from __future__ import division, print_function, unicode_literals

from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer as Summarizer
from sumy.summarizers.text_rank import TextRankSummarizer as TextRankSummarizer
from sumy.summarizers.kl import KLSummarizer as KL
from sumy.summarizers.lex_rank import LexRankSummarizer as LRS
from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words
import sumy.evaluation.rouge as Rogue
import seaborn as sns
import matplotlib.pyplot as plt
sns.set_style("white")
import os


LANGUAGE = "english"
SENTENCES_COUNT = 5


if __name__ == "__main__":

    stemmer = Stemmer(LANGUAGE)

    tr = [0.0, 0.0, 0.0]
    lsa = [0.0, 0.0, 0.0]
    kl = [0.0, 0.0, 0.0]
    lrs = [0.0, 0.0, 0.0]

    metrics = [tr, lsa, kl, lrs]

    path = "../text_summarization/output/articles"
    for file in os.listdir(path):
        if file.endswith(".txt"):
            print(file)
            parser = PlaintextParser.from_file(path + file, Tokenizer(LANGUAGE))

            tr_summarizer = TextRankSummarizer(stemmer)
            lsa_summarizer = Summarizer(stemmer)
            kl_summarizer = KL(stemmer)
            lrs_summarizer = LRS(stemmer)
            summarizers = [tr_summarizer, lsa_summarizer, kl_summarizer, lrs_summarizer]

            for summarizer in summarizers:
                summarizer.stop_words = get_stop_words(LANGUAGE)

            tr_summary = []
            lsa_summary = []
            kl_summary = []
            lrs_summary = []
            summaries = [tr_summary, lsa_summary, kl_summary, lrs_summary]
            for i in range(0, len(summarizers), 1):
                for sentence in summarizers[i](parser.document, SENTENCES_COUNT):
                    summaries[i].append(sentence)
                    print(sentence)

                metrics[i][0] += Rogue.rouge_1(summaries[i], parser.document.sentences)
                metrics[i][1] += Rogue.rouge_2(summaries[i], parser.document.sentences)
                metrics[i][2] += Rogue.rouge_n(summaries[i], parser.document.sentences, 3)

    labels = ['TextRank', 'LSA', 'KL', 'LRS']

    plt.figure(1, figsize=(10, 10))
    plt.tick_params(
        axis='x',  # changes apply to the x-axis
        which='both',  # both major and minor ticks are affected
        bottom='off',  # ticks along the bottom edge are off
        top='off',  # ticks along the top edge are off
        labelbottom='off')  # labels along the bottom edge are off
    plt.grid(True)
    for i,metric in enumerate(metrics):
        plt.plot([1,2,3], metric, linewidth=1, label=labels[i])
    plt.axis('tight')
    plt.title('Text summarization quality')
    plt.xlabel('ROUGE')
    plt.ylabel('Score')
    plt.legend()
    plt.savefig('text_summarization_quality.pdf')
