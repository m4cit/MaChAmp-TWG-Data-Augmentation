# /////////////// Replaces words in the RRG conllu file with randomly chosen ones from the Unimorph file

import csv
import random
import re
import argparse
import os
import time
from tqdm import tqdm

tags = ['aPoss', 'nS', 'nP', 'all', 'aCmpr', 'aSup', 
            'vPst', 'vPres3S', 'vPresPart', 'vPstPart', 'noun', 'verb', 'adj',
            'adv', 'advInt', 'advSup', 'advCmpr']

# //////////////////////////////////
class color:
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'
# //////////////////////////////////

# ///////////////////////////////////////////////
def sentLengths(linesList, emptyList):
    try:
        for i in range(len(linesList)):
            if len(linesList[i]) == 0:    
                count = linesList[i-1][0]
                emptyList.append(count)
            i += 1
        #print(emptyList)      
    except(IndexError):
        i += 1  
# ///////////////////////////////////////////////

# ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
def info():
    print('\nTags:\n')
    print('nS:  Noun Singular\nnP:  Noun Plural\n')
    print('aPoss:  Adjective Possessive\naCmpr:  Adjective Comparative\naSup:  Adjective Superlative\n')
    print('vPst:  Verb Past Tense\nvPresPart:  Verb Present Tense, Participle Form\nvPstPart:  Verb Past Tense, Participle Form\n')
    print('adv (for internal dataswap only):  Adverb\nadvInt (for internal dataswap only):  Adverb, Pronominal type: Interrogative\nadvSup (for internal dataswap only):  Adverb Superlative\nadvCmpr (for internal dataswap only):  Adverb Comparative\n')
    print('noun:  All nouns\n')
    print('adj:  All adjectives\n')
    print('verb:  All verbs\n')
    print('all:  All available tags\n')
# ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

# ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////  
def appendListsDef(lineU, listname, stringToMatch1, stringToMatch2):
    for i in range(len(lineU)):
        if re.match(r'[A-Za-z][^0-9]', lineU[i][0]):
            if lineU[i][2] == stringToMatch1 and lineU[i][3] == stringToMatch2:
                listname.append(lineU[i])
                i += 1
# ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////  
def appendListsDefIntern(lineRRG, listname, stringToMatch1, stringToMatch2):
    for i in range(len(lineRRG)):
        if lineRRG[i][3] == stringToMatch1 and lineRRG[i][5] == stringToMatch2:
            listname.append(lineRRG[i])
            i += 1
# ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////                  
def appendListsIndef(lineU, listname, stringToMatch, substring1, substring2, substring3):
    for i in range(len(lineU)):
        if re.match(r'[A-Za-z][^0-9]', lineU[i][0]):
            if lineU[i][2] == stringToMatch and substring1 in lineU[i][3] and substring2 in lineU[i][3] and substring3 in lineU[i][3]:
                listname.append(lineU[i])
                i += 1         
# ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////                  
def appendListsIntrans(lineU, listname, stringToMatch, substring1, substring2, substring3):
    for i in range(len(lineU)):
        if re.match(r'[A-Za-z][^0-9]', lineU[i][0]):
            if lineU[i][2] == stringToMatch and substring1 in lineU[i][3] and substring2 in lineU[i][3] and substring3 in lineU[i][3] and '|intransitive' in lineU[i][3]:
                listname.append(lineU[i])
                i += 1
# ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////                  
def appendListsTrans(lineU, listname, stringToMatch, substring1, substring2, substring3):
    for i in range(len(lineU)):
        if re.match(r'[A-Za-z][^0-9]', lineU[i][0]):
            if lineU[i][2] == stringToMatch and substring1 in lineU[i][3] and substring2 in lineU[i][3] and substring3 in lineU[i][3] and ('|transitive' in lineU[i][3] or ' transitive' in lineU[i][3]):
                listname.append(lineU[i])
                i += 1
# ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////   
def appendListsIntransIntern(lineRRG, listname, stringToMatch, substring1, substring2, substring3):
    for i in range(len(lineRRG)):
        if lineRRG[i][3] == stringToMatch and substring1 in lineRRG[i][5] and substring2 in lineRRG[i][5] and substring3 in lineRRG[i][5] and lineRRG[i][9] == '_':
            listname.append(lineRRG[i])
            i += 1
# ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////                  
def appendListsTransIntern(lineRRG, listname, stringToMatch, substring1, substring2, substring3):
    for i in range(len(lineRRG)):
        if lineRRG[i][3] == stringToMatch and substring1 in lineRRG[i][5] and substring2 in lineRRG[i][5] and substring3 in lineRRG[i][5] and 'transitive' in lineRRG[i][9]:
            listname.append(lineRRG[i])
            i += 1
# ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////   

# ///////////////////////////////////////////////////////
def remOdd(mylist):
    for i in range(len(mylist)):
        if '&' in mylist[i][0] or '#' in mylist[i][0]:
            mylist[i].pop()
# ///////////////////////////////////////////////////////

# ////////////////////////////////////////////////////////////////////////////////////////////////////////////
def lG(L_nS, L_nP, L_aPoss, L_aCmpr, L_aSup, L_vPst, L_vInf, L_vPresPart, L_vPstPart):
    print('\n1. Reading Unimorph file into a list...')
    print('2. Creating sub-lists from Unimorph data...')
    progressbar = tqdm(total=5)
    
    with open('./unimorph/acc_to_conllu_eng.txt', 'r', encoding='UTF-8', newline='\n') as infileUNI:
        readerUNI = csv.reader(infileUNI, delimiter='\t')
        linesUNI = list(readerUNI)
        progressbar.update()
        
        appendListsDef(linesUNI, L_nS, 'NOUN', 'Number=Sing')
        appendListsDef(linesUNI, L_nP, 'NOUN', 'Number=Plur')
        appendListsDef(linesUNI, L_aPoss, 'ADJ', 'Degree=Pos')
        appendListsDef(linesUNI, L_aCmpr, 'ADJ', 'Degree=Cmp')
        appendListsDef(linesUNI, L_aSup, 'ADJ', 'Degree=Sup')
        progressbar.update()
        
        appendListsIndef(linesUNI, L_vPst, 'VERB', 'Tense=Past', 'VerbForm=Fin','VerbForm=Fin')
        appendListsIndef(linesUNI, L_vInf, 'VERB', 'VerbForm=Inf', 'VerbForm=Inf', 'VerbForm=Inf')
        appendListsIndef(linesUNI, L_vPresPart, 'VERB', 'Tense=Pres', 'VerbForm=Part', 'VerbForm=Part') 
        appendListsIndef(linesUNI, L_vPstPart, 'VERB', 'Tense=Past', 'VerbForm=Part', 'VerbForm=Part') 
        progressbar.update()

        remOdd(L_nS)
        remOdd(L_nP)
        remOdd(L_aPoss)
        remOdd(L_aCmpr)
        remOdd(L_aSup)
        progressbar.update()

        remOdd(L_vPst)
        remOdd(L_vInf)
        remOdd(L_vPresPart)
        remOdd(L_vPstPart)
        progressbar.update()
        progressbar.close()
# ////////////////////////////////////////////////////////////////////////////////////////////////////////////

# ////////////////////////////////////////////////////////////////////////////////////////////////////////////
def lGacc(L_nS, L_nP, L_aPoss, L_aCmpr, L_aSup, L_vPst, L_vInf, L_vPresPart, L_vPstPart, L_vPstIntr, L_vInfIntr, L_vPresPartIntr, L_vPstPartIntr):
    print('\n1. Reading Unimorph file into a list...')
    print('2. Creating sub-lists from Unimorph data...')
    progressbar = tqdm(total=6)
    
    with open('./unimorph/acc_to_conllu_eng.txt', 'r', encoding='UTF-8', newline='\n') as infileUNI:
        readerUNI = csv.reader(infileUNI, delimiter='\t')
        linesUNI = list(readerUNI)
        progressbar.update()
        
        appendListsDef(linesUNI, L_nS, 'NOUN', 'Number=Sing')
        appendListsDef(linesUNI, L_nP, 'NOUN', 'Number=Plur')
        appendListsDef(linesUNI, L_aPoss, 'ADJ', 'Degree=Pos')
        appendListsDef(linesUNI, L_aCmpr, 'ADJ', 'Degree=Cmp')
        appendListsDef(linesUNI, L_aSup, 'ADJ', 'Degree=Sup')
        progressbar.update()
        
        # /// transitives
        appendListsTrans(linesUNI, L_vPstPart, 'VERB', 'Tense=Past', 'VerbForm=Part', 'VerbForm=Part')
        appendListsTrans(linesUNI, L_vPresPart, 'VERB', 'Tense=Pres', 'VerbForm=Part', 'VerbForm=Part')
        appendListsTrans(linesUNI, L_vInf, 'VERB', 'VerbForm=Inf', 'VerbForm=Inf', 'VerbForm=Inf')
        appendListsTrans(linesUNI, L_vPst, 'VERB', 'Tense=Past', 'VerbForm=Fin', 'VerbForm=Fin')
        progressbar.update()
        
        # /// intransitives
        appendListsIntrans(linesUNI, L_vPstPartIntr, 'VERB', 'Tense=Past', 'VerbForm=Part', 'VerbForm=Part')
        appendListsIntrans(linesUNI, L_vPresPartIntr, 'VERB', 'Tense=Pres', 'VerbForm=Part', 'VerbForm=Part')
        appendListsIntrans(linesUNI, L_vInfIntr, 'VERB', 'VerbForm=Inf', 'VerbForm=Inf', 'VerbForm=Inf')
        appendListsIntrans(linesUNI, L_vPstIntr, 'VERB', 'Tense=Past', 'VerbForm=Fin', 'VerbForm=Fin')
        progressbar.update()
        
        remOdd(L_nS)
        remOdd(L_nP)
        remOdd(L_aPoss)
        remOdd(L_aCmpr)
        remOdd(L_aSup)
        progressbar.update()

        remOdd(L_vPst)
        remOdd(L_vInf)
        remOdd(L_vPresPart)
        remOdd(L_vPstPart)
        remOdd(L_vPstIntr)
        remOdd(L_vInfIntr)
        remOdd(L_vPresPartIntr)
        remOdd(L_vPstPartIntr)
        progressbar.update()
        progressbar.close()
# ////////////////////////////////////////////////////////////////////////////////////////////////////////////

# ////////////////////////////////////////////////////////////////////////////////////////////////////////////
def lGIntern(L_nS, L_nP, L_aPoss, L_aCmpr, L_aSup, L_adv, L_advInt, L_advSup, L_advCmpr, L_vPst, L_vInf, L_vPresPart, L_vPstPart, L_vPstIntr, L_vInfIntr, L_vPresPartIntr, L_vPstPartIntr):
    print('\n1. Reading Conllu file into a list...')
    print('2. Creating sub-lists from Conllu data...')
    progressbar = tqdm(total=4)
    
    with open('./rrgparbank/conllu/filtered_acc_en_conllu.conllu', 'r', encoding='UTF-8', newline='\n') as infileRRG:
        readerRRG = csv.reader(infileRRG, delimiter='\t')
        linesRRG = list(readerRRG)
        
        for i in range(len(linesRRG)):
            if len(linesRRG[i]) > 0:
                linesRRG[i].append('\t')       
                linesRRG[i][10] = '_'
        progressbar.update()
        
        appendListsDefIntern(linesRRG, L_nS, 'NOUN', 'Number=Sing')
        appendListsDefIntern(linesRRG, L_nP, 'NOUN', 'Number=Plur')
        appendListsDefIntern(linesRRG, L_aPoss, 'ADJ', 'Degree=Pos')
        appendListsDefIntern(linesRRG, L_aCmpr, 'ADJ', 'Degree=Cmp')
        appendListsDefIntern(linesRRG, L_aSup, 'ADJ', 'Degree=Sup')
        appendListsDefIntern(linesRRG, L_adv, 'ADV', '_')
        appendListsDefIntern(linesRRG, L_advInt, 'ADV', 'PronType=Int')
        appendListsDefIntern(linesRRG, L_advSup, 'ADV', 'Degree=Sup')
        appendListsDefIntern(linesRRG, L_advCmpr, 'ADV', 'Degree=Cmp')
        progressbar.update()

        # /// transitives
        appendListsTransIntern(linesRRG, L_vPstPart, 'VERB', 'Tense=Past', 'VerbForm=Part', 'VerbForm=Part')
        appendListsTransIntern(linesRRG, L_vPresPart, 'VERB', 'Tense=Pres', 'VerbForm=Part', 'VerbForm=Part')
        appendListsTransIntern(linesRRG, L_vInf, 'VERB', 'VerbForm=Inf', 'VerbForm=Inf', 'VerbForm=Inf')
        appendListsTransIntern(linesRRG, L_vPst, 'VERB', 'Tense=Past', 'VerbForm=Fin', 'VerbForm=Fin')
        progressbar.update()

        # /// intransitives
        appendListsIntransIntern(linesRRG, L_vPstPartIntr, 'VERB', 'Tense=Past', 'VerbForm=Part', 'VerbForm=Part')
        appendListsIntransIntern(linesRRG, L_vPresPartIntr, 'VERB', 'Tense=Pres', 'VerbForm=Part', 'VerbForm=Part')
        appendListsIntransIntern(linesRRG, L_vInfIntr, 'VERB', 'VerbForm=Inf', 'VerbForm=Inf', 'VerbForm=Inf')
        appendListsIntransIntern(linesRRG, L_vPstIntr, 'VERB', 'Tense=Past', 'VerbForm=Fin', 'VerbForm=Fin')
        progressbar.update()
        progressbar.close()
# ////////////////////////////////////////////////////////////////////////////////////////////////////////////

# ////////////////////// main function ////////////////////////////////////////////////////////////////////////////////////////////////
def mainG(input, trainInput, output, tag, L_nS, L_nP, L_aPoss, L_aCmpr, L_aSup, L_vPst, L_vInf, L_vPresPart, L_vPstPart):    
    start = time.perf_counter()

    if tag not in tags and tag != None:
        print(color.RED, color.BOLD, '\nWrong tag.\n')
        print("Enter available tag.", color.END)
        exit()
    elif tag == None:
        print(color.RED, color.BOLD, '\nMissing tag (-t) input!')
        print("Enter available tag.", color.END)
        exit()
        
    pth = str(os.path.dirname(input)).replace('\\', '')
    fileNoPath = (input).replace(pth, '').replace('/', '')
    # print('./rrgparbank/conllu/'+args.input)

    # if input is without a path, default path is attached to filename
    if input == fileNoPath:
        input = './rrgparbank/conllu/'+input
        
    try:    
        with open(input, encoding='UTF-8', newline='\n') as infileRRG:
            with open(trainInput, 'r+', encoding='UTF-8', newline='\n') as training:
                readerTr = csv.reader(training, delimiter='\t')
                linesTr = list(readerTr)
                readerRRG = csv.reader(infileRRG, delimiter='\t')
                linesRRG = list(readerRRG)  #///creates lists of lines from the file

                print('\nGenerating new columns and swapping words...')        
                progressbar = tqdm(total=len(linesRRG))        
                for i in range(len(linesRRG)):     
                    try:
                        if len(linesRRG[i]) > 0:
                            linesRRG[i].append('\t')       
                            linesRRG[i][10] = '_'
                            
                        if tag == 'nS' or tag == 'noun' or tag == 'all':
                            rndm = random.choice(L_nS)
                            if '&amp;' in rndm[0] or '#' in rndm[0] or '*' in rndm[0]:
                                rndm = random.choice(L_nS)
                            else:
                                if linesRRG[i][3] == 'NOUN' and linesRRG[i][5] == 'Number=Sing':                                                               
                                    if linesRRG[i][0] == '1':
                                        newrandom = rndm[0].capitalize()
                                        linesRRG[i][10] = linesRRG[i][1] # original word attached
                                        linesRRG[i][1] = newrandom
                                    else:
                                        linesRRG[i][10] = linesRRG[i][1]
                                        linesRRG[i][1] = rndm[0]
                                        linesRRG[i][2] = rndm[1]
                        if tag == 'nP' or tag == 'noun' or tag == 'all':
                            rndm = random.choice(L_nP)
                            if '&amp;' in rndm[0] or '#' in rndm[0] or '*' in rndm[0]:
                                rndm = random.choice(L_nP)
                            else:
                                if linesRRG[i][3] == 'NOUN' and linesRRG[i][5] == 'Number=Plur':
                                    if linesRRG[i][0] == '1':
                                        newrandom = rndm[0].capitalize()
                                        linesRRG[i][10] = linesRRG[i][1] # original word attached
                                        linesRRG[i][1] = newrandom
                                    else:
                                        linesRRG[i][10] = linesRRG[i][1]
                                        linesRRG[i][1] = rndm[0]
                                        linesRRG[i][2] = rndm[1]                                                                   
                                
                        if tag == 'aPoss' or tag == 'adj' or tag == 'all':
                            rndm = random.choice(L_aPoss)
                            if '&amp;' in rndm[0] or '#' in rndm[0] or '*' in rndm[0]:
                                rndm = random.choice(L_aPoss)
                            else:
                                if linesRRG[i][3] == 'ADJ' and linesRRG[i][5] == 'Degree=Pos':
                                    if linesRRG[i][0] == '1':
                                        newrandom = rndm[0].capitalize()
                                        linesRRG[i][10] = linesRRG[i][1] # original word attached
                                        linesRRG[i][1] = newrandom
                                    else:
                                        linesRRG[i][10] = linesRRG[i][1]
                                        linesRRG[i][1] = rndm[0]
                                        linesRRG[i][2] = rndm[1]                                                                    
                                
                        if tag == 'aCmpr' or tag == 'adj' or tag == 'all':
                            rndm = random.choice(L_aCmpr)
                            if '&amp;' in rndm[0] or '#' in rndm[0] or '*' in rndm[0]:
                                rndm = random.choice(L_aCmpr)
                            else:
                                if linesRRG[i][3] == 'ADJ' and linesRRG[i][5] == 'Degree=Cmp':
                                    if linesRRG[i][0] == '1':
                                        newrandom = rndm[0].capitalize()
                                        linesRRG[i][10] = linesRRG[i][1] # original word attached
                                        linesRRG[i][1] = newrandom
                                    else:
                                        linesRRG[i][10] = linesRRG[i][1]
                                        linesRRG[i][1] = rndm[0]
                                        linesRRG[i][2] = rndm[1]                                                                       
                                
                        if tag == 'aSup' or tag == 'adj' or tag == 'all':
                            rndm = random.choice(L_aSup)
                            if '&amp;' in rndm[0] or '#' in rndm[0] or '*' in rndm[0]:
                                rndm = random.choice(L_aSup)
                            else:
                                if linesRRG[i][3] == 'ADJ' and linesRRG[i][5] == 'Degree=Sup':
                                    if linesRRG[i][0] == '1':
                                        newrandom = rndm[0].capitalize()
                                        linesRRG[i][10] = linesRRG[i][1] # original word attached
                                        linesRRG[i][1] = newrandom
                                    else:
                                        linesRRG[i][10] = linesRRG[i][1]
                                        linesRRG[i][1] = rndm[0]
                                        linesRRG[i][2] = rndm[1]                                                                 
        
                        if tag == 'vPst' or tag == 'verb' or tag == 'all':
                            rndm = random.choice(L_vPst)
                            if '&amp;' in rndm[0] or '#' in rndm[0] or '*' in rndm[0]:
                                rndm = random.choice(L_vPst)
                            else:
                                if linesRRG[i][3] == 'VERB' and 'Tense=Past' in linesRRG[i][5] and 'VerbForm=Fin' in linesRRG[i][5]:
                                    if linesRRG[i][0] == '1':
                                        newrandom = rndm[0].capitalize()
                                        linesRRG[i][10] = linesRRG[i][1] # original word attached
                                        linesRRG[i][1] = newrandom
                                    else:
                                        linesRRG[i][10] = linesRRG[i][1]
                                        linesRRG[i][1] = rndm[0]
                                        linesRRG[i][2] = rndm[1]                                   
                                                                
                        if tag == 'vInf' or tag == 'verb' or tag == 'all':
                            rndm = random.choice(L_vInf)
                            if '&amp;' in rndm[1] or '#' in rndm[1] or '*' in rndm[1]:
                                rndm = random.choice(L_vInf)
                            else:
                                if linesRRG[i][3] == 'VERB' and 'VerbForm=Inf' in linesRRG[i][5]:
                                    if linesRRG[i][0] == '1':
                                        newrandom = rndm[1].capitalize()
                                        linesRRG[i][10] = linesRRG[i][1] # original word attached
                                        linesRRG[i][1] = newrandom
                                    else:
                                        linesRRG[i][10] = linesRRG[i][1]
                                        linesRRG[i][1] = rndm[1]
                                        linesRRG[i][2] = rndm[1]
                                                                    
                        if tag == 'vPresPart' or tag == 'verb' or tag == 'all':
                            rndm = random.choice(L_vPresPart)
                            if '&amp;' in rndm[0] or '#' in rndm[0] or '*' in rndm[0]:
                                rndm = random.choice(L_vPresPart)
                            else:
                                if linesRRG[i][3] == 'VERB' and 'Tense=Pres' in linesRRG[i][5] and 'VerbForm=Part' in linesRRG[i][5]:
                                    if linesRRG[i][0] == '1':
                                        newrandom = rndm[0].capitalize()
                                        linesRRG[i][10] = linesRRG[i][1] # original word attached
                                        linesRRG[i][1] = newrandom
                                    else:
                                        linesRRG[i][10] = linesRRG[i][1]
                                        linesRRG[i][1] = rndm[0]
                                        linesRRG[i][2] = rndm[1]
                                                                    
                        if tag == 'vPstPart' or tag == 'verb' or tag == 'all':
                            rndm = random.choice(L_vPstPart)
                            if '&amp;' in rndm[0] or '#' in rndm[0] or '*' in rndm[0]:
                                rndm = random.choice(L_vPstPart)
                            else:
                                if linesRRG[i][3] == 'VERB' and 'Tense=Past' in linesRRG[i][5] and 'VerbForm=Part' in linesRRG[i][5]:
                                    if linesRRG[i][0] == '1':
                                        newrandom = rndm[0].capitalize()
                                        linesRRG[i][10] = linesRRG[i][1] # original word attached
                                        linesRRG[i][1] = newrandom
                                    else:
                                        linesRRG[i][10] = linesRRG[i][1]
                                        linesRRG[i][1] = rndm[0]
                                        linesRRG[i][2] = rndm[1]
                                                                                                 
                    except(IndexError):
                        i += 1
                        
                    progressbar.update()         
                progressbar.close()
                
    except(NameError):
        print("\nMissing tag.")
    except(FileNotFoundError):
        print("\nFile or path does not exist.")
    
    with open(trainInput, 'r+', encoding='UTF-8', newline='\n') as training:
        with open(output+'/modified_'+fileNoPath, 'w', encoding='UTF-8', newline='\n') as outfileRRG:
            writerRRG = csv.writer(outfileRRG, delimiter='\t')
            readerTr = csv.reader(training, delimiter='\t')
            linesTr = list(readerTr)
            
            trainLength = []    
            sentLengths(linesTr, trainLength)      
            
            print('\nChecking and writing relevant lines to the new file...')        
            progressbar = tqdm(total=len(linesRRG))
            # /// only writes changed lines and ones with a valid length
            try:
                for k in range(len(linesRRG)):
                    progressbar.update() 
                    if len(linesRRG[k]) > 0 and linesRRG[k][10] != '_' and linesRRG[k][4] in trainLength:                     
                        writerRRG.writerow(linesRRG[k])     
            except(IndexError):
                k += 1 
            
            progressbar.close()
            
    end = time.perf_counter()
    #print(f'\nTime taken: {((end-start)):0.2f} seconds')
# ////////////////////// end of main function ////////////////////////////////////////////////////////////////////////////////////////////////

# ////////////////////// main accurate function ////////////////////////////////////////////////////////////////////////////////////////////////
def mainGacc(input, trainInput, output, tag, L_nS, L_nP, L_aPoss, L_aCmpr, L_aSup, L_vPst, L_vInf, L_vPresPart, L_vPstPart, L_vPstIntr, L_vInfIntr, L_vPresPartIntr, L_vPstPartIntr):    
    start = time.perf_counter()

    if tag not in tags and tag != None:
        print(color.RED, color.BOLD, '\nWrong tag.\n')
        print("Enter available tag.", color.END)
        exit()
    elif tag == None:
        print(color.RED, color.BOLD, '\nMissing tag (-t) input!')
        print("Enter available tag.", color.END)
        exit()
        
    pth = str(os.path.dirname(input)).replace('\\', '')
    fileNoPath = (input).replace(pth, '').replace('/', '')
    # print('./rrgparbank/conllu/'+args.input)

    # if input is without a path, default path is attached to filename
    if input == fileNoPath:
        input = './rrgparbank/conllu/'+input
    
    try:    
        with open(input, encoding='UTF-8', newline='\n') as infileRRG:
            with open(trainInput, 'r+', encoding='UTF-8', newline='\n') as training:
                readerTr = csv.reader(training, delimiter='\t')
                linesTr = list(readerTr)
                readerRRG = csv.reader(infileRRG, delimiter='\t')
                linesRRG = list(readerRRG)  #///creates lists of lines from the file

                print('\nGenerating new columns and swapping words...')        
                progressbar = tqdm(total=len(linesRRG))        
                for i in range(len(linesRRG)):     
                    try:
                        if len(linesRRG[i]) > 0:
                            linesRRG[i].append('\t')       
                            linesRRG[i][10] = '_'
                       
                        if tag == 'nS' or tag == 'noun' or tag == 'all':
                            rndm = random.choice(L_nS)
                            while '&amp;' in rndm[0] or '#' in rndm[0] or '*' in rndm[0]:
                                rndm = random.choice(L_nS)
                            else:
                                if linesRRG[i][3] == 'NOUN' and linesRRG[i][5] == 'Number=Sing':
                                    if linesRRG[i][0] == '1':
                                        newrandom = rndm[0].capitalize()
                                        linesRRG[i][10] = linesRRG[i][1] # original word attached
                                        linesRRG[i][1] = newrandom
                                    else:
                                        linesRRG[i][10] = linesRRG[i][1]
                                        linesRRG[i][1] = rndm[0]
                                        linesRRG[i][2] = rndm[1]                                   
                          
                        if tag == 'nP' or tag == 'noun' or tag == 'all':
                            rndm = random.choice(L_nP)
                            while '&amp;' in rndm[0] or '#' in rndm[0] or '*' in rndm[0]:
                                rndm = random.choice(L_nP)
                            else:
                                if linesRRG[i][3] == 'NOUN' and linesRRG[i][5] == 'Number=Plur':
                                    if linesRRG[i][0] == '1':
                                        newrandom = rndm[0].capitalize()
                                        linesRRG[i][10] = linesRRG[i][1] # original word attached
                                        linesRRG[i][1] = newrandom
                                    else:
                                        linesRRG[i][10] = linesRRG[i][1]
                                        linesRRG[i][1] = rndm[0]
                                        linesRRG[i][2] = rndm[1]                                   
                                 
                        if tag == 'aPoss' or tag == 'adj' or tag == 'all':
                            rndm = random.choice(L_aPoss)
                            while '&amp;' in rndm[0] or '#' in rndm[0] or '*' in rndm[0]:
                                rndm = random.choice(L_aPoss)
                            else:
                                if linesRRG[i][3] == 'ADJ' and linesRRG[i][5] == 'Degree=Pos':
                                    if linesRRG[i][0] == '1':
                                        newrandom = rndm[0].capitalize()
                                        linesRRG[i][10] = linesRRG[i][1] # original word attached
                                        linesRRG[i][1] = newrandom
                                    else:
                                        linesRRG[i][10] = linesRRG[i][1]
                                        linesRRG[i][1] = rndm[0]
                                        linesRRG[i][2] = rndm[1]                                     
                               
                        if tag == 'aCmpr' or tag == 'adj' or tag == 'all':
                            rndm = random.choice(L_aCmpr)
                            while '&amp;' in rndm[0] or '#' in rndm[0] or '*' in rndm[0]:
                                rndm = random.choice(L_aCmpr)
                            else:
                                if linesRRG[i][3] == 'ADJ' and linesRRG[i][5] == 'Degree=Cmp':
                                    if linesRRG[i][0] == '1':
                                        newrandom = rndm[0].capitalize()
                                        linesRRG[i][10] = linesRRG[i][1] # original word attached
                                        linesRRG[i][1] = newrandom
                                    else:
                                        linesRRG[i][10] = linesRRG[i][1]
                                        linesRRG[i][1] = rndm[0]
                                        linesRRG[i][2] = rndm[1]                                   
                                             
                        if tag == 'aSup' or tag == 'adj' or tag == 'all':
                            rndm = random.choice(L_aSup)
                            while '&amp;' in rndm[0] or '#' in rndm[0] or '*' in rndm[0]:
                                rndm = random.choice(L_aSup)
                            else:
                                if linesRRG[i][3] == 'ADJ' and linesRRG[i][5] == 'Degree=Sup':
                                    if linesRRG[i][0] == '1':
                                        newrandom = rndm[0].capitalize()
                                        linesRRG[i][10] = linesRRG[i][1] # original word attached
                                        linesRRG[i][1] = newrandom
                                    else:
                                        linesRRG[i][10] = linesRRG[i][1]
                                        linesRRG[i][1] = rndm[0]
                                        linesRRG[i][2] = rndm[1]                                    
                         
                        if tag == 'vPst' or tag == 'verb' or tag == 'all':
                            rndm = random.choice(L_vPst)
                            rndmIntr = random.choice(L_vPstIntr)
                            while '&amp;' in rndm[0] or '#' in rndm[0] or '*' in rndm[0]:
                                rndm = random.choice(L_vPst)
                            while '&amp;' in rndmIntr[0] or '#' in rndmIntr[0] or '*' in rndmIntr[0]:
                                rndmIntr = random.choice(L_vPstIntr)
                            else:
                                if linesRRG[i][3] == 'VERB' and 'Tense=Past' in linesRRG[i][5] and 'VerbForm=Fin' in linesRRG[i][5] and 'transitive' in linesRRG[i][9]:
                                    if linesRRG[i][0] == '1':
                                        newrandom = rndm[0].capitalize()
                                        linesRRG[i][10] = linesRRG[i][1] # original word attached
                                        linesRRG[i][1] = newrandom
                                    else:
                                        linesRRG[i][10] = linesRRG[i][1]
                                        linesRRG[i][1] = rndm[0]
                                        linesRRG[i][2] = rndm[1]                                     
                                if linesRRG[i][3] == 'VERB' and 'Tense=Past' in linesRRG[i][5] and 'VerbForm=Fin' in linesRRG[i][5] and linesRRG[i][9] == '_':
                                    if linesRRG[i][0] == '1':
                                        newrandom = rndmIntr[0].capitalize()
                                        linesRRG[i][10] = linesRRG[i][1] # original word attached
                                        linesRRG[i][1] = newrandom
                                    else:
                                        linesRRG[i][10] = linesRRG[i][1]
                                        linesRRG[i][1] = rndmIntr[0]
                                        linesRRG[i][2] = rndmIntr[1]                                     
                                 
                        if tag == 'vInf' or tag == 'verb' or tag == 'all':
                            rndm = random.choice(L_vInf)
                            rndmIntr = random.choice(L_vInfIntr)
                            while '&amp;' in rndm[1] or '#' in rndm[1] or '*' in rndm[1]:
                                rndm = random.choice(L_vInf)
                            while '&amp;' in rndmIntr[1] or '#' in rndmIntr[1] or '*' in rndmIntr[1]:
                                rndmIntr = random.choice(L_vInfIntr)
                            else:
                                if linesRRG[i][3] == 'VERB' and 'VerbForm=Inf' in linesRRG[i][5] and 'transitive' in linesRRG[i][9]:
                                    if linesRRG[i][0] == '1':
                                        newrandom = rndm[1].capitalize()
                                        linesRRG[i][10] = linesRRG[i][1] # original word attached
                                        linesRRG[i][1] = newrandom
                                    else:
                                        linesRRG[i][10] = linesRRG[i][1]
                                        linesRRG[i][1] = rndm[1]
                                        linesRRG[i][2] = rndm[1] 
                                if linesRRG[i][3] == 'VERB' and 'VerbForm=Inf' in linesRRG[i][5] and linesRRG[i][9] == '_':
                                    if linesRRG[i][0] == '1':
                                        newrandom = rndmIntr[1].capitalize()
                                        linesRRG[i][10] = linesRRG[i][1] # original word attached
                                        linesRRG[i][1] = newrandom
                                    else:
                                        linesRRG[i][10] = linesRRG[i][1]
                                        linesRRG[i][1] = rndmIntr[1]
                                        linesRRG[i][2] = rndmIntr[1]                                     
                                
                        if tag == 'vPresPart' or tag == 'verb' or tag == 'all':
                            rndm = random.choice(L_vPresPart)
                            rndmIntr = random.choice(L_vPresPartIntr)
                            while '&amp;' in rndm[0] or '#' in rndm[0] or '*' in rndm[0]:
                                rndm = random.choice(L_vPresPart)
                            while '&amp;' in rndmIntr[0] or '#' in rndmIntr[0] or '*' in rndmIntr[0]:
                                rndmIntr = random.choice(L_vPresPartIntr)
                            else:
                                if linesRRG[i][3] == 'VERB' and 'Tense=Pres' in linesRRG[i][5] and 'VerbForm=Part' in linesRRG[i][5] and 'transitive' in linesRRG[i][9]:
                                    if linesRRG[i][0] == '1':
                                        newrandom = rndm[0].capitalize()
                                        linesRRG[i][10] = linesRRG[i][1] # original word attached
                                        linesRRG[i][1] = newrandom
                                    else:
                                        linesRRG[i][10] = linesRRG[i][1]
                                        linesRRG[i][1] = rndm[0]
                                        linesRRG[i][2] = rndm[1] 
                                if linesRRG[i][3] == 'VERB' and 'Tense=Pres' in linesRRG[i][5] and 'VerbForm=Part' in linesRRG[i][5] and linesRRG[i][9] == '_':
                                    if linesRRG[i][0] == '1':
                                        newrandom = rndmIntr[0].capitalize()
                                        linesRRG[i][10] = linesRRG[i][1] # original word attached
                                        linesRRG[i][1] = newrandom
                                    else:
                                        linesRRG[i][10] = linesRRG[i][1]
                                        linesRRG[i][1] = rndmIntr[0]
                                        linesRRG[i][2] = rndmIntr[1]                  
                               
                        if tag == 'vPstPart' or tag == 'verb' or tag == 'all':
                            rndm = random.choice(L_vPstPart)
                            rndmIntr = random.choice(L_vPstPartIntr)
                            while '&amp;' in rndm[0] or '#' in rndm[0] or '*' in rndm[0]:
                                rndm = random.choice(L_vPstPart)
                            while '&amp;' in rndmIntr[0] or '#' in rndmIntr[0] or '*' in rndmIntr[0]:
                                rndmIntr = random.choice(L_vPstPartIntr)
                            else:
                                if linesRRG[i][3] == 'VERB' and 'Tense=Past' in linesRRG[i][5] and 'VerbForm=Part' in linesRRG[i][5] and 'transitive' in linesRRG[i][9]:
                                    if linesRRG[i][0] == '1':
                                        newrandom = rndm[0].capitalize()
                                        linesRRG[i][10] = linesRRG[i][1] # original word attached
                                        linesRRG[i][1] = newrandom
                                    else:
                                        linesRRG[i][10] = linesRRG[i][1]
                                        linesRRG[i][1] = rndm[0]
                                        linesRRG[i][2] = rndm[1]
                                if linesRRG[i][3] == 'VERB' and 'Tense=Past' in linesRRG[i][5] and 'VerbForm=Part' in linesRRG[i][5] and linesRRG[i][9] == '_':
                                    if linesRRG[i][0] == '1':
                                        newrandom = rndmIntr[0].capitalize()
                                        linesRRG[i][10] = linesRRG[i][1] # original word attached
                                        linesRRG[i][1] = newrandom
                                    else:
                                        linesRRG[i][10] = linesRRG[i][1]
                                        linesRRG[i][1] = rndmIntr[0]
                                        linesRRG[i][2] = rndmIntr[1]  
                                                                                              
                    except(IndexError):
                        i += 1
                    progressbar.update()
                progressbar.close() 
                
    except(NameError):
        print("\nMissing tag.")
    except(FileNotFoundError):
        print("\nFile or path does not exist.")
    
    with open(trainInput, 'r+', encoding='UTF-8', newline='\n') as training:
        with open(output+'/modified_'+fileNoPath, 'w', encoding='UTF-8', newline='\n') as outfileRRG:
            writerRRG = csv.writer(outfileRRG, delimiter='\t')
            readerTr = csv.reader(training, delimiter='\t')
            linesTr = list(readerTr)
            
            trainLength = []    
            sentLengths(linesTr, trainLength)      
            
            print('\nChecking and writing relevant lines to the new file...')        
            progressbar = tqdm(total=len(linesRRG))
            # /// only writes changed lines and ones with a valid length
            try:
                for k in range(len(linesRRG)):
                    progressbar.update() 
                    if len(linesRRG[k]) > 0 and linesRRG[k][10] != '_' and linesRRG[k][4] in trainLength:                     
                        writerRRG.writerow(linesRRG[k])     
            except(IndexError):
                k += 1 
            
            progressbar.close()
            
    end = time.perf_counter()
    #print(f'\nTime taken: {((end-start)):0.2f} seconds')
# ////////////////////// end of accurate main function /////////////////////////////////////////////////////////////////////////////////////////

# ////////////////////// main internal function ////////////////////////////////////////////////////////////////////////////////////////////////
def mainGintern(input, trainInput, output, tag, L_nS, L_nP, L_aPoss, L_aCmpr, L_aSup, L_adv, L_advInt, L_advSup, L_advCmpr, L_vPst, L_vInf, L_vPresPart, L_vPstPart, L_vPstIntr, L_vInfIntr, L_vPresPartIntr, L_vPstPartIntr):    
    start = time.perf_counter()

    if tag not in tags and tag != None:
        print(color.RED, color.BOLD, '\nWrong tag.\n')
        print("Enter available tag.", color.END)
        exit()
    elif tag == None:
        print(color.RED, color.BOLD, '\nMissing tag (-t) input!')
        print("Enter available tag.", color.END)
        exit()
        
    pth = str(os.path.dirname(input)).replace('\\', '')
    fileNoPath = (input).replace(pth, '').replace('/', '')
    # print('./rrgparbank/conllu/'+args.input)

    # if input is without a path, default path is attached to filename
    if input == fileNoPath:
        input = './rrgparbank/conllu/'+input
    
    try:    
        with open(input, encoding='UTF-8', newline='\n') as infileRRG:
            with open(trainInput, 'r+', encoding='UTF-8', newline='\n') as training:
                readerTr = csv.reader(training, delimiter='\t')
                linesTr = list(readerTr)
                readerRRG = csv.reader(infileRRG, delimiter='\t')
                linesRRG = list(readerRRG)  #///creates lists of lines from the file

                print('\nGenerating new columns and swapping words...')        
                progressbar = tqdm(total=len(linesRRG))        
                for i in range(len(linesRRG)):     
                    try:
                        if len(linesRRG[i]) > 0:
                            linesRRG[i].append('\t')       
                            linesRRG[i][10] = '_'
                       
                        if tag == 'nS' or tag == 'noun' or tag == 'all':
                            rndm = random.choice(L_nS)
                            while rndm == linesRRG[i]:
                                rndm = random.choice(L_nS)
                            else:
                                if linesRRG[i][3] == 'NOUN' and linesRRG[i][5] == 'Number=Sing':
                                    if linesRRG[i][0] == '1':
                                        newrandom = rndm[1].capitalize()
                                        linesRRG[i][10] = linesRRG[i][1] # original word attached
                                        linesRRG[i][1] = newrandom
                                    else:
                                        linesRRG[i][10] = linesRRG[i][1]
                                        linesRRG[i][1] = rndm[1]
                                        linesRRG[i][2] = rndm[2]                                   
                          
                        if tag == 'nP' or tag == 'noun' or tag == 'all':
                            rndm = random.choice(L_nP)
                            while rndm == linesRRG[i]:
                                rndm = random.choice(L_nP)
                            else:
                                if linesRRG[i][3] == 'NOUN' and linesRRG[i][5] == 'Number=Plur':
                                    if linesRRG[i][0] == '1':
                                        newrandom = rndm[1].capitalize()
                                        linesRRG[i][10] = linesRRG[i][1] # original word attached
                                        linesRRG[i][1] = newrandom
                                    else:
                                        linesRRG[i][10] = linesRRG[i][1]
                                        linesRRG[i][1] = rndm[1]
                                        linesRRG[i][2] = rndm[2]                                   
                                 
                        if tag == 'aPoss' or tag == 'adj' or tag == 'all':
                            rndm = random.choice(L_aPoss)
                            while rndm == linesRRG[i]:
                                rndm = random.choice(L_aPoss)
                            else:
                                if linesRRG[i][3] == 'ADJ' and linesRRG[i][5] == 'Degree=Pos':
                                    if linesRRG[i][0] == '1':
                                        newrandom = rndm[1].capitalize()
                                        linesRRG[i][10] = linesRRG[i][1] # original word attached
                                        linesRRG[i][1] = newrandom
                                    else:
                                        linesRRG[i][10] = linesRRG[i][1]
                                        linesRRG[i][1] = rndm[1]
                                        linesRRG[i][2] = rndm[2]                                     
                               
                        if tag == 'aCmpr' or tag == 'adj' or tag == 'all':
                            rndm = random.choice(L_aCmpr)
                            while rndm == linesRRG[i]:
                                rndm = random.choice(L_aCmpr)
                            else:
                                if linesRRG[i][3] == 'ADJ' and linesRRG[i][5] == 'Degree=Cmp':
                                    if linesRRG[i][0] == '1':
                                        newrandom = rndm[1].capitalize()
                                        linesRRG[i][10] = linesRRG[i][1] # original word attached
                                        linesRRG[i][1] = newrandom
                                    else:
                                        linesRRG[i][10] = linesRRG[i][1]
                                        linesRRG[i][1] = rndm[1]
                                        linesRRG[i][2] = rndm[2]                                   
                                             
                        if tag == 'aSup' or tag == 'adj' or tag == 'all':
                            rndm = random.choice(L_aSup)
                            while rndm == linesRRG[i]:
                                rndm = random.choice(L_aSup)
                            else:
                                if linesRRG[i][3] == 'ADJ' and linesRRG[i][5] == 'Degree=Sup':
                                    if linesRRG[i][0] == '1':
                                        newrandom = rndm[1].capitalize()
                                        linesRRG[i][10] = linesRRG[i][1] # original word attached
                                        linesRRG[i][1] = newrandom
                                    else:
                                        linesRRG[i][10] = linesRRG[i][1]
                                        linesRRG[i][1] = rndm[1]
                                        linesRRG[i][2] = rndm[2] 
                                        
                        # if tag == 'adv' or tag == 'all':
                        #     if linesRRG[i][3] == 'ADV' and '_' in linesRRG[i][5]:
                        #         rndm = random.choice(L_adv)
                        #         while linesRRG[i][7] != rndm[7]:
                        #             rndm = random.choice(L_adv)   
                        #         if linesRRG[i][0] == '1':
                        #             newrandom = rndm[1].capitalize()
                        #             linesRRG[i][10] = linesRRG[i][1] # original word attached
                        #             linesRRG[i][1] = newrandom
                        #         else:
                        #             linesRRG[i][10] = linesRRG[i][1]
                        #             linesRRG[i][1] = rndm[1]
                        #             linesRRG[i][2] = rndm[2]
                                    
                        # if tag == 'advInt' or tag == 'all':
                        #     if linesRRG[i][3] == 'ADV' and 'PronType=Int' in linesRRG[i][5]:
                        #         rndm = random.choice(L_advInt)
                        #         while linesRRG[i][7] != rndm[7]:
                        #             rndm = random.choice(L_advInt)   
                        #         if linesRRG[i][0] == '1':
                        #             newrandom = rndm[1].capitalize()
                        #             linesRRG[i][10] = linesRRG[i][1] # original word attached
                        #             linesRRG[i][1] = newrandom
                        #         else:
                        #             linesRRG[i][10] = linesRRG[i][1]
                        #             linesRRG[i][1] = rndm[1]
                        #             linesRRG[i][2] = rndm[2] 
                                    
                        # if tag == 'advSup' or tag == 'all':   
                        #     if linesRRG[i][3] == 'ADV' and 'Degree=Sup' in linesRRG[i][5]:
                        #         rndm = random.choice(L_advSup)
                        #         while linesRRG[i][7] != rndm[7]:
                        #             rndm = random.choice(L_advSup)   
                        #         if linesRRG[i][0] == '1':
                        #             newrandom = rndm[1].capitalize()
                        #             linesRRG[i][10] = linesRRG[i][1] # original word attached
                        #             linesRRG[i][1] = newrandom
                        #         else:
                        #             linesRRG[i][10] = linesRRG[i][1]
                        #             linesRRG[i][1] = rndm[1]
                        #             linesRRG[i][2] = rndm[2]
                                    
                        # if tag == 'advCmpr' or tag == 'all':    
                        #     if linesRRG[i][3] == 'ADV' and 'Degree=Cmp' in linesRRG[i][5]:
                        #         rndm = random.choice(L_advCmpr)
                        #         while linesRRG[i][7] != rndm[7]:
                        #             rndm = random.choice(L_advCmpr)   
                        #         if linesRRG[i][0] == '1':
                        #             newrandom = rndm[1].capitalize()
                        #             linesRRG[i][10] = linesRRG[i][1] # original word attached
                        #             linesRRG[i][1] = newrandom
                        #         else:
                        #             linesRRG[i][10] = linesRRG[i][1]
                        #             linesRRG[i][1] = rndm[1]
                        #             linesRRG[i][2] = rndm[2]                                     
                         
                        if tag == 'vPst' or tag == 'verb' or tag == 'all':
                            if linesRRG[i][3] == 'VERB' and 'Tense=Past' in linesRRG[i][5] and 'VerbForm=Fin' in linesRRG[i][5] and 'transitive' in linesRRG[i][9]:
                                rndm = random.choice(L_vPst)
                                while rndm[9] != linesRRG[i][9]:
                                    rndm = random.choice(L_vPst)
                                if linesRRG[i][0] == '1':
                                    newrandom = rndm[1].capitalize()
                                    linesRRG[i][10] = linesRRG[i][1] # original word attached
                                    linesRRG[i][1] = newrandom
                                else:
                                    linesRRG[i][10] = linesRRG[i][1]
                                    linesRRG[i][1] = rndm[1].lower()
                                    linesRRG[i][2] = rndm[2]                                     
                            if linesRRG[i][3] == 'VERB' and 'Tense=Past' in linesRRG[i][5] and 'VerbForm=Fin' in linesRRG[i][5] and linesRRG[i][9] == '_':
                                rndmIntr = random.choice(L_vPstIntr)
                                while rndmIntr == linesRRG[i]:
                                    rndmIntr = random.choice(L_vPstIntr)
                                if linesRRG[i][0] == '1':
                                    newrandom = rndmIntr[1].capitalize()
                                    linesRRG[i][10] = linesRRG[i][1] # original word attached
                                    linesRRG[i][1] = newrandom
                                else:
                                    linesRRG[i][10] = linesRRG[i][1]
                                    linesRRG[i][1] = rndmIntr[1].lower()
                                    linesRRG[i][2] = rndmIntr[2]                                     
                                 
                        if tag == 'vInf' or tag == 'verb' or tag == 'all':
                            if linesRRG[i][3] == 'VERB' and 'VerbForm=Inf' in linesRRG[i][5] and 'transitive' in linesRRG[i][9]:
                                rndm = random.choice(L_vInf)
                                while rndm[9] != linesRRG[i][9]:
                                    rndm = random.choice(L_vInf)
                                if linesRRG[i][0] == '1':
                                    newrandom = rndm[1].capitalize()
                                    linesRRG[i][10] = linesRRG[i][1] # original word attached
                                    linesRRG[i][1] = newrandom
                                else:
                                    linesRRG[i][10] = linesRRG[i][1]
                                    linesRRG[i][1] = rndm[1].lower()
                                    linesRRG[i][2] = rndm[2] 
                            if linesRRG[i][3] == 'VERB' and 'VerbForm=Inf' in linesRRG[i][5] and linesRRG[i][9] == '_':
                                rndmIntr = random.choice(L_vInfIntr)
                                while rndmIntr == linesRRG[i]:
                                    rndmIntr = random.choice(L_vInfIntr)
                                if linesRRG[i][0] == '1':
                                    newrandom = rndmIntr[1].capitalize()
                                    linesRRG[i][10] = linesRRG[i][1] # original word attached
                                    linesRRG[i][1] = newrandom
                                else:
                                    linesRRG[i][10] = linesRRG[i][1]
                                    linesRRG[i][1] = rndmIntr[1].lower()
                                    linesRRG[i][2] = rndmIntr[2]                                     
                            
                        if tag == 'vPresPart' or tag == 'verb' or tag == 'all':
                            if linesRRG[i][3] == 'VERB' and 'Tense=Pres' in linesRRG[i][5] and 'VerbForm=Part' in linesRRG[i][5] and 'transitive' in linesRRG[i][9]:
                                rndm = random.choice(L_vPresPart)
                                while rndm[9] != linesRRG[i][9]:
                                    rndm = random.choice(L_vPresPart)
                                if linesRRG[i][0] == '1':
                                    newrandom = rndm[1].capitalize()
                                    linesRRG[i][10] = linesRRG[i][1] # original word attached
                                    linesRRG[i][1] = newrandom
                                else:
                                    linesRRG[i][10] = linesRRG[i][1]
                                    linesRRG[i][1] = rndm[1].lower()
                                    linesRRG[i][2] = rndm[2] 
                            if linesRRG[i][3] == 'VERB' and 'Tense=Pres' in linesRRG[i][5] and 'VerbForm=Part' in linesRRG[i][5] and linesRRG[i][9] == '_':
                                rndmIntr = random.choice(L_vPresPartIntr)
                                while rndmIntr == linesRRG[i]:
                                    rndmIntr = random.choice(L_vPresPartIntr)
                                if linesRRG[i][0] == '1':
                                    newrandom = rndmIntr[1].capitalize()
                                    linesRRG[i][10] = linesRRG[i][1] # original word attached
                                    linesRRG[i][1] = newrandom
                                else:
                                    linesRRG[i][10] = linesRRG[i][1]
                                    linesRRG[i][1] = rndmIntr[1].lower()
                                    linesRRG[i][2] = rndmIntr[2]                  
                               
                        if tag == 'vPstPart' or tag == 'verb' or tag == 'all':
                            if linesRRG[i][3] == 'VERB' and 'Tense=Past' in linesRRG[i][5] and 'VerbForm=Part' in linesRRG[i][5] and 'transitive' in linesRRG[i][9]:
                                rndm = random.choice(L_vPstPart)
                                while rndm[9] != linesRRG[i][9]:
                                    rndm = random.choice(L_vPstPart)
                                if linesRRG[i][0] == '1':
                                    newrandom = rndm[1].capitalize()
                                    linesRRG[i][10] = linesRRG[i][1] # original word attached
                                    linesRRG[i][1] = newrandom
                                else:
                                    linesRRG[i][10] = linesRRG[i][1]
                                    linesRRG[i][1] = rndm[1].lower()
                                    linesRRG[i][2] = rndm[2]
                            if linesRRG[i][3] == 'VERB' and 'Tense=Past' in linesRRG[i][5] and 'VerbForm=Part' in linesRRG[i][5] and linesRRG[i][9] == '_':
                                rndmIntr = random.choice(L_vPstPartIntr)
                                while rndmIntr == linesRRG[i]:
                                    rndmIntr = random.choice(L_vPstPartIntr)
                                if linesRRG[i][0] == '1':
                                    newrandom = rndmIntr[1].capitalize()
                                    linesRRG[i][10] = linesRRG[i][1] # original word attached
                                    linesRRG[i][1] = newrandom
                                else:
                                    linesRRG[i][10] = linesRRG[i][1]
                                    linesRRG[i][1] = rndmIntr[1].lower()
                                    linesRRG[i][2] = rndmIntr[2]  
                                                                                              
                    except(IndexError):
                        i += 1
                    progressbar.update()
                progressbar.close() 
                
    except(NameError):
        print("\nMissing tag.")
    except(FileNotFoundError):
        print("\nFile or path does not exist.")
    
    with open(trainInput, 'r+', encoding='UTF-8', newline='\n') as training:
        with open(output+'/modified_'+fileNoPath, 'w', encoding='UTF-8', newline='\n') as outfileRRG:
            writerRRG = csv.writer(outfileRRG, delimiter='\t')
            readerTr = csv.reader(training, delimiter='\t')
            linesTr = list(readerTr)
            
            trainLength = []    
            sentLengths(linesTr, trainLength)      
            
            print('\nChecking and writing relevant lines to the new file...')        
            progressbar = tqdm(total=len(linesRRG))
            # /// only writes changed lines and ones with a valid length
            try:
                for k in range(len(linesRRG)):
                    progressbar.update() 
                    if len(linesRRG[k]) > 0 and linesRRG[k][10] != '_' and linesRRG[k][4] in trainLength:                     
                        writerRRG.writerow(linesRRG[k])     
            except(IndexError):
                k += 1 
            
            progressbar.close()
            
    end = time.perf_counter()
    #print(f'\nTime taken: {((end-start)):0.2f} seconds')
# ////////////////////// end of internal main function /////////////////////////////////////////////////////////////////////////////////////////

# ////////////////////// main supertag function ////////////////////////////////////////////////////////////////////////////////////////////////
def mainGsupertag(trainInput, output, tag):    
    start = time.perf_counter()
    trainInput = './experiments/rrgparbank-en/base/train.supertags'
    output = './experiments/rrgparbank-en/'
    
        
    pth = str(os.path.dirname(trainInput)).replace('\\', '')
    fileNoPath = (trainInput).replace(pth, '').replace('/', '')
    # print('./rrgparbank/conllu/'+args.input)

    # if input is without a path, default path is attached to filename
    if trainInput == fileNoPath:
        trainInput = './rrgparbank-en/base/'+trainInput
    
    try:    
        with open(trainInput, encoding='UTF-8', newline='\n') as infileTr:
            with open(output+'tempST.txt', 'w', encoding='UTF-8', newline='\n') as infileTempTr:
                readerTr = csv.reader(infileTr, delimiter='\t')
                linesTr = list(readerTr) 
                writerTr = csv.writer(infileTempTr, delimiter='\t')
                
                print('\nGenerating new columns and swapping words...')        
                progressbar = tqdm(total=len(linesTr))        
                for i in range(len(linesTr)):     
                    try:
                        if len(linesTr[i]) > 0:
                            linesTr[i].append('\t')       
                            linesTr[i][4] = '_'
                    
                        rndm = random.choice(linesTr)
                        while rndm[3] != linesTr[i][3]:
                            rndm = random.choice(linesTr)
                        else:
                            if linesTr[i][0] == '1':
                                newrandom = rndm[1].capitalize()
                                linesTr[i][4] = linesTr[i][1] # original word attached
                                linesTr[i][1] = newrandom
                            else:
                                linesTr[i][4] = linesTr[i][1]
                                linesTr[i][1] = rndm[1]
                    except(IndexError):
                        i += 1
                    
                    progressbar.update()
                progressbar.close() 
                writerTr.writerows(linesTr)
                
    except(NameError):
        print("\nMissing tag.")
    except(FileNotFoundError):
        print("\nFile or path does not exist.")
    
    end = time.perf_counter()
    #print(f'\nTime taken: {((end-start)):0.2f} seconds')
# ////////////////////// end of supertag main function /////////////////////////////////////////////////////////////////////////////////////////

if __name__ == '__main__': 
    # // commands //////////////////////////////////////////////////////////////////////////////////////////
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument('-h', '--help', help=info(), action='help')
    parser.add_argument('--unimorph0', action='store_true', required=False, help='UniMorph Inaccurate verb replacements with regard to transitivity. In place of --unimorph1, --internal, --supertag, or --original.')
    parser.add_argument('--unimorph1', action='store_true', required=False, help='UniMorph Accurate verb replacements with regard to transitivity. In place of --unimorph0, --internal, --supertag, or --original.')
    parser.add_argument('--internal', action='store_true', required=False, help='For internal word swapping. In place of --unimorph0, unimorph1, --supertag, or --original.')
    parser.add_argument('--supertag', action='store_true', required=False, help='For internal supertag word swapping. In place of --unimorph0, unimorph1, --internal, or --original.')
    parser.add_argument('-i', '--input', type=str, required=False, default='./rrgparbank/conllu/filtered_acc_en_conllu.conllu', help='(OPTIONAL) File input.')
    parser.add_argument('-ti', '--trainInput', type=str, required=False, default='./experiments/rrgparbank-en/base/train.supertags', help='(OPTIONAL) train.supertags file input')
    parser.add_argument('-o', '--output', type=str, required=False, default='./rrgparbank/conllu', help='(OPTIONAL) Output folder.')
    parser.add_argument('-t', '--tag', type=str, required=True, help='Word tags.')
    args = parser.parse_args()
    # ////////////////////////////////////////////////////////////////////////////////////////////////////// 
    
    L_nS = []
    L_aPoss = []
    L_nP = []
    L_aCmpr = []
    L_aSup = []
    L_vPst = []
    L_vInf = []
    L_vPresPart = []
    L_vPstPart = []
    L_adv = []
    L_advInt = []
    L_advSup = []
    L_advCmpr = [] 
    L_vPstIntr = []
    L_vInfIntr = []
    L_vPresPartIntr = []
    L_vPstPartIntr = []
    
    if args.unimorph0 == True and args.unimorph1 == False:
        lG(L_nS, L_nP, L_aPoss, L_aCmpr, L_aSup, L_vPst, L_vInf, L_vPresPart, L_vPstPart)  
        mainG(args.input, args.trainInput, args.output, args.tag, L_nS, L_nP, L_aPoss, L_aCmpr, L_aSup, L_vPst, L_vInf, L_vPresPart, L_vPstPart) 
    elif args.unimorph1 == True and args.unimorph0 == False:
        lGacc(L_nS, L_nP, L_aPoss, L_aCmpr, L_aSup, L_vPst, L_vInf, L_vPresPart, L_vPstPart, L_vPstIntr, L_vInfIntr, L_vPresPartIntr, L_vPstPartIntr)
        mainGacc(args.input, args.trainInput, args.output, args.tag, L_nS, L_nP, L_aPoss, L_aCmpr, L_aSup, L_vPst, L_vInf, L_vPresPart, L_vPstPart, L_vPstIntr, L_vInfIntr, L_vPresPartIntr, L_vPstPartIntr) 
    elif args.internal == True and args.unimorph0 == False and args.unimorph1 == False and args.supertag == False:
        lGIntern(L_nS, L_nP, L_aPoss, L_aCmpr, L_aSup, L_adv, L_advInt, L_advSup, L_advCmpr, L_vPst, L_vInf, L_vPresPart, L_vPstPart, L_vPstIntr, L_vInfIntr, L_vPresPartIntr, L_vPstPartIntr)
        mainGintern(args.input, args.trainInput, args.output, args.tag, L_nS, L_nP, L_aPoss, L_aCmpr, L_aSup, L_adv, L_advInt, L_advSup, L_advCmpr, L_vPst, L_vInf, L_vPresPart, L_vPstPart, L_vPstIntr, L_vInfIntr, L_vPresPartIntr, L_vPstPartIntr)
    elif args.supertag == True and args.unimorph0 == False and args.unimorph1 == False and args.internal == False:
        mainGsupertag(args.trainInput, args.output, args.tag)
    else:
        print(color.RED+'Use --unimorph0, --unimorph1, --supertag or --internal'+color.END)
        exit()
   