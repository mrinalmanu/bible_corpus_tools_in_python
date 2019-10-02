#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct  2 22:27:29 2019

@author: mrinalmanu
"""
import pandas as pd
import phonemeviewer
import json
from pandas.io.json import json_normalize
import sklearn
from sklearn.cluster import KMeans
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


def main():
    ipa_df_path = '/home/mrinalmanu/Documents/corpuses/bible-corpus-1.2.1/IPA_DF.pkl'
    ipa_df = pd.read_pickle(ipa_df_path)
    json_phonemes = '/home/mrinalmanu/Documents/corpuses/bible-corpus-1.2.1/phonemes-master/phonemes.json'


    with open(json_phonemes, 'r') as f:
        phonemes_df = pd.read_json(f, orient='index')
        f.close()
    
    phonemes_df['phoneme'] = phonemes_df.index
    add_df = pd.read_csv('/home/mrinalmanu/Documents/corpuses/bible-corpus-1.2.1/feature_DF.csv')
    
    add_df.reset_index(drop=True, inplace=True)
    phonemes_df.reset_index(drop=True, inplace=True)  
    
    phonemes_df = phonemes_df.drop(phonemes_df.columns[0],axis=1)
    
    feature_df = pd.concat([phonemes_df, add_df], axis=1)
    feature_df = feature_df.drop(feature_df.columns[2], axis=1)
    
    
    feature_df.to_csv('/home/mrinalmanu/Documents/corpuses/bible-corpus-1.2.1/annotated_feature_DF.csv')
    
    
    
main()    