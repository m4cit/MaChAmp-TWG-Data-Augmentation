# /////////////// Filters out all unused words / lines in the RRG CoNLLU file

import csv
import os
from tqdm import tqdm
import time
import argparse
from generate import sentLengths

if __name__ == '__main__':
    start = time.perf_counter()
    
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', default='./rrgparbank/conllu/acc_en_conllu.conllu', type=str, help='RRG file input')
    parser.add_argument('-f', '--filter', type=str, default='./experiments/rrgparbank-en/base/train.supertags', help='Which file to filter for')
    args = parser.parse_args() 

    # if args.accuracy == 0:
    #     args.input = './rrgparbank/conllu/en_conllu.conllu'
    # elif args.accuracy == 1:
    #     args.input = './rrgparbank/conllu/acc_en_conllu.conllu'
    
    pthIn = str(os.path.dirname(args.input)).replace('\\', '')
    pthF = str(os.path.dirname(args.filter)).replace('\\', '')
    fileNoPathIn = (args.input).replace(pthIn, '').replace('/', '')
    fileNoPathF = (args.filter).replace(pthF, '').replace('/', '')
    
    if args.input == fileNoPathIn:
        args.input = './rrgparbank/conllu/'+args.input
    if args.filter == fileNoPathF:
        args.filter = './experiments/rrgparbank-en/base/'+args.filter
        
    with open(args.input, 'r+', encoding='UTF-8', newline='\n') as infileRRG:
        with open(args.filter, 'r+', encoding='UTF-8', newline='\n') as training:
            with open('./rrgparbank/conllu/temp.txt', 'w', encoding='UTF-8', newline='\n') as tempfile:
                readerRRG = csv.reader(infileRRG, delimiter='\t')
                readerTr = csv.reader(training, delimiter='\t')
                linesRRG = list(readerRRG)
                linesTr = list(readerTr)
                writerTemp = csv.writer(tempfile, delimiter='\t')
                
                trainLength = []
                rrgLength = []
                sentLengths(linesRRG, rrgLength) 
                sentLengths(linesTr, trainLength)
                
                try:
                    countTr = 0
                    for i in range(len(linesTr)):               
                        if len(linesTr[i]) > 0:
                            linesTr[i].append('\t')
                            linesTr[i][4] = '_'
                    for i in range(len(linesTr)):         
                        if len(linesTr[i]) > 0:
                            linesTr[i][4] = trainLength[countTr]
                        else:
                            countTr += 1
                except(IndexError):
                    i += 1
                
                try:
                    countRRG = 0
                    for i in range(len(linesRRG)):               
                        if len(linesRRG[i]) > 0:
                            linesRRG[i][4] = rrgLength[countRRG]
                        else:
                            countRRG += 1
                except(IndexError):
                    i += 1
                
                # /// creating dictionaries for faster access
                dctRRG = {'lines':[i for i in linesRRG if len(i) > 0]}
                dctTr = {'lines':[i for i in linesTr if len(i) > 0]}                
                
                print('\nFiltering...')
                progressbar = tqdm(total=(len(linesTr)-linesTr.count([])))        
                for lineTr in dctTr['lines']:    
                    for lineRRG in dctRRG['lines']:
                        if lineRRG[1] == lineTr[1] and lineRRG[0] == lineTr[0] and lineRRG[4] == lineTr[4] and (lineRRG[3] == 'NOUN' or lineRRG[3] == 'VERB' or lineRRG[3] == 'ADJ' or lineRRG[3] == 'ADV'):
                                writerTemp.writerow(lineRRG)          
                    progressbar.update()
                progressbar.close()

    with open('./rrgparbank/conllu/temp.txt', 'r', encoding='UTF-8', newline='\n') as tempfile:
        with open('./rrgparbank/conllu/filtered_'+fileNoPathIn, 'w', encoding='UTF-8', newline='\n') as outfile:    
            writerRRG = csv.writer(outfile, delimiter='\t')
            readerTemp = csv.reader(tempfile, delimiter='\t')
            linesTemp = list(readerTemp)
            
            #linesTemp.sort(key=lambda x:x[8])

            writerRRG.writerows(linesTemp)

    os.remove('./rrgparbank/conllu/temp.txt')

    end = time.perf_counter()
    print(f'\nTime taken: {((end-start)/60):0.2f} minutes')         
            
