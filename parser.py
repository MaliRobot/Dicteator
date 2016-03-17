# -*- coding: utf-8 -*-
"""
Parse 

Created on Thu Apr 16 15:09:09 2015

@author: misha
"""

# recnik sinonima
#from entry_classes.sinonimi_class import *
# recnik vojvodjanskih 
from entry_classes.vd_class import *
# ornitoloski recnik
#from entry_classes.ornitology_class import *
from collections import Counter, OrderedDict
from bs4 import BeautifulSoup, NavigableString
import os, json, pickle
from sys import argv
#from sr_lat2cyr2lat import *

SOURCE = [x for x in os.listdir('data')]
print ("Reading file(s): ", SOURCE)

DICT_TITLE = 'VD'


def get_html(source):
    """    
    Loads dictionary and checks if BS output is valid by counting tags. 
    """    
    tag_to_compare = '</p>'
    html = open('data/' + source, "r", encoding="utf8")
    data = html.read()
    html.close()
    soup = BeautifulSoup(data, "html.parser")
    if data.count(tag_to_compare) != str(soup).count(tag_to_compare):
        return 0, str(soup)
    return soup
    
def get_contents(element):
    """
    Extracts text from paragraphs.
    """
    units = []
    for el in element:
        units.append([(x.get_text()).strip() for x in el.contents if isinstance(x, NavigableString) == False])
    return units

def main(argv):
    """
    Loads dictionary html file(s) and extracts paragraphs.
    Sends data to appropriate classes for further processing and retrieves 
    processed data as entry objects in dict form {'entry name' : <entry object>}.
    Saves data in json format.
    @params:
        script - None or 'cyr'. If 'cyr' text would be transliterated to 
        cyrillic if it already ins't. If None text would be left in it's original
        form. 
        debug - If True it will print out attributes of each processed object.
        text_only - If True it will extract pure text, otherwise html via 
        text_only variable
    """   
    if 'cyr' in argv:
        script = 'cyr'
    else:
        script = 'lat'
    if 'debug' in argv:
        debug = True
    else:
        debug = False
    if 't' in argv:
        text_only = True
    else:
        text_only = False
    if 'p' in argv:
        to_pickle = True
    else:
        to_pickle = False
    
    temp = open('titles', 'w', encoding="utf8")
    to_write = {DICT_TITLE: OrderedDict()}
    all_dicts = {}
    total = 0
    if debug:
            print ('*********************DICTIONARY ' + DICT_TITLE + '****************************\n')
    for source in SOURCE:
        print(source)
        data = get_html(source)
        if isinstance(data, tuple):
            try:
                print ('Error!\n', 'Line: ', data[1][-100:])
            except IndexError:
                print ('Error!')
            return
        paras = data.findAll('p')
        total += len(paras)

        ''' Either chose pure text or html via text_only variable '''
        if text_only:
            contents = get_contents(paras)
        else:
            contents = paras
        dictionary = make_entries(contents) 
        
        all_dicts.update(dictionary)
        for d in dictionary:
            if debug:
                entry.debug()
            temp.write(d + '\n')
            
    for e in all_dicts:
        to_write[DICT_TITLE].update({e:all_dicts[e].json_ready()})
                
    if script == 'cyr':
        name = DICT_TITLE + '_cyr'
    else:
        name = DICT_TITLE + '_lat'
        
    if to_pickle:
        pickle.dump(all_dicts, open('out/%s' % (name), 'wb'))      
        
    outfile = open('parsed/%s.json' % (name), 'w', encoding="utf8")
    json.dump(to_write, outfile, ensure_ascii=False, indent=4, separators=(',', ': '))
    print('Parsed a total of ' + str(total) + ' paragraphs.')
    outfile.close()
    temp.close()
    
if __name__ == "__main__":
    main(argv)

