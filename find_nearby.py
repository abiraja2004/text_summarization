#!/bin/python2

import artm
from scipy import stats
import pandas
import preprocess
import argparse
import os
import gensim
import numpy as np
import sys

class Doc_search():
    def __init__(self, store_path, num_of_topics=50):
        self.store_path = store_path
        self.dictionary = artm.Dictionary().load_text(dictionary_path=store_path+'big_dictionary')
        self.model = artm.ARTM(num_topics=num_of_topics, dictionary=self.dictionary, cache_theta=True,
                               theta_columns_naming='title',
                               class_ids={'@abstract': 2, '@title': 3, '@body': 1, '@authors': 2, 'journal_key': 1})
        self.model.regularizers.add(artm.SmoothSparsePhiRegularizer(name='SparsePhi',
                                                                    class_ids=['@abstract', '@title', '@body',
                                                                               '@authors', '@journal_key']))
        self.model.regularizers.add(artm.SmoothSparseThetaRegularizer(name='SparseTheta', tau=-3))
        self.model.regularizers.add(artm.DecorrelatorPhiRegularizer(name='decorrelator_phi', tau=1,
                                                                    class_ids=['@abstract', '@title', '@body',
                                                                               '@authors', '@journal_key']))
        self.model.regularizers.add(artm.ImproveCoherencePhiRegularizer(name='CoherencePhi', tau=1))
        self.model.load(filename=store_path+'saved_p_wt', model_name='p_wt')
        self.model.load(filename=store_path+'saved_n_wt', model_name='n_wt')
        self.theta = pandas.read_csv(store_path+'theta.csv')
        self.col_names = self.theta.columns.values
        with open(store_path+'raw_titles.txt') as f:
            self.titles = f.read().splitlines()

    def load_test_data(self, vw_file):
        self.batch_vectorizer_test = artm.BatchVectorizer(data_path=self.store_path+vw_file,
                                                          data_format='vowpal_wabbit',
                                                          target_folder=self.store_path+'test_batches')
        self.theta_test = self.model.transform(batch_vectorizer=self.batch_vectorizer_test)

    def find_nearby(self, query, doc_file, top_size=5, show_titles=True, distance_type='kl'):
        dists = []
        if distance_type == 'kl':
            for col_num in self.col_names[1:]:
                dists.append(stats.entropy(pk=self.theta_test[query], qk=self.theta[col_num], base=None))
            top_kl = [(self.col_names[i[0]], i[1]) for i in
                      sorted(list(enumerate(dists)), key=lambda x: x[1])[:top_size]]
            if show_titles: self.show_titles(query, doc_file, top_kl, 'kl divergence')
            return top_kl
        elif distance_type == 'cos':
            for col_num in self.col_names[1:]:
                dists.append(gensim.matutils.cossim(self.theta_test[query], self.theta[col_num]))
            top_cos = [(self.col_names[i[0]], i[1]) for i in
                       sorted(list(enumerate(dists)), key=lambda x: x[1], reverse=True)[:top_size]]
            if show_titles: self.show_titles(query, doc_file, top_cos, 'cos distance')
            return top_cos
        elif distance_type == 'hellinger':
            dists = []
            for col_num in self.col_names[1:]:
                dists.append(sum(pow(np.sqrt(self.theta[col_num]) - np.sqrt(self.theta_test[query]), 2)))
            top_he = [(self.col_names[i[0]], i[1]) for i in
                      sorted(list(enumerate(dists)), key=lambda x: x[1])[:top_size]]
            if show_titles: self.show_titles(query, doc_file, top_he, 'hellinger distance')
            return top_he

    def show_titles(self, query, doc_file, close_docs, distance_type='kl divergence'):
        with open(doc_file, 'r') as f:
            doc_name = f.read().splitlines()[0]
        print 'query:', doc_name
        print 'close docs by '+distance_type+':'
        for doc in close_docs:
            print doc, self.titles[int(doc[0][3:])]
        print

if __name__ == '__main__':
    parser = argparse.ArgumentParser(fromfile_prefix_chars='@') # argument_default={}
    parser.add_argument("--model_store_path", type=str, help='path to the model files')
    parser.add_argument("--docs_store_path", type=str, help='path to the folder with aim docs')
    if os.path.isfile('args.txt') and len(sys.argv) == 1:
        args = parser.parse_args(['@args.txt'])
    else:
        args = parser.parse_args()

    print('Loading bigartm model...')
    artm_model = Doc_search(args.model_store_path)

    while True:
        doc_name = raw_input("Enter file doc name: ")
        if os.path.isfile(args.docs_store_path+doc_name):
            preprocess.process_doc(args.docs_store_path, doc_name)
            artm_model.load_test_data('one_temp_doc.vw')
            artm_model.find_nearby(artm_model.theta_test.columns.values[0], args.docs_store_path+doc_name,
                                   distance_type='kl')
        else:
            print('incorrect path(' + args.docs_store_path + ') or filename(' + doc_name + ')')