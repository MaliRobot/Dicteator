# -*- coding: utf-8 -*-
"""
Created on Tue Aug 11 17:16:06 2015

@author: misha
"""

import json, re, os, pickle, codecs
import sys
from getopt import getopt
from tools.sr_lat2cyr2lat import *
from collections import OrderedDict, Counter
#from entry_classes.sinonimi_wiki import *
from entry_classes.vd_class import *
from entry_classes.vd_wiki import *

def load_json(source):
    """
    Load dictionary from JSON.
    """
    file = open(source, 'r', encoding="utf8")
    dictionary_json = json.load(file, object_pairs_hook=OrderedDict)
    dictionary_json = dictionary_json[next(iter(dictionary.keys()))]
    return dictionary_json
                    
def load_pickle(source):
    """
    Load dictionary from pickle.
    """
    file = open(source, 'rb')
    dictionary_pickle = pickle.load(file, fix_imports=True, encoding="ASCII", errors="strict")
    return dictionary_pickle                    
                    
def make_entries(dictionary, to_text, to_json, to_pickle, debug, breakpoint, lat = False):
    """
    Iterate over dictionary in order of entries. If entry is a duplicate, put 
    the object that represents it in the list which contains all objects with
    the same duplicate name. 
    """
    dictionary = expand_dictionary(dictionary)    
    
    if debug:
        names = []
    entries = {}
    duplicates = find_duplicate_keys(dictionary, len(dictionary))
    for i, s in enumerate(dictionary.keys()):
        if debug:        
            names.append(" ".join([x for x in dictionary[s].keys()]))
        entry_name = re.sub(r'\([^)]*\)', '', s).strip()
        entry_name = re.sub(r'\s\{\d}', '', s).strip()
    
#        sinonimi
#        entry = Entry(entry_name, lat)
        entry = dictionary[s]

        if len(entry.keys) > 1: # delete this after testing
            if entry_name in duplicates:
                entry.not_unique()
                if entry_name in entries:
                    entries[entry_name].append(entry)                
                else:
                    entries[entry_name] = [entry]
            else:
                entries[s] = entry     
        
        """
        Getting the type of the word
        """
        entry = get_type_of_entry(dictionary, s, entry)
    
        """
        Stop early for debugging
        """
        if breakpoint:
            if i == breakpoint:
                break

    """
    To print the entries to a text file.
    """
    if to_text:
        out = codecs.open('out/test0.txt', 'w', encoding = 'utf8')
        for k in entries:
            out.write('\n{{-start-}}\n')
            out.write('\'\'\'%s\'\'\'\n' % (transliterate(k, lat)))
            if isinstance(entries[k], list):
                string = []
                for i, e in enumerate(entries[k]):
                    if i == 0:
                        string.extend(e.to_wiki(True, False))
                    elif i == (len(entries[k]) - 1):
                        string.extend(e.to_wiki(False, True))
                    else:
                        string.extend(e.to_wiki())
                
                string = concat_entry(string)
                out.write(string)
            elif isinstance(entries[k], object):
                string = concat_entry(entries[k].to_wiki(True, True))
                out.write(string)
            out.write('\n{{-stop-}}\n')
        out.close()            
            
    """
    To print the entries to the console.
    """
    if debug:
        print (Counter(names))
        for k in entries:
            if isinstance(entries[k], list):
                for i in range(len(entries[k])):
                    entries[k][i].debug()
            else:
                entries[k].debug()
    """
    To Pickle
    """
    if to_pickle:
        pickle.dump(entries, open('out/synonymsX', 'wb')) 
    
    print('Finish')

def main(argv):
    to_text = to_pickle = to_json = debug = lat = False
    print(sys.argv)
    source = ''
    try:
        opts, args = getopt(sys.argv[1:],"hi:",["ifile="])
    except GetoptError:
        print('reader.py -i <inputfile> t p j d l')
        sys.exit()

    for opt, arg in opts:
        if opt == '-h':
            print('reader.py -i <inputfile> t p j d l')
            sys.exit()
        elif opt in ("-i", "--ifile"):
            source = arg
            
    for arg in sys.argv:
        print(arg)
        if arg == 't':
            to_text = True
        if arg == 'p':
            to_pickle = True
        if arg == 'j':
            to_json = True
        if arg == 'd':
            debug = True
        if arg == 'l':
            lat = True

    print('Reading file: ', source, ' Exporting wiki entries: ', to_text, ' Debugging: ', debug, 'Latin: ', lat)
    breakpoint = None
    for a in sys.argv:
        if a.isdigit():
            breakpoint = a
    if source.endswith('.json'):
        dictionary = load_json(source)
    else:
        dictionary = load_pickle(source)
    if debug:
        print (len(dictionary[dict_name]))
    
    if source != '':   
        make_entries(dictionary, to_text, to_json, to_pickle, debug, breakpoint, lat)
    else:
        sys.exit()

if __name__ == "__main__":
    main(sys.argv)