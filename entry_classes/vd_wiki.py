# -*- coding: utf-8 -*-
"""
Created on Tue Mar 22 16:54:07 2016

@author: Milosh
"""
import os, re
from collections import Counter
from entry_classes.vd_class import *
        
def get_wiki_type(types):
    for typ in types:
        if typ in ['м','ж','с', 'гл им', 'м/ж', 'мн', 'зб', 'јд']:
            return 'Именица'
        if typ in ['учест', 'повр', 'несвр', '(не)свр', 'свр', 'прел']:
            return 'Глагол'
        if typ in ['рад', 'поим прид', 'присв прид', 'прид']:
            return 'Придев'
        if typ in ['прил',  'прил сад']:
            return 'Прилог'
        if typ in ['предл']:
            return 'Предлог'
        if typ in ['зам']:
            return 'Заменица'
        if typ in ['узвик']:
            return 'Узвик'
        if typ in ['бр']:
            return 'број'
        if typ in ['везн']:
            return 'Везник'
        if typ in ['реч.']:
            return 'речца' 
        return None

def find_duplicate_keys(d, no_of_dup):
    """
    Read dictionary keys and figure out which are duplicates. Store them in a
    txt file. If the file exists it skips this step and reads the file.
    """
    if os.path.isfile("duplicates.txt"):
        duplicates = open("duplicates.txt", "r", encoding="utf8").read().split()
        return duplicates
    else:
        all_keys = d.keys()
        all_keys_list = [re.sub(r'\{[^}]*\}', '', x).strip() for x in all_keys]
        ordered_keys = Counter(all_keys_list).most_common(no_of_dup)
        duplicates = ([x[0] for x in ordered_keys if x[1] > 1])
        outfile = open("out/duplicates.txt", "w", encoding="utf8")
        outfile.write("\n".join(duplicates))
        return duplicates
        
def get_type_of_entry(dictionary, s, entry):
    """
    Transfering entries from parsing class to wiki class.
    """
    global i
    if len(dictionary[s].keys) == 1:
        if len(dictionary[s].type) > 0:
#            print(dictionary[s]['elements']['(0, 0)']['type'])
            pass
        else:
            if dictionary[s].other != []:
                pass
            else:
#                print(s)
                pass
#                i += 1
    else:
        pass
#        for k in dictionary[s]['keys']:
#            k = str(k)
#    #        print(dictionary[s]['elements'])
#            if 'type' in dictionary[s]['elements'][k]:
#                print(dictionary[s]['elements'][k]['type'])
    return entry
    
def make_deaccented_entry(entry, dictionary):
    copy = dictionary[entry]
    copy.deaccentized_title_entry()
#    print(copy.origin, copy.standard_title, copy.title)
    if copy.title != None:
        title = copy.title
        if title != '' and copy.title not in dictionary.keys():
            dictionary.update({title:copy})
    dictionary[entry].origin = copy.title
    return dictionary
    
def make_subentries_of_entry(entry, dictionary):
    if len(dictionary[entry].keys) > 1:
        print(dictionary[entry].sub_entries)
    return dictionary
    
def expand_dictionary(dictionary):
    print(len(dictionary))
    entries = list(dictionary.keys())
    for e in entries:
        dictionary = make_deaccented_entry(e, dictionary)
        dictionary = make_subentries_of_entry(e, dictionary)
    print(len(dictionary))
    return dictionary