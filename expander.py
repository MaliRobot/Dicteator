# -*- coding: utf-8 -*-
"""
Created on Thu Mar 17 16:46:05 2016

@author: misha
"""

import pickle, json
from entry_classes.vd_class import *

def load_pickle():
    infile = open('out/VD_default', 'rb')
    syn_dict = pickle.load(infile, fix_imports=True, encoding="ASCII", errors="strict")
    return syn_dict

def insert_type(types, res):
    types_list = []
    for t in types:
        if t not in res:
            res[t] = {}
        types_list.append(t)
    return res, types_list
    
def insert_form(forms, res, types_list, name, entry):
    forms = [x for x in forms if x.strip().startswith('-')]
    nforms = []
    for f in forms:
        f = f.split(' ', 1)[0]
        f = f.replace('˜', entry.title)
        f = f.strip(' .;')
        nforms.append(f)
    forms = nforms
    if name == '':
        return res
    name = name.replace('˜', entry.title)
    name = name.strip(' ;.d')
    for typ in types_list:
        for f in forms:
            if f in res[typ]:
                res[typ][f].append(name)
            else:
                res[typ].update({f:[name]})    
    return res


def save_json(dictionary, mode):
    if mode == 'norm':
        outfile = open('out/deaccented_main_entries.json' , 'w', encoding="utf8")
    elif mode == 'suffix':
        outfile = open('out/suffix_dict.json' , 'w', encoding="utf8")
    elif mode == 'sub':
        outfile = open('out/subentries.json' , 'w', encoding="utf8")
    json.dump(dictionary, outfile, ensure_ascii=False, indent=4, separators=(',', ': '))
    outfile.close()

def make_sufix_dict(syn_dict):
    res = {}
    for i in syn_dict:
        for key in syn_dict[i].keys:
            if key in syn_dict[i].type and key in syn_dict[i].forms:
                for sub_entr in syn_dict[i].type[key]:
                    res, types_list = insert_type(syn_dict[i].type[key][sub_entr], res)
                    if sub_entr in syn_dict[i].forms[key]:
                        try:
                            name = syn_dict[i].sub_entries[key][sub_entr]
                            name = list(name.keys())[0]
                        except KeyError:
                            name = syn_dict[i].title
                        forms = syn_dict[i].forms[key][sub_entr]
                        res = insert_form(forms, res, types_list, name, syn_dict[i])
    return res, 'suffix'
    
def make_normalized_entries(dictionary):
    normalized = {}
    for d in dictionary:
        copy = dictionary[d]
        copy.deaccentized_title_entry()
        print(copy.origin, copy.standard_title, copy.title)
        if copy.title != None:
            title = copy.title
            if title != '':
                normalized.update({title:copy.json_ready()})
    print('Made ', len(normalized), ' additional entries')
    return normalized, 'norm'
    
def make_entries_from_sub(dictionary):
    dict_subs = {}
#    i = 0
    for d in dictionary:
#        print(dictionary[d].keys)
        if len(dictionary[d].keys) > 1:
            for o in dictionary[d].sub_entries.keys():
                for q in dictionary[d].sub_entries[o]:
#                    i += 1
                    print(dictionary[d].sub_entries[o][q])
#    print(i)
    return dict_subs, 'sub'
    
def main():
    dictionary = load_pickle()
#    new_dictionary, mode = make_sufix_dict(dictionary)
    new_dictionary, mode = make_normalized_entries(dictionary)
#    new_dict_from_sub, mode = make_entries_from_sub(dictionary)
    save_json(new_dictionary, mode)
    
    
if __name__ == "__main__":
    main()

#    if syn_dict[i].standard_title != None:
#        j += 1
                        
