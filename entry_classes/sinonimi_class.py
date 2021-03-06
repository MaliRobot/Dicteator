# -*- coding: utf-8 -*-
"""
Created on Tue Jan 12 16:43:55 2016

Run parser.py with to_text param set to True

@author: Milosh
"""

import re
from tools.sr_lat2cyr2lat import *
from collections import OrderedDict 

class Entry:
    """
    Class to store, format and return dictionary entries.
    """
    def __init__(self, title, typ = None, meaning = [], delimiter = 'split', 
                 reference = {'reference_type': 'orginal', 'page': 0}):
        self.title = title
        self.type, meaning = self.process_type(typ, meaning)
        self.reference = reference
        self.meaning = self.process_meaning(meaning, delimiter)       
#        print  'THIS:::::',title, 'Type>>>>>', typ, 'MEANING::::::', meaning, '\n'
#        print self.meaning.update(self.reference), title
    def get_title(self, trans = None):
        if trans == None:
            return self.title
        elif trans == 'cyr':
            return syn_transliterate(self.title)
    def get_type(self):
        return self.type
    def get_meaning(self, trans = None):
        if trans == None:
            return self.meaning
        else:
            if trans == 'cyr':
                for m in self.meaning:
                    for k in self.meaning[m]:
                        for n in self.meaning[m][k]:
                            if isinstance(self.meaning[m][k][n], str):
                                self.meaning[m][k][n] = syn_transliterate(self.meaning[m][k][n])
                            elif isinstance(self.meaning[m][k][n], dict): 
                                for key in self.meaning[m][k][n].keys():
                                    if isinstance(self.meaning[m][k][n][key], list):
                                        for i in range(len(self.meaning[m][k][n][key])):
                                            self.meaning[m][k][n][key][i] = syn_transliterate(self.meaning[m][k][n][key][i])
                                    elif isinstance(self.meaning[m][k][n][key], str):
                                        self.meaning[m][k][n][key] = syn_transliterate(self.meaning[m][k][n][key])
                            elif isinstance(self.meaning[m][k][n], list):
                                lst = []
                                for w in self.meaning[m][k][n]:
                                    lst.append(syn_transliterate(w))
                                self.meaning[m][k][n] = lst
            return self.meaning
    def get_reference(self):
        return self.reference
    def process_type(self, typ, meaning):
        abbs = set([u'anat.', u'anatom.', u'arh.', u'arheol.', u'aug.',
                    u'biol.', u'bot.', u'crkv.', u'dem.', u'ekon.',
                    u'ekonom.', u'ekpr.', u'ekspr.', u'ekspri.', u'euf.', 
                    u'fam.', u'fig.', u'fil.', u'filoz.', u'fiz.', u'form.', 
                    u'geog.', u'geogr.', u'geol.', u'gram.', u'hem.', u'hip.', 
                    u'hrv.', u'iron.', u'ist.', u'izr.', u'komp.', u'lat.',
                    u'lingv.', u'mat.', u'med.', u'mit.', u'muz.', u'nar.', 
                    u'pesn.', u'pog.', u'pol.', u'pravn.', u'psih.', u'refl.',
                    u'reg.', u'ret.', u'sl.', u'sport.', u'tehn.', u'v.', 
                    u'var.', u'vet.', u'voj.', u'vojn.', u'vulg.', u'zool.',
                    u'žarg.', u'šalj.'])
                             
        filtered_types = []
        proc = [x.strip() for x in typ.split() if x != '']
    
        for p in proc:
            if p in abbs:
                meaning = p + ' ' + meaning
            else:
                filtered_types.append(p)
    
        return filtered_types, meaning
        
    def process_meaning(self, meaning, delimiter):
        """
        input: meaning of the entry as a raw string to be processed
        output: split different meanings and submeanings within each of them, 
        create tags and attach them to the words output format example: 
        {1: m1 (tag1) (tag2), m2, ..., mn, {ref.1: m1, m2 (tag1), ..., mn},
        2: m1, m2, mn, {sub.2: m1, ..., mn}, ...}
        'split' is used as a delimiter.        
        """
        if meaning == None: 
            return None
        meanings = {}
        if delimiter in meaning:          
            split_means = meaning.split('split') #[1:]
            for s in range(1, len(split_means)):  
                meanings[s] = switch(split_means[s]) 
            return meanings
        else:
            meanings[1] = switch(meaning)
        return meanings
    def __str__(self, trans = None):
        string = self.get_title(trans) + '\n'
        string = string + u'Type: ' + ' '.join(self.get_type()) + u'\n'
        string = string + ''.join(str(self.get_reference())) + u'\n'
        string = string + ''.join(str(self.get_meaning(trans))) + u'\n'
#        for key, value in self.get_meaning().iteritems():
#            string2 = u'Meaning ' + str(key).encode('utf-8') + u': ' + str(value) + u'\n'
#            string = string + string2
        string = ('').join(string)
        return string.encode('utf-8')           
    def __repr__(self):
        return self.__class__.__name__, self.title, self.type, self.meaning
    def json_ready(self, trans):
        return {self.get_title(trans): {str(self.type) : [self.get_meaning(trans), str(self.get_reference())]}}
        
def syn_transliterate(string, to_latin = False):
    if to_latin == False:
        script = AZBUKA
    else:
        script = ABECEDA
    skip = False
    latin = False
    new = ''   
    for i, s in enumerate(string):
        if skip == True:
            skip = False
            continue  
        elif s == '#':
            latin = True
            continue
        elif latin == True:
            new = new + s
            latin == False
        elif s.isalpha() == False:
            new = new + s
        else:
            low_s = s.lower()
            if low_s == 'n' or low_s == 'd' or low_s == 'l': 
                try:
                    n = string[i+1]
                    low_n = n.lower()
                    if (low_s == 'n' and low_n == 'j')\
                    or (low_s == 'd' and low_n == 'ž')\
                    or (low_s == 'l' and low_n == 'j'):
                        if low_n == 'ž':
                            n = u'ž'
                        s = s + n
                        skip = True                        
                except:
                    pass
            if s in script.keys():
                new = new + script[s]
            elif s == '#':
                latin == True
            else:
                new = new + s
    return new        
        
def switch(split_means):
    """
    Wrapper that connects class method 'process_meaning' with 'format_trails' and 
    'format_meaning'. Its purpose is to further split units of the meaning of the 
    entry till it reaches their basic constituents. Most importantly, it processes
    trailing parts of the meaning (everything after '-' sign).
    """
    mean, subm = split(split_means)
    if subm:
        subm = format_trails(subm)
        meaning = format_meaning(mean) 
        meaning.update(subm)
    else:
        meaning = format_meaning(mean)
    return meaning

def format_trails(sub):
    """
    input: submeaning as a string
    output: dictionary with relation to the entry as the key and meanings as values.
    Values are strings which are filtered for description and categories by
    calling format_meaning function.
    """
    if sub == []:
        return None

    d = {}
    keys = {'- reg':'regional','- sl':'similar meaning','- up':'compare', 
            u'- suž':'narrow meaning', u'- žarg':'jargon', '- fig':'figurative',
            '- fam':'familiarly', '- euf':'eufemizam', '- nar':'popularly', 
            '- arh':'archaic', '- izr':'expression', '- ret':'rare', 
            '- v': 'see'}
            
    abb = re.compile('\-\D{1,5}[:|.]')
    pref = abb.findall(sub)
    pointers = [x for x in range(len(sub)) if sub[x:x+2] == '- ']
    if len(pointers) > 1:
        for s in range(1, len(pointers)):
            trail = sub[pointers[s-1]:pointers[s]]
            trail = re.sub(pref[s-1], '', trail)
            k = keys[pref[s-1][:-1]]
            d[k] = format_meaning(trail.split(','))
    else:
        trail = re.sub(pref[0], '', sub)
        #print sub
        k = keys[pref[0][:-1]]
        d[k] = format_meaning(trail.split(','))
    return d
    
def split(meaning):
    """
    split meaning but not the submeaning (categories: similar, compare, narrow 
    sense - 'sl.', 'up.' i 'suž.')
    """
    r = re.compile(r'(?:[^,(]|\([^)]*\))+')
    abb = re.compile(r'\-\D{1,5}[:|.]')
    sub = abb.findall(meaning) 
    if sub:
        try:
            idx = re.search(re.escape(sub[0]), meaning).start()
        except AttributeError:
            idx = meaning.index('-')
        split = r.findall(meaning[:idx])
        return split, meaning[idx:]
    else:
        split = r.findall(meaning)
    return split, ''
    
def format_meaning(meanings):
    """
    input: meaning of the entry as a list
    output: formatted meaning as a dictionary of dictionaries
    - This is a two step process:
    1)
        Rearrange each particular string in the list so that 'v.' ('v.' which 
        marks that we refer to the other entry in the dictionary) goes
        to the front of the string followed by the numbers marking particular
        meaning the entry that is refered to - all this if such reference 
        exists. Then comes the word followed by the tags associated with this 
        word which are put into the paranthesis.  
    2)
        Finally, we put extracted data into dictionary form with descriptor
        as a key and data as values. There are three descriptors:
        a. Form
        b. Description
        c. Categories
        First we look if there are any other elements beside Form, if not, we 
        simply return it. Otherwise, we look for words in paranthesis, which
        is Description we are looking for. We remove it from original data
        and start looking for Categories which we can easily recognize because
        they all end with coma. Finally, all what is left are Forms, which can 
        consist of multiple words, but we maintain their order. We return
        all this as dictionary with all values and their keys we could find.
        
    """
    # 1)
    synonyms = {}
    terms = []
    for i in range(len(meanings)):
        if re.search(r'[0-9]. i [0-9].', meanings[i]):
            meanings[i] = meanings[i].replace(' i ', ' ')
        elements = meanings[i].split()
        words = ''
        tags = ''
        nums = ''
        latin = False
        for el in elements:         
            if el.endswith('.') and not el.startswith('(lat') and latin == False: 
                if el[0].isalpha():
                    if el != 'v.':
                        tags = tags + ' ' + el
                    else:
                        nums = el + nums
                else:
                    nums = nums + ' ' + el
            else:
                if el.startswith('(lat'):
                    latin = True
                if el.endswith(')') and latin == True:
                    latin = False
                words = words + ' ' + el
        string = nums + words + tags
        terms.append(string.lstrip())  
    # 2)
    for i, term in enumerate(terms):
        para = re.findall(r'\([^)]*\)', term)
        form = [] 
        description = [] 
        categories = []
        if ' ' in term:
            if para != []:
                for p in para:
                    term_no_para = term.replace(p,'')
                    term = term_no_para
                description = " ".join(para)
            w = re.findall('\([^\)]*\)|\[[^\]]*|\S+', term)
            categories = [x for x in w if x.endswith('.') and x[0].isalpha()]
            form = [x for x in w if x not in categories]
            if form:
                form = ' '.join(form)
            synonyms[i] = {'form': form, 'description': description, 'categories': categories}
            synonyms[i] = {k:v for k,v in synonyms[i].items() if v != []}
        else:
            synonyms[i] = {'form': term}   
    return synonyms  
    
def make_entries(contents):
    """
    Making instances of Entry class.
    """
    # for counting entries - uncomment
    #words = []
    delimiter = 'split' 
    dictionary = OrderedDict()
    for c in contents:
        c = [x for x in c if x != '']
        if c[1].isdigit():
            c[0] = c[0] + ' (' + c[1] + ') '
            c = [c[0]] + c[2:]
        if len(c[2:]) > 1:
            meaning = ' '.join(c[2:])
        else:
            meaning = c[-1]
        dictionary[c[0]] = Entry(c[0], c[1], meaning, delimiter)
        # for counting entries - uncomment
        #words.append(c[0])
    # meant only to find duplicates
    #print Counter(sorted(words)).most_common(25)
    return dictionary