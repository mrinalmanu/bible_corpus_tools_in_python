#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep 28 19:29:48 2019

@author: mrinalmanu
"""

import epitran
import pandas as pd
import ast
import progressbar
import time
from time import sleep
import multiprocessing
from multiprocessing import Manager
import itertools



def process_data_for_model(big_df, lang_pairs):
    
    """ Performs some cleaning to the data and prepares for IPA transcription """
    big_df = big_df.rename(columns={'langauge':'language'})
    big_df['verse_text'] = big_df['verse_text'].replace("'",'', regex=True)

    lang_pairs = lang_pairs.drop(lang_pairs.columns[1],axis=1)
    lang_pairs = lang_pairs.rename(columns={'Lang_in_bible':'language'})
    
    epi_tran_models = []
    for item in lang_pairs['Code']:
        model = 'epitran.Epitran({}{}{})'.format("'",item,"'")
        epi_tran_models.append(model)
        
    
    lang_pairs['model'] = epi_tran_models
    
    curated_df = pd.merge(big_df, lang_pairs, how='inner', on=['language'])
    
    curated_df = curated_df.replace('\n','', regex=True)
    curated_df = curated_df.replace('\t','', regex=True)

    curated_df = curated_df.drop(curated_df.columns[2],axis=1)
    curated_df = curated_df.drop(curated_df.columns[2],axis=1)
    curated_df = curated_df.drop(curated_df.columns[2],axis=1)
    curated_df = curated_df.drop(curated_df.columns[3],axis=1)
    curated_df = curated_df.drop(curated_df.columns[3],axis=1)
    
    return curated_df


def main():

    lang_pairs = pd.read_csv('/home/mrinalmanu/Documents/corpuses/bible-corpus-1.2.1/supported_lang_epitran', sep='\t')
    lang_pairs = lang_pairs.dropna()
    cedict = '/home/mrinalmanu/Documents/corpuses/bible-corpus-1.2.1/cedict_1_0_ts_utf-8_mdbg/cedict_ts.u8'
    cedict_file = cedict

    big_df = pd.read_pickle('/home/mrinalmanu/Documents/corpuses/bible-corpus-1.2.1/final_DF.pkl')
    
    curated_df = process_data_for_model(big_df, lang_pairs)  
    curated_df['model'] = curated_df['model'].replace("epitran.Epitran('cmn-Hant')", "epitran.Epitran('cmn-Hant', cedict_file='{}')".format(cedict_file), regex=False)

    # sample
    # curated_df = curated_df.sample(100)
    
    """ Creating a new data frame by combining the 'model' column with 'verse_text'"""

    """ Output will be stored as another df"""     
    # curated_df = curated_df.sample(1000)

    bar = progressbar.ProgressBar(maxval=20, \
    widgets=[progressbar.Bar('█', '[', ']'), ' ', progressbar.Percentage()])
    
    # create as many processes as there are CPUs on your machine
    num_processes = multiprocessing.cpu_count()
    chunk_size = 20
    chunks = [curated_df.ix[curated_df.index[i:i + chunk_size]] for i in range(0, curated_df.shape[0], chunk_size)]

    def give_me_ipa(chunk):
        """ Function that runs on a given row to return IPA string"""
        print('I am processing from row number {}'.format(chunk.index[0]))
        
        dict_of_languages = {k: v for k, v in chunk.groupby('verse_text')}
    
        new_key = []
        
        for key, value in dict_of_languages.items():
            new_key.append(value)
        
        x = []
        bar.start()
        
        for mini_df in new_key:
            for item in mini_df.values:
                text = item[1]
                model = item[3]
                verse_id = item[0]
                lang = item[2]
                ipa_s = eval("{}.transliterate(u'{}')".format(model, text))
                x.append([verse_id, lang, text, ipa_s])

        bar.finish() 
        
        return x
    
    # create our pool with `num_processes` processes
    pool = multiprocessing.Pool(processes=7) 
    ####
    ## Install flite for correct functioning for English language
    ####
    y = pool.map(give_me_ipa, chunks)
    
    merged = list(itertools.chain.from_iterable(y))
    
    ipa_command_df = pd.DataFrame(merged)

    

    
    ipa_command_df.to_pickle('/home/mrinalmanu/Documents/corpuses/bible-corpus-1.2.1/IPA_DF.pkl')
    print("dataframe saved as .pkl file at '/home/mrinalmanu/Documents/corpuses/bible-corpus-1.2.1/IPA_DF.pkl")
    
    
    
main()
