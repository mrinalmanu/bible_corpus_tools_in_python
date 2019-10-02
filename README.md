# Python code for parsing XML files, this is a part of Bible Corpus Tools

```{<!-- language: lang-none -->}
  /***
  *    ______._._....._........_____.............................._____..........._.....
  *    |.___.(_|.|...|.|....../..__.\............................|_..._|.........|.|....
  *    |.|_/./_|.|__.|.|.___..|./..\/.___.._.__._.__.._..._.___....|.|.___...___.|.|___.
  *    |.___.|.|.'_.\|.|/._.\.|.|..../._.\|.'__|.'_.\|.|.|./.__|...|.|/._.\./._.\|./.__|
  *    |.|_/.|.|.|_).|.|..__/.|.\__/|.(_).|.|..|.|_).|.|_|.\__.\...|.|.(_).|.(_).|.\__.\
  *    \____/|_|_.__/|_|\___|..\____/\___/|_|..|..__/.\__,_|___/...\_/\___/.\___/|_|___/
  *    ........................................|.|......................................
  *    ........................................|_|......................................
  */
```

Author: **Mrinal Vashisth; mrinalmanu10@gmail.com**

It's my personal fun project :))

This is a set of functions for processing text for language processing, from XML files in Open Bible Data mentioned in the paper **A massively parallel corpus: the Bible in 100 languages**, Christos Christodouloupoulos and Mark Steedman.
(https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4551210/)

Get data here: 
**https://github.com/christos-c/bible-corpus**

Description:

**bcp.py** contains functions to convert XML files into text files or CSV files. For whatever purpose.
For the sake of language processing CSV files are more informative and give output as a pandas dataframe with:

[verse_id]  [text] [book] [name] [chapter] [verse_number]


```{<!-- language: lang-none -->}

Next step is to take the CSV and optimize data to lose minimum information and get the text of New Testament (NT) up and ready for analysis.
```

```{<!-- language: lang-none -->}

Final update:

I took the data and tried to find out which verses are shared across the most languages.

Then I took the epitran package and converted these verses into IPA annotation.

Using multiprocessing, and the dreadful rowwise operation on pandas dataframe, it took 4 hours with 7 CPUs to to process about 121,000 lines.

The final database contains 121,000 lines from 30 langauges.

I may in future figure out a way of using this dataframe.

The dataframe annotation_features.csv, includes details about the phonemes, and their annotation.

Final dataset link here: 

https://www.kaggle.com/mrinalmanu/bible-verses-30-languages-ipa-annotated
```
