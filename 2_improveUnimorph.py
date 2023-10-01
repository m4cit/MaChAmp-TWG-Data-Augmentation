# /////////////// Looks up all verbs from the Unimorph file successively on dictionary.com, and categorizes them into transitive and intransitive

import csv
import requests
import os
from bs4 import BeautifulSoup
from tqdm import tqdm

url = 'https://www.dictionary.com/browse/'

with open('./unimorph/to_conllu_eng.txt', 'r', newline='\n', encoding='UTF-8') as infile:            
    with open('./unimorph/acc_to_conllu_eng.txt', 'w', newline='\n', encoding='UTF-8') as outfile:
        with open('./unimorph/tempfile.txt', 'w', newline='\n', encoding='UTF-8') as tempfile:
            reader = csv.reader(infile, delimiter='\t')
            writer = csv.writer(outfile, delimiter='\t')
            tempwriter = csv.writer(tempfile, delimiter='\t')
            lines = list(reader)
            verbs = [lines[i] for i in range(len(lines)) if lines[i][2] == 'VERB']
            
            tempwriter.writerows(verbs)
            
            # /// writing all lines != 'VERB' to new file
            for i in range(len(lines)):
                if lines[i][2] != 'VERB':
                    writer.writerow(lines[i])

# /// identifying the number of verbs for progressbar 'total'                    
with open('./unimorph/tempfile.txt', 'r', newline='\n', encoding='UTF-8') as infile:
    listreader = csv.reader(infile, delimiter='\t')
    lines = list(listreader)
    lenLines = len(lines)

# /// Checking dictionary.com entries for all verbs from the tempfile        
with open('./unimorph/tempfile.txt', 'r', newline='\n', encoding='UTF-8') as infile:
    with open('./unimorph/acc_to_conllu_eng.txt', 'a', newline='\n', encoding='UTF-8') as outfile:
        reader = csv.DictReader(infile, delimiter='\t', fieldnames=['word','base form','type','properties'], lineterminator='\n')
        writer = csv.DictWriter(outfile, delimiter='\t', fieldnames=['word','base form','type','properties'], lineterminator='\n')
        
        print('\nProgress...')
        progressbar = tqdm(total=lenLines) 
        
        for l in reader: 
            # /// url + word
            page = requests.get((url+l['base form']))
            soup = BeautifulSoup(page.content, 'html.parser')   
            root = soup.find(id='root')
            wordtype = root.find_all('span', class_='luna-pos')
        
            if 'verb (used without object)' and 'verb (used with object)' in str(wordtype):
                l['properties'] = l['properties']+'|intransitive and transitive'
            elif 'verb (used without object)' in str(wordtype):
                l['properties'] = l['properties']+'|intransitive'
            elif 'verb (used with object)' in str(wordtype):
                l['properties'] = l['properties']+'|transitive'
            else:
                l['properties'] = l['properties']
            progressbar.update()
            writer.writerow(l)
        progressbar.close()

# Removing temporary file
os.remove('./unimorph/tempfile.txt')            
    