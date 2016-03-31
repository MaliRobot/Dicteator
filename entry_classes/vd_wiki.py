# -*- coding: utf-8 -*-
"""
Assumes dictionary is loaded from pickle. This is in order to be able to
extract other entries from original ones more easily. 

Created on Tue Mar 22 16:54:07 2016

@author: Misha
"""
import os, re
from collections import Counter
from entry_classes.vd_class import *
from copy import deepcopy
from tools.sr_lat2cyr2lat import *

i = 0
        
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
#        print(all_keys)
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
    return entry
    
def make_deaccented_entry(entry, dictionary):
    """
    Creates of a copy of entry with only difference that the title of a copy
    is without accents. If original entry title has no accents their titles
    would be identical and in this case new instance of entry would not be
    created.
    """
    dictionary[entry].set_standard_title()
    if dictionary[entry].standard_title != dictionary[entry].title or dictionary[entry].standard_title != None:
        new_entry = deepcopy(dictionary[entry])
        new_entry.deaccentized_title_entry()

        if new_entry.title != None:
            title = new_entry.title
            if new_entry != '' and new_entry.title not in dictionary.keys():
                dictionary.update({title:new_entry})
    return dictionary
    
def make_subentries_of_entry(entry, dictionary):
    """
    
    """
    global i
    if len(dictionary[entry].keys) > 1:
        for k in dictionary[entry].sub_entries:
            try:
                for se in dictionary[entry].sub_entries[k]:
                    title = list(dictionary[entry].sub_entries[k][se].keys())[0]
                    if title not in dictionary:
                        if '˜' in title:
                            title = title.replace('˜', dictionary[entry].title)
                        if title.endswith(' d'):
                            title = title[:-2]
                        new_entry = Entry(title)
                        new_entry.origin = entry
                        dictionary[entry].children.append(title)
                        if k in dictionary[entry].forms:
                            if se in dictionary[entry].forms[k]:
                                new_entry.forms = {k:{se:dictionary[entry].forms[k][se]}}
                        if k in dictionary[entry].type:
                            if se in dictionary[entry].type[k]:
                                new_entry.type = {k:{se:dictionary[entry].type[k][se]}}
                        if k in dictionary[entry].examples:
                            if se in dictionary[entry].examples[k]:
                                new_entry.examples = {k:{se:dictionary[entry].examples[k][se]}}
                        if k in dictionary[entry].meanings:
                            if se in dictionary[entry].meanings[k]:
                                new_entry.meanings = {k:{se:dictionary[entry].meanings[k][se]}}
                        if k in dictionary[entry].sub_entries:
                            new_entry.sub_entries = {k:{}}
                            for se2 in dictionary[entry].sub_entries[k]:
                                if dictionary[entry].sub_entries[k][se2] != dictionary[entry].title or se != se2:
                                    new_entry.sub_entries[k].update({se:dictionary[entry].sub_entries[k][se2]})
                        if k in dictionary[entry].phrases:
                            if se in dictionary[entry].phrases[k]:
                                new_entry.phrases = {k:{se:dictionary[entry].phrases[k][se]}}
                        new_entry.keys = [k]
                        dictionary[title] = new_entry
                        i += 1
                        new_entry.set_standard_title()

                        if new_entry.standard_title != None and new_entry.standard_title not in dictionary:
                            one_more_entry = new_entry
                            one_more_entry.title = new_entry.standard_title
                            one_more_entry.origin = entry
                            new_entry.children.append(one_more_entry.title)
                            dictionary[one_more_entry.title] = one_more_entry
                            i += 1
            except KeyError as e:
                print('error', e)

    return dictionary
    
def expand_dictionary(dictionary):
    global i
    print(len(dictionary))
    entries = list(dictionary.keys())
    for e in entries:
        dictionary = make_subentries_of_entry(e, dictionary)
    for e in entries:
        dictionary = make_deaccented_entry(e, dictionary)
    print('subentries', i)
    print(len(dictionary))
    return dictionary
    
def concat_entry(strings):
#    print(strings)
    final = ''.join(strings)
#    final = transliterate(final, True)
#    print('sss', final, 'ddd')
    return final