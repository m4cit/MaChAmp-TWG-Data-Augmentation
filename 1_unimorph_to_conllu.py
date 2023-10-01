# /////////////// Translate the original Unimorph file into the language of the conllu file

import os
import csv
import argparse
from tqdm import tqdm

# parser = argparse.ArgumentParser()
# parser.add_argument('-i', '--input', type=str, required=False, default='./unimorph/eng.txt', help='(OPTIONAL) Unimorph file input.')
# args = parser.parse_args()

try:  
    with open('./unimorph/eng.txt', encoding='UTF-8', newline='\n') as infile:
        with open('./unimorph/temp.txt', 'w', encoding='UTF-8', newline='\n') as tempout:
            reader = csv.reader(infile, delimiter='\t')
            writer = csv.writer(tempout, delimiter='\t')
            lines = list(reader) # ///creates lists of lines from the file

            print('\nProgress...')
            progressbar = tqdm(total=len(lines)) 
            
            for i in range(len(lines)):
                line2 = lines[i][1]
                line1 = lines[i][0]
                lines[i][0] = line2
                lines[i][1] = line1
                lines[i].append('\t')
                lines[i][3] = '_'
                
                
                try:
                    if lines[i][2] == 'ADJ;SPRL':
                        lines[i][2] = 'ADJ'
                        lines[i][3] = 'Degree=Sup'
                        i += 1
                    elif lines[i][2] == 'ADJ;CMPR':
                        lines[i][2] = 'ADJ'
                        lines[i][3] = 'Degree=Cmp'
                        i += 1    
                    elif lines[i][2] == 'ADJ':
                        lines[i][3] = 'Degree=Pos'
                        i += 1 
                    elif lines[i][2] == 'N;SG':
                        lines[i][2] = 'NOUN'
                        lines[i][3] = 'Number=Sing'
                        i += 1
                    elif lines[i][2] == 'N;PL':
                        lines[i][2] = 'NOUN'
                        lines[i][3] = 'Number=Plur'
                        i += 1
                    elif lines[i][2] == 'V;PST':
                        lines[i][2] = 'VERB'
                        lines[i][3] = 'Tense=Past|VerbForm=Fin'
                        i += 1
                    elif lines[i][2] == 'V;NFIN;IMP+SBJV':
                        lines[i][2] = 'VERB'
                        lines[i][3] = 'VerbForm=Inf|conj'
                        i += 1
                    elif lines[i][2] == 'V;PRS;3;SG':
                        lines[i][2] = 'VERB'
                        lines[i][3] = 'Tense=Pres|Number=Sing|Pers=3'
                        i += 1
                    elif lines[i][2] == 'V;V.PTCP;PRS':
                        lines[i][2] = 'VERB'
                        lines[i][3] = 'Tense=Pres|VerbForm=Part'
                        i += 1  
                    elif lines[i][2] == 'V;V.PTCP;PST':
                        lines[i][2] = 'VERB'
                        lines[i][3] = 'Tense=Past|VerbForm=Part'
                        i += 1
                except (IndexError):
                    i += 1
                    
                progressbar.update()
            progressbar.close()
            writer.writerows(lines)

    with open('./unimorph/temp.txt', encoding='UTF-8', newline='\n') as tempin:            
        with open('./unimorph/to_conllu_eng.txt', 'w', encoding='UTF-8', newline='\n') as outfile:
            writer = csv.writer(outfile, delimiter='\t')
            linesSet = sorted(set(tempin)) # /// removes duplicates
            
            for line in linesSet:
                outfile.write(f"{line}")

except(NameError):
    print("No filename specified!")
except(FileNotFoundError):
    print('\033[1m' +"| python uniToConllu.py 'unimorph/file.txt' |"+'\033[0m')
    print("File does not exist.")           

os.remove('./unimorph/temp.txt')
