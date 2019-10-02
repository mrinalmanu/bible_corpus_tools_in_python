#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep 22 17:20:57 2019

@author: mrinalmanu
"""

# Read CSV's and combine into a single dataframe 

import pandas as pd 
import os
import re
import pymysql
import sys
import string
import itertools
import seaborn as sns
import numpy as np


def get_all_csv_list(path):
    
    """Get all CSVs files in the specified path/ folder """
    files = []
    # r=root, d=directories, f = files
    for r, d, f in os.walk(path):
        for file in f:
            '''This is where it will sieve off PART files'''
            if not 'PART.txt.csv' in file:
                files.append(os.path.join(r, file))
    
    samples = [l.split(path+'/') for l in ''.join(files).split(path+'/')]
    """remove 1st element from sample_names as it is an empty list"""
    samples.pop(0)
    sample_names = []
    j = 0
    for j in range(0, len(samples)): 
        sample_names.append([re.sub('.txt', '', i) for i in samples[j]])
        j+1
        
    def repack(lst): 
        res = [] 
        for el in lst: 
            sub = el.split(', ') 
            res.append(sub) 
        return(res) 
    
    return repack(files), sample_names


def csvs_to_flat_df(files, sample_names):
    
    """Get all csvs and convert into a big flattened dataframe """
    mass_df = []
    i = 0
    for i in range(0, len(files)):
        for item in files[i]:
            for sample in sample_names[i]:
                mass_df.append(pd.read_csv(item))
                i = i+1
    lens = []
    for elem in mass_df:
        lens.append(len(elem))
        
    samples = pd.DataFrame(sample_names)
    samples = samples[0].str.replace('.csv', '')
    samples = pd.DataFrame(samples)
    samples['numero'] = samples.index
    samples = samples[0].str.replace('-NT', '')
    samples = pd.DataFrame(samples)
    
    my_sample_list = []
    for item in samples[0]:
        my_sample_list.append(item)
      
    ann = list(itertools.chain(*(itertools.repeat(elem, n) for elem, n in zip(my_sample_list, lens))))
    big_df = pd.concat(mass_df)
    big_df['langauge'] = (pd.DataFrame(ann))[0].values
    
    big_df = big_df.drop(big_df.columns[0],axis=1)
    big_df = big_df.drop(big_df.columns[2],axis=1)
    
    return big_df

def get_the_best_out_of_data(big_df, sample_names):
    
    """Preparing the dataset """
    
    count = pd.DataFrame(big_df['verse_id'].value_counts())
    
    dist_len = []
    for i in range(0, len(sample_names)+1):
        what_len = i
        omni_rows = count[count.verse_id == what_len]
        dist_len.append(len(omni_rows))
    
    sns.set_style('whitegrid') 
    sns.distplot(dist_len, kde = False, color ='red', bins = len(sample_names)) 

    
    
    what_len = len(sample_names)
    omni_rows = count[count.verse_id == what_len]
    omni_rows = omni_rows.rename(columns={'verse_id':'counts'})
    omni_rows['verse_id'] = omni_rows.index
    
    
    print("We used {} samples giving us {} lines common across samples matched by verse ids.".format(what_len, len(omni_rows)))
    new_df = pd.merge(big_df, omni_rows, how='inner', on=['verse_id'])

    return new_df

def save_df(final_df, path):
    final_df.to_pickle('{}'.format(path))
    print("dataframe saved as .pkl file at {}".format(path))

def main():
    path = '/home/mrinalmanu/Documents/corpuses/bible-corpus-1.2.1/csv_output'
    files, sample_names = get_all_csv_list(path)
    
    big_df = csvs_to_flat_df(files, sample_names)
    mass_df =  get_the_best_out_of_data(big_df, sample_names)
    
    save_df(mass_df, '/home/mrinalmanu/Documents/corpuses/bible-corpus-1.2.1/final_DF.pkl')

    
    # we take verses that are present in atleast 100% of the samples
    
    
main()    
