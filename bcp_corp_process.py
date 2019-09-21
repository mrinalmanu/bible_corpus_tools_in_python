#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep 21 18:03:13 2019

@author: mrinalmanu
"""

# Python code for parsing XML files


from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
import pandas as pd 
from pandas.io.json import json_normalize
import string
import os
import itertools
import re


def get_corpus_list(path):
    files = []
    # r=root, d=directories, f = files
    for r, d, f in os.walk(path):
        for file in f:
            if '.xml' in file:
                files.append(os.path.join(r, file))
    
    samples = [l.split(path+'/') for l in ''.join(files).split(path+'/')]
    """remove 1st element from sample_names as it is an empty list"""
    samples.pop(0)
    sample_names = []
    j = 0
    for j in range(0, len(samples)): 
        sample_names.append([re.sub('.xml', '.txt', i) for i in samples[j]])
        j+1
        
    def repack(lst): 
        res = [] 
        for el in lst: 
            sub = el.split(', ') 
            res.append(sub) 
        return(res) 
    
    return repack(files), sample_names

   
def process_corpus_file(file):
        
    infile = open(file,"r")
    contents = infile.read()
    soup = BeautifulSoup(contents,'lxml')

    # Extract all of the <a> tags:    

    # Extract all of the <a> tags:    
    tags = soup.find_all('seg')

    corpus = []

    for item in tags:
        text = item.text
        corpus.append(text)
        
    return corpus


def generate_text_files(output_path, files, sample_names):
    """Generate individual text corpus files"""
    for i in range(0, len(files)):
        for item in files[i]:
            for name in sample_names[i]:
                corpus = process_corpus_file(item)
                with open(output_path+name, 'a+') as f:
                    f.writelines(["%s\n" % item  for item in corpus])
                    f.close()
                    
                    
def parse_xml_get_df(file_input):
    tree = ET.parse(file_input)
    root = tree.getroot()

    df_cols = ["verse_id", "verse_text"]
    rows = []
    
    for node in root.iter('seg'):
        verse_id = node.attrib
        verse_text = node.text
        rows.append({"verse_id": verse_id, "verse_text": verse_text})
 
    df = pd.DataFrame(rows, columns = df_cols)
    df2 = json_normalize(df['verse_id'])
    df['verse_id'] = df2['id']
    # splitting the id column for better retrieval of entries
    df['book'], df['name'], df['chapter'], df['verse'] = df['verse_id'].str.split('.', 3).str

    return df
                    
                
def g_ann_csv_files(output_path, files, sample_names):
    "Generate annotated csv files from the input files"
    for i in range(0, len(files)):
        for item in files[i]:
            for name in sample_names[i]:
                parse_xml_get_df(item).to_csv(r'{}{}.csv'.format(output_path, name))


def main():
    path = '/home/mrinalmanu/Documents/corpuses/bible-corpus-1.2.1/bibles'
    files, sample_names = get_corpus_list(path)
    
    output_path = '/home/mrinalmanu/Documents/corpuses/bible-corpus-1.2.1/output/'
   # generate_text_files(output_path, files, sample_names)
    
    csv_output_path = '/home/mrinalmanu/Documents/corpuses/bible-corpus-1.2.1/csv_output/'
    g_ann_csv_files(csv_output_path, files, sample_names)
    

main()