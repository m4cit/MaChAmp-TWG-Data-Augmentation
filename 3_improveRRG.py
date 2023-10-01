# /////////////// Checks and adds the transitivity of all verbs to the RRG conllu file

import csv
import time
from tqdm import tqdm

start = time.perf_counter()

with open('./rrgparbank/conllu/en_conllu.conllu', 'r', encoding='UTF-8', newline='\n') as infileRRG:
    with open('./rrgparbank/conllu/acc_en_conllu.conllu', 'w', encoding='UTF-8', newline='\n') as outfileRRG:
        reader = csv.reader(infileRRG, delimiter='\t')
        writer = csv.writer(outfileRRG, delimiter='\t')
        lines = list(reader)
        verbs = [lines[i] for i in range(len(lines)) if len(lines[i]) > 0 and lines[i][3] == 'VERB']
        adp = [lines[i] for i in range(len(lines)) if len(lines[i]) > 0 and lines[i][3] == 'ADP']

        # /// Adds sentence id to lines[i][8]
        count = 1
        for i in range(len(lines)):        
            if len(lines[i]) > 0:
                lines[i][8] = str(count)
            else:
                count += 1
        
        
        # /// Checking transitivity of verbs
        print('\n1. Checking transitivity of verbs...\n2. Replacing lines containing verbs...')
        progressbar = tqdm(total=len(lines)*3)
       
        for i in range(len(lines)):
            if len(lines[i]) > 0:
                

                if lines[i][3] == 'NOUN' or lines[i][3] == 'PROPN' or lines[i][3] == 'NUM' or lines[i][3] == 'PRON':
                    for j in range(len(verbs)):
                        if (lines[i][6] == verbs[j][0] and 'nsubj' not in lines[i][7]) and lines[i][8] == verbs[j][8]:
                            prop = '-'+lines[i][7]
                            verbs[j][9] ='transitive'
                            verbs[j][9] += prop.lower()
            progressbar.update()
        
            
        for i in range(len(lines)):
            if len(lines[i]) > 0:  
                if lines[i][3] == 'NOUN' or lines[i][3] == 'PROPN' or lines[i][3] == 'NUM' or lines[i][3] == 'PRON':      
                    for j in range(len(adp)):
                        if lines[i][0] == adp[j][6] and lines[i][8] == adp[j][8]:
                            for l in range(len(verbs)):
                                if verbs[l][8] == adp[j][8] and (lines[i][6] == verbs[l][0] and lines[i][8] == verbs[l][8]): 
                                    verbs[l][9] += '-'+adp[j][1].lower()
            progressbar.update()
        
        
        # /// Replacing verbs from the original file with checked ones.
        for i in range(len(lines)):
            if len(lines[i]) > 0:
                for j in range(len(verbs)):
                    if lines[i][3] == 'VERB':
                        if lines[i][0] == verbs[j][0] and lines[i][1] == verbs[j][1] and lines[i][2] == verbs[j][2] and lines[i][3] == verbs[j][3] and lines[i][8] == verbs[j][8]:
                            lines[i] = verbs[j]
            progressbar.update()
        progressbar.close()
        writer.writerows(lines)    
            