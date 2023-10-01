# MaChAmp-TWG_Data-Augmentation
Data Augmentation for the parser MaChAmp-TWG

# Requirements
- Python 3.6 or newer
- modules from the requirements.txt file

# Installation
```
pip install -r requirements.txt
```

# Options
**-h, --help**  

**--unimorph0:**  _UniMorph Inaccurate verb replacements with regard to transitivity. In place of --unimorph1, --internal, --supertag, or --original._  

**--unimorph1:**  _UniMorph Accurate verb replacements with regard to transitivity. In place of --unimorph0, --internal, --supertag, or --original._  

**--internal:**  _For internal word swapping. In place of --unimorph0, unimorph1, --supertag, or --original._  

**--supertag:**  _For internal supertag word swapping. In place of --unimorph0, unimorph1, --internal, or --original._  

**--original:**  _Appends the training data by itself without changes. In place of --unimorph0, unimorph1, --internal, or --supertag._  

**-i, --RRGinput:**  _(OPTIONAL) Filtered RRG file input. Default file: "rrgparbank/conllu/filtered_acc_en_conllu.conllu"._  

**-o, --RRGoutput:**  _(OPTIONAL) Filtered RRG file output directory. Default directory: "rrgparbank/conllu"._  

**-t, --tag:**  _Word tags._  

**-ti, --trainInput:**  _(OPTIONAL) train.supertags file input. Default file: "experiments/rrgparbank-en/base/train.supertags"._  

**-to, --trainOutput:**  _(OPTIONAL) train.supertags file output directory. If the directory is not specified, the default directory is used and filename changes to "new_train.supertags"._  

**-s, --extensionSize:**  _Extension size of the resulting training file. Must be >= 2. "2" doubles the size (sentences) of the base training file, thus does 1 run through the file (-s input-1)._  

# Available tags for replacement task
**nS:**  _Noun Singular_  
**nP:**  _Noun Plural_  

**aPoss:**  _Adjective Possessive_  
**aCmpr:**  _Adjective Comparative_  
**aSup:**  _Adjective Superlative_  

**vPst:**  _Verb Past Tense_  
**vPresPart:**  _Verb Present Tense, Participle Form_  
**vPstPart:**  _Verb Past Tense, Participle Form_  

**adv (for internal dataswap only):**  _Adverb_  
**advInt (for internal dataswap only):**  _Adverb, Pronominal type: Interrogative_  
**advSup (for internal dataswap only):**  _Adverb Superlative_  
**advCmpr (for internal dataswap only):**  _Adverb Comparative_  

**noun:**  _All nouns_  

**adj:**  _All adjectives_  

**verb:**  _All verbs_  

**all:**  _All available tags_

# Usage
augment.py [-h] [--unimorph0] [--unimorph1] [--internal] [--supertag] [--original]  
[-i RRGINPUT] [-o RRGOUTPUT] [-t TAG] [-ti TRAININPUT] [-to TRAINOUTPUT] -s EXTENSIONSIZE

