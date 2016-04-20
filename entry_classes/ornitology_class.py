# -*- coding: utf-8 -*-
"""
Created on Tue Feb 23 20:15:28 2016

@author: Misha
"""


from collections import OrderedDict 
from bs4 import BeautifulSoup, NavigableString
import re

MIGRATION = ['↓','↕','→','←','↔', '†', '*']


class Entry():
    '''
    Entry class to contain attributes of the entries from the Ornitološki rečnik
    '''
    def __init__(self, name):
        self.genus = name
        self.discover = None
        self.species = {}
        self.latin = None
        self.serbian = None
        self.num_species = 0
    def set_discover(self, discover):
        self.discover = discover
    def set_latin(self, latin):
        self.latin = latin
    def set_serbian(self, serbian):
        self.serbian = serbian
    def set_species(self, migration, latin, serbian):
        self.num_species += 1
        self.species[self.num_species] = [migration, latin, serbian]
    def json_ready(self):
        return {self.genus : {'discoverer': self.discover, 'latin name': self.latin, 'serbian name' : self.serbian, 'species' :     self.species}}
        
def process_discover(discover):
    '''
    Process the name of the discoverer.
    '''
    if discover == None:
        return []
    discover = [x[0].strip() for x in discover]

    if len(discover) > 0:
        if discover[-1].endswith('–'):
            discover[-1] = discover[-1].strip().rstrip('–')
        elif discover[-1].endswith('.'):
            discover[-1] = discover[-1].split('.')[0]
        discover[-1] = discover[-1].strip()   

    discover = ' '.join(discover)
#    print('dis', discover)
    return discover
    
def process_latin(latin):
    '''
    Process Latin names of the species.
    '''
    if latin == None:
        return []
    latin = [(x[0].strip(), x[1]) for x in latin]
    
    if latin != []:
        latin[0] = (latin[0][0].split('–')[1], latin[0][1])
       
    if len(latin) > 1:
        latin[-1] = (latin[-1][0].split('–')[0], latin[-1][1])
    latin = [x for x in latin if x[0] not in ['', 'f.', '.', 'f']]
    latin[0] = (latin[0][0].lstrip('f. '), latin[0][1])
    
    latin = ' '.join([x[0] for x in latin])
    latin = latin.strip()
    return latin
    
def process_serbian(serbian):
    '''
    Process Serbian names of the species.
    '''
    srb_final = []

    if serbian == None or serbian == [] or serbian == ['']:
        return []
    serbian = [x for x in serbian if x[0] not in ['', '.']]
    serbian = [x for x in serbian if x[0] != '.']
    serbian = [(x[0].strip(), x[1]) for x in serbian]
    if serbian != [] or serbian != ['']:
        serbian[0] = (serbian[0][0].split('–')[1], serbian[0][1])

    srb_str = ' '.join([x[0] for x in serbian])
    srb_lst = srb_str.replace('),', ')//').split('//')

    bold = [x[0] for x in serbian if x[1] == 0]
    rare = [x[0] for x in serbian if x[1] == 1]
    for sl in srb_lst:
        sl = sl.strip()

        ref = re.findall('\((.*?)\)', sl)[0]
        bird = re.sub(r'\([^)]*\)', '', sl)
        ref = ref.strip()
        bird = bird.strip(' .')
        
        if bird in bold:
            srb_final.append([bird, ref, 'frequent'])
        elif bird in rare:
            srb_final.append([bird, ref, 'rare'])
        else:
            srb_final.append([bird, ref, 'normal'])
    return srb_final
        
def get_genus(gen_list):
    '''
    Process information on genus which includes discoverer, latin word and
    serbian words for the genus.
    '''
    discover = latin = serbian = None
    name = gen_list[0]
    idx = [i for i, x in enumerate(gen_list) if '–' in x[0]]
    if len(idx) == 1:
        discover = gen_list[:idx[0]+1]
        latin = gen_list[idx[0]:]
        serbian = []
    if len(idx) == 2:
        discover = gen_list[:idx[0]+1]
        latin = gen_list[idx[0]:idx[1]+1]
        serbian = gen_list[idx[1]:]

    entry = Entry(name[0])    
    
    discover = process_discover(discover)

    latin = process_latin(latin)
    serbian = process_serbian(serbian)
#    print(discover)
    discover = discover.replace(name[0], '').strip()    
    
    entry.set_discover(discover)
    entry.set_latin(latin)
    entry.set_serbian(serbian)

    return entry 
        
def get_species(species, entry):
    '''
    Process each species from the list of string. Get names and references for
    Serbian names and get all Latin names.
    '''
    for s in species:
        serbian = []
        latin = []
        text = ' '.join([x[0] for x in s])
        text = text.strip()
        migration = text[0]

        latin.append(re.findall('[A-Z].*?\(', text[1:])[0])
        text = text[1:].replace(latin[0], '')
        latin.append(re.findall('.*?\)', text)[0])
        
        text = text.replace(latin[-1], '')
        t = re.findall('\(.*?(?:\? \)|\?\))', text)
        if t != []:
            text = text.replace(t[0], '')
        text = text.lstrip(' ,–')
        text_lst = text.split(',')
        bold = [x[0] for x in s if x[1] == 0]
        rare = [x[0] for x in s if x[1] == 1]
        for sl in text_lst:
            ref = re.findall('\((.*?)\)', sl)
            bird = re.sub(r'\([^)]*\)', '', sl)            
            bird = bird.rstrip(' .')
            bird = bird.strip()
            
            ref = [x.strip() for x in ref]
            ref = ''.join(ref)
            ref = ref.replace('  ', ' ')
            
            if bird in bold:
                serbian.append([bird, ref, 'frequent'])
            elif bird in rare:
                serbian.append([bird, ref, 'rare'])
            else:
                serbian.append([bird, ref, 'normal'])
                
        latin = ' '.join(latin)
        latin = latin.replace(' .', '.')
        latin = latin.replace(' ,', ',')
        latin = latin.replace('  ', ' ')
        latin = latin.replace('   ', ' ')
        
        entry.set_species(migration, latin, serbian)
    return entry

def get_entries(para):
    '''
    We know in advance that species in the genus entry are devided by migration
    marker. We use it for extracting species. We also know that genus comes in
    the beginning of the paragraph and we can extract it by grabbing the 
    part of the string before first migration marker.
    Once we devide genus and species parts we pass them for further processing
    accordinglly.
    '''
    idx = []
    species = []
    print(para, '\n')
    for i,p in enumerate(para):
        for m in MIGRATION:
            if m in p[0]:
                idx.append(i)
    print(idx)
    if len(idx) == 0:
        genus = para
    elif len(idx) == 1:
        genus = para[:idx[0]]
        species = [para[idx[0]:]]
    elif len(idx) == 2:
        genus = para[:idx[0]]
        species = [para[idx[0]:idx[1]], para[idx[1]:]]
    else:
        genus = para[:idx[0]]
        for i in range(len(idx)):
            if i == len(idx) - 1:
                species.append(para[idx[i]:])
            elif i == 0:
                species.append(para[idx[0]:idx[1]])
            else:
                species.append(para[idx[i]:idx[i+1]])
    entry = get_genus(genus)
    entry = get_species(species, entry)
    return {entry.genus : entry}
        
def make_entries(contents):
    """
    Making instances of Entry class.
    First we need to tranlsate html code into more practical structure.
    We convert html code into a serie of tuples each containing a string
    and information on font style (bold, italic or normal) because it
    determines type of data we are working with (for example entry titles
    are always in bold text). We concatenate adjecent string of the same
    font style.
    """
    entries = OrderedDict()
    for p in contents:
        para = []
        for s in p:
#            print(s, '\n')
            if not isinstance(s, NavigableString) and s.get_text() != None:
                try:
                    if 'bold' in s['style']:
                            para.append((s.get_text(), 0))
                    elif 'italic' in s['style']:
                            para.append((s.get_text(), 1))
                    else:
                            para.append((s.get_text(), 2))
                except KeyError:
                        para.append((s.get_text(), 2))
            else:
                if s != '' or s != ' ':
                    para.append((s, 2))

        para = [x for x in para if x[0] != '\xa0']
        para = [x for x in para if x[0] != '']
        para = [x for x in para if x[0] != ' ']
        if para == []:
            continue
        parsed_entry = get_entries(para)
        entries.update(parsed_entry)
        
    return entries
    
