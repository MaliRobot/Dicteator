# -*- coding: utf-8 -*-
"""
Created on Tue Aug 11 17:16:06 2015

@author: misha
"""

import json, re, os, pickle, codecs
from sys import argv
from tools.sr_lat2cyr2lat import *
from collections import OrderedDict, Counter
from entry_classes.sinonimi_wiki import *

def load_dict(source):
    """
    Load Recnik Sinonima from JSON.
    """
    file = open(source, 'r', encoding="utf8")
    dictionary_json = json.load(file, object_pairs_hook=OrderedDict)
    return dictionary_json
                    
def make_entries(dictionary, to_text, to_pickle, debug, breakpoint, lat = False):
    """
    Iterate over dictionary in order of entries. If entry is a duplicate, put 
    the object that represents it in the list which contains all objects with
    the same duplicate name. 
    """
    dict_name = next(iter(dictionary.keys()))

    if debug:
        names = []
    entries = {}
    duplicates = find_duplicate_keys(dictionary, len(dictionary[dict_name]), dict_name)
    for i, s in enumerate(dictionary[dict_name].keys()):
        if debug:        
            names.append(" ".join([x for x in dictionary[dict_name][s].keys()]))
        entry_name = re.sub(r'\([^)]*\)', '', s).strip()
        entry = Entry(entry_name, lat)
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
        typ = list(dictionary[dict_name][s].keys())[0] 
        entry.set_type(typ)
        """
        Iterate over the meanings of the dictionary entry. Only 'reference'
        subdictionary is not ordered, so we use this fact to distinguish
        between them. Pass submeaning for further processing.
        """
        for j, body in enumerate(dictionary[dict_name][s][typ]):
            if isinstance(body, OrderedDict):
                for meaning in dictionary[dict_name][s][typ][0]:
                    entry.increase_key()
                    extract_meaning(dictionary[dict_name][s][typ][0][meaning], entry, dictionary, skey = meaning)
            else:
#                it's reference which is not needed because it contains no data
                pass

        
        """
        Enable for debugging
    
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
    print(argv)
    if 't' in argv:
        to_text = True
    if 'p' in argv:
        to_pickle = True
    if 'j' in argv:
        to_json = True
    if 'd' in argv:
        debug = True
    if 'l' in argv:
        lat = True
    if 's' in argv:
        source = SHORT
    else:
        source = FULL
    print(source, to_text, debug, lat)
    breakpoint = None
    for a in argv:
        if a.isdigit():
            breakpoint = a
    dictionary_json = load_dict(source)
    if debug:
        print (len(dictionary_json[dict_name]))
    make_entries(dictionary_json, to_text, to_pickle, debug, breakpoint, lat)

if __name__ == "__main__":
    main(argv)