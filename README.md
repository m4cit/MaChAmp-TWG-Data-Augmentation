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

**--unimorph0:**  UniMorph Inaccurate verb replacements with regard to transitivity. In place of --unimorph1, --internal, --supertag, or --original  

**--unimorph1:**  UniMorph Accurate verb replacements with regard to transitivity. In place of --unimorph0, --internal, --supertag, or --original.  

**--internal:**  For internal word swapping. In place of --unimorph0, unimorph1, --supertag, or --original.  

**--supertag:**  For internal supertag word swapping. In place of --unimorph0, unimorph1, --internal, or --original.  

**--original:**  Appends the training data by itself without changes. In place of --unimorph0, unimorph1, --internal, or --supertag.  

**-i, --RRGinput:**  (OPTIONAL) Filtered RRG file input. Default file: "rrgparbank/conllu/filtered_acc_en_conllu.conllu".  

**-o, --RRGoutput:**  (OPTIONAL) Filtered RRG file output directory. Default directory: "rrgparbank/conllu".  

**-t, --tag:**  Word tags.  

**-ti, --trainInput:**  (OPTIONAL) train.supertags file input. Default file: "experiments/rrgparbank-en/base/train.supertags".  

**-to, --trainOutput:**  (OPTIONAL) train.supertags file output directory. If the directory is not specified, the default directory is used and filename changes to "new_train.supertags".  

**-s, --extensionSize:**  Extension size of the resulting training file. Must be >= 2. "2" doubles the size (sentences) of the base training file, thus does 1 run through the file (-s input-1).  


# Usage
augment.py [-h] [--unimorph0] [--unimorph1] [--internal] [--supertag] [--original]  
[-i RRGINPUT] [-o RRGOUTPUT] [-t TAG] [-ti TRAININPUT] [-to TRAINOUTPUT] -s EXTENSIONSIZE

