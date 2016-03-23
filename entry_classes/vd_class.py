# -*- coding: utf-8 -*-
"""
Created on Tue Jan 12 16:54:08 2016

@author: Misha
"""

from tools.sr_lat2cyr2lat import *
from collections import OrderedDict, Counter
from entry_classes.vd_abbreviations import *
import re

class Entry():
    '''
    Class to contain data from dictionary entry.
    '''
    def __init__(self, name, latin = None):
        self.title = name
        self.standard_title = None
        self.origin = None
        self.script = 'cyr'
        self.original_title = None
        self.gender = None
        self.children = []
        self.other = []
        self.type = OrderedDict()
        self.forms = OrderedDict()
        self.examples = OrderedDict()
        self.synonyms = OrderedDict()
        self.meanings = OrderedDict()
        self.meanings_count = (0, 0)
        self.derived = 0
        self.sub_entries = OrderedDict()
        self.sub_entries_count = 0
        self.keys = [(0, 0)]
        self.phrases = {}
        self.unique = True
        self.latin = latin

    def add_see(self, other):
        '''
        self.other is equivalent to 'see:' in dictionary entry, pointing out
        to the other entry. Usually such entries are reduced to that other 
        entry and can take all of it's data as it's own.
        '''
        self.other.append(other)
    def set_origin(self, origin):
        '''
        If entry is dervied from the other entry or if it is subentry of the
        other, this method will assign name of parent entry to self.origin.
        '''
        origin = strip_all(origin)
        self.origin = origin
    def increase_meaning(self, second_lvl = False, only_second_lvl = False):
        '''
        This method is called each time we detect submeaning in the entry.
        It modifes the meanings_count attribute which is a tuple containg two
        numbers. First is the current meaning, if it's first, or only meaning
        which entry contains it will have value of 0. Any subsequent submeanings
        will increase meanings count by 1. The second number in the tuple 
        represents parts of the submeaning. For example, if we have submeaning
        denoted by the number '1.' followed by 'a.' we will increase both 
        variables in the tuple by 1. On the other hand, if we encounter 'b.', 
        we will increase only the second number. Finally, if we have only '1.'
        or '2.', etc, we will incrase only the first number.
        @params
            second_lvl - boolean, if True we increase part of the entry num.
            only_second_lvl - we incease only the part of the entry num     
        '''
        if only_second_lvl == True:
            self.meanings_count = (self.meanings_count[0], self.meanings_count[1] + 1)
        elif second_lvl == False and self.meanings_count[1] > 0:
            self.meanings_count = (self.meanings_count[0] + 1, 0)
        elif second_lvl == True and self.meanings_count[1] == 0:
            self.meanings_count  = (self.meanings_count[0] + 1, self.meanings_count[1] + 1)
        elif second_lvl == True and self.meanings_count[1] > 0:
            self.meanings_count  = (self.meanings_count[0], self.meanings_count[1] + 1)
        else:
            self.meanings_count  = (self.meanings_count[0] + 1, self.meanings_count[1]) 
        self.keys.append(self.meanings_count)
    def add_type(self, typ):
        '''
        Adds types of the entry.
        '''
        typ = strip_all(typ)
        if self.meanings_count in self.type:
            if self.sub_entries_count in self.type[self.meanings_count]:
                self.type[self.meanings_count][self.sub_entries_count].append(typ)
            else:
                self.type[self.meanings_count][self.sub_entries_count] = [typ]
        else:
            self.type[self.meanings_count] = {self.sub_entries_count : [typ]}
    def add_forms(self, form):
        '''
        Adds forms of the entry.
        '''
        form = strip_all(form)
        if self.meanings_count in self.forms:
            if self.sub_entries_count in self.forms[self.meanings_count]:
                self.forms[self.meanings_count][self.sub_entries_count].append(form)
            else:
                self.forms[self.meanings_count][self.sub_entries_count] = [form]
        else:
            self.forms[self.meanings_count] = {self.sub_entries_count : [form]}
    def add_synonym(self, synonym, category):
        '''
        Adds sysnonyms of the entry with their category.
        '''
        synonym, category = strip_all(synonym), strip_all(category)
        if self.meanings_count in self.synonyms:
            if self.sub_entries_count in self.synonyms[self.meanings_count]:
                self.synonyms[self.meanings_count][self.sub_entries_count].append([synonym, category])
            else:
                self.synonyms[self.meanings_count][self.sub_entries_count] = [[synonym, category]]
        else:
            self.synonyms[self.meanings_count] = {self.sub_entries_count : [[synonym, category]]}
    def add_meaning(self, meaning, reference, location):
        '''
        Adds meaning of the entry together with location and bibliographical
        reference for each.
        '''
        meaning, reference, location = strip_all(meaning, "'‘’ "), strip_all(reference), strip_all(location)
        if self.meanings_count in self.meanings:
            if self.sub_entries_count in self.meanings[self.meanings_count]:                            
                self.meanings[self.meanings_count][self.sub_entries_count].update({meaning : [reference, location]})
            else:
                self.meanings[self.meanings_count][self.sub_entries_count] = {meaning : [reference, location]}
        else:
            self.meanings[self.meanings_count] = {self.sub_entries_count : {meaning : [reference, location]}}
    def increase_sub_entry_count(self):
        '''
        Sub entries are smaller units of the meaning of the entry. They are
        delimited by ';' sign. We call this method every time we encounter 
        such string in the right context, or when submeaning is exhausted. 
        '''
        self.sub_entries_count += 1
    def add_sub_entry(self, sub_entry_name):
        '''
        Adds subentry title with the list that can possibly contain more data.
        '''
        sub_entry_name = strip_all(sub_entry_name)
        if self.meanings_count in self.sub_entries:
            self.sub_entries[self.meanings_count].update({self.sub_entries_count : {sub_entry_name : []}})
        else:
            self.sub_entries[self.meanings_count] = {self.sub_entries_count : {sub_entry_name: []}}
    def add_examples(self, description, reference, location):
        '''
        Adds example sentences with geographical and bibliographical references.
        '''
        description, reference, location = strip_all(description), strip_all(reference), strip_all(location)
        if self.meanings_count in self.examples:
            if self.sub_entries_count in self.examples[self.meanings_count]:
                self.examples[self.meanings_count][self.sub_entries_count].update({description : [reference, location]})
            else:
                self.examples[self.meanings_count].update({self.sub_entries_count : {description : [reference, location]}})
        else:
            self.examples[self.meanings_count] = {self.sub_entries_count : {description : [reference, location]}}
    def add_phrase(self, phrase, phrase_type = None, meaning = None, example = None, location = None, reference = None):
        '''
        Adds phrase as the unit of the entry. Phrase is more complex part as 
        it can contain data such as it's own meaning, examples, type, and
        geographical and bibliographical references.
        '''
        data = [phrase_type, meaning, example, location, reference]
        data = [x for x in data if x != None]
        data = strip_all(data)
        if self.meanings_count in self.phrases:
            if self.sub_entries_count in self.phrases[self.meanings_count]:
                self.phrases[self.meanings_count][self.sub_entries_count].update({phrase : data})
            else:
                self.phrases[self.meanings_count].update({self.sub_entries_count : {phrase : data}})
        else:
            self.phrases[self.meanings_count] = {self.sub_entries_count : {phrase : data}}
    def set_standard_title(self):
        '''
        We can set the standard title of the entry using this method. 
        Standard entry is deaccentized version of the original title.
        We can only set the standard title if original title is not already
        without any accentuated characters.
        '''
        temp = ''
        for s in self.title:
            if s.lower() in AZBUKA_STR:
                temp += s
            elif s in ' {}1234567890d':
                temp += s
        if temp != self.title:
            self.standard_title = temp
    def not_unique(self):
        self.unique = False
    def get_title(self):
        return self.title
    def get_gender(self):
        return self.gender
    def get_other(self):
        return self.other
    def get_meanings_no(self):
        return self.meanings_count
    def get_sub_entries_count(self):
        return self.sub_entries_count
    def get_forms(self):
        return self.forms 
    def get_type(self):
        return self.type
                
    def deaccentized_title_entry(self):
        '''
        This method sets title to deaccented title and standard_title to None.
        It maintains information on original title by storing it in origin.
        '''
        if self.standard_title == None:
            self.set_standard_title()
        self.origin = self.title
        self.title, self.standard_title = self.standard_title, None
    def copy_self(self):
        '''
        This method returns a copy of entry object. Useful when creating 
        deaccentized versions of original entries.
        '''
        return Entry()
    def debug(self):
        print(self.title)
        print(self.meanings_count)
        print('forms: ', self.forms)
        print('meanings:', self.meanings)
        print('subentries: ', self.sub_entries)
        print('examples: ', self.examples)
        print('phrases: ', self.phrases)
        print('synonyms: ', self.synonyms)
        print('types: ', self.type)
        print('\n')
        
    def reconstruct_entry(self):
        """
        The goal of this function is to recontruct as much as possible the
        original form of the entry. 
        """
        def get_elements(var, meaning, subentry):
            try:
                if isinstance(var[meaning][subentry], dict):
                    for d in var[meaning][subentry]:
                        lst = [x for x in var[meaning][subentry][d] if x != None]
                        if lst != [] and d != None:
                            return ' '.join([d, ' '.join(lst)])
                        elif d == None:
                            return ' '.join(lst)
                        else:
                            return d
                elif isinstance(var[meaning][subentry], list):
                    lst = [str(x) for x in var[meaning][subentry] if x != None]
                    return ' '.join(lst)
                else:
                    return var[meaning][subentry]
            except KeyError:
                pass
            
        if self.get_other() != []:
            entry_parts = [self.get_title(), 'see:', ' '.join(self.get_other())]
        else:
            entry_parts = [self.get_title()]
            for i in range(self.get_meanings_no()[0] + 1):
                for j in range(self.get_meanings_no()[1] + 1):
                    key = (i, j)
                    for k in range(self.get_sub_entries_count() + 1):
                        parts = [self.type, self.sub_entries, self.forms, self.meanings, self.examples, self.synonyms, self.phrases]
                        parts_to_add = [get_elements(x, key, k) for x in parts]
                        entry_parts.extend(parts_to_add)

        entry_parts = [x for x in entry_parts if x != None]
        return ' '.join(entry_parts)
        
    def json_ready(self):
        '''
        Returns class attributes formated so that they can exported to JSON.
        '''
        standard_name = self.standard_title
        original_title = self.original_title
        script = self.script
        origin = self.origin
        gender = self.gender
        children = self.children
        other = self.other
        keys = self.keys
        
        json = OrderedDict({'standard name':standard_name, 'original title':original_title, 
                            'origin':origin, 'gender':gender, 'children':children, 'other':other,
                            'script':script, 'keys':keys})
        
        body = OrderedDict()
        for key in self.keys:
                part = str(key)
                body[part] = OrderedDict()
                if key in self.sub_entries:
                    body[part]['sub_entries'] = OrderedDict()
                    for sub_entry in self.sub_entries[key]:
                        body[part]['sub_entries'].update({sub_entry:self.sub_entries[key][sub_entry]})
                if key in self.type:
                    body[part]['type'] = OrderedDict()
                    for typ in self.type[key]:
                        body[part]['type'].update({typ:self.type[key][typ]})
                if key in self.forms:
                    body[part]['forms'] = OrderedDict()
                    for form in self.forms[key]:
                        body[part]['forms'].update({form:self.forms[key][form]})  
                if key in self.meanings:
                    body[part]['meanings'] = OrderedDict()
                    for meaning in self.meanings[key]:
                        body[part]['meanings'].update({meaning:self.meanings[key][meaning]}) 
                if key in self.examples:
                    body[part]['examples'] = OrderedDict()
                    for example in self.examples[key]:
                        body[part]['examples'].update({example:self.examples[key][example]}) 
                if key in self.synonyms:
                    body[part]['synonyms'] = OrderedDict()
                    for synonym in self.synonyms[key]:
                        body[part]['synonyms'].update({synonym:self.synonyms[key][synonym]}) 
                if key in self.phrases:
                    body[part]['phrases'] = OrderedDict()
                    for phrase in self.phrases[key]:
                        body[part]['phrases'].update({phrase:self.phrases[key][phrase]}) 
        
        json.update({'elements':body})
        return json
    def to_wiki(self, begin = False, end = False):
        string = []
        if begin:
            if self.script == 'lat':
                string.append('== %s ([[Викиречник:Српски|српски]], [[Викиречник:Ћирилица|ћир.]] [[%s]]) ==\n\n' % (self.title, self.original_title))
            else:
                string.append('== %s ([[Викиречник:Српски|српски]]) ==\n\n' % (self.title))
                
        for k in self.keys:
            string.append('=== %s ===\n' % (self.get_wiki_type()))
            string.append(format_type(self.get_type(), self.get_wiki_type()))
        
        

def strip_all(entity, chars = None):
    '''
    Use built in strip fnction to erase extra characters from the beginning or
    end of the string, or in the strings in the list or in the values of the
    dictionary. It can also recursively strip characters if dict values
    or list items themselves contain lists or dicts.
    @params:
        entity - string, list or dict.
        chars - string containg characters to be removed
    @returns:
        A string, or a list or a dict with its members, 
        with removed extra characters and spaces.
    '''
    if isinstance(entity, str):
        if chars:
            return entity.strip(chars)
        return entity.strip()
    elif isinstance(entity, list):
        if chars:
            return [strip_all(x, chars) for x in entity]
        return [strip_all(x) for x in entity]
    elif isinstance(entity, dict):
        new_dict = OrderedDict()
        if chars:
            for key in entity:
                new_dict[key.strip(chars)] = strip_all(entity[key], chars)
            return new_dict
        else:
            for key in entity:
                new_dict[key.strip(chars)] = strip_all(entity[key], chars)
            return new_dict
    else:
        return entity

def parse_phrase(string):
    """
    Function that extracts phrase data, that is, the phrase itself, its meaning,
    meaning description, reference, geographical locations where it is
    used, as well as categories it belongs to.
    @params:
        string - string
    @returns:
        strings: phrase, meaning, example, location, reference, typ
    """
    meaning = example = location = reference = typ = None
    
    
    '''
    First, look for abbreviations, they are in the beginning of the string.
    '''
    string_copy = string
    abb_list = []
    while True:
        try:
            abb, string_copy = string_copy.split(' ', 1)
            if abb in ABBREVIATIONS:
                abb_list.append(abb)
                continue
            else:
                break
                    
        except ValueError:
            abb = string_copy.strip()
            break
            
    if abb in ABBREVIATIONS:
        if typ != None:
            typ = typ + ' ' + abb
        else:
            typ = abb  
            
    '''
    Find the phrase itself, and cut it from the rest of the string. 
    '''
    string = re.sub('\d\.', '', string)
    phrase = re.findall('.*?[‘|\([A-Z]|;|\.]', string)

    if phrase:
        phrase = phrase[0][:-1]
    else:
        phrase = string
    
    '''
    Find meaning, examples, location and reference parts of the phrase.
    '''
    find_meaning = re.findall('‘[^"]*[’|\']', string)
    if find_meaning:
        meaning = find_meaning[0][1:-1]
        
    find_example = re.findall('—.*?[\.|\()|\[]', string)
    if find_example:
        example = find_example[0][2:-2]
        
    find_location = re.findall('\(.*?\)', string)
    if find_location:
        location = find_location[-1]
        if location[1].isupper() == False:
            location = None
            
    find_reference = re.findall('\[.*?\]', string)
    if find_reference:
        reference = find_reference[-1]
        if reference[1].isupper() == False:
            reference = None
            
    return phrase, meaning, example, location, reference, typ
        
def analyze_phrase(string, entry):
    """
    Function determines how many phrases the string contains and splits them.
    It calls a function parse_phrase that will extract needed data from each.
    There are two types of phrases depending on the symbol:
    △ - phrase where title of the entry has meaning of its own independently
    of other words in a phrase.
    □ - phrase where the meaning of the title word is dependent on the other
    words in a phrase.
    ▭ - phrase with interesting details in the example as denoted by dictionary
    authors.
    
    @params:
        string - string
        entry - Entry class object
    @returns:
        Entry class object
    """
    string = string.strip()
    phrase_type = None
    if string[:1] == '△':
        phrase_type = '△'
    elif string[:1] == '□':
        phrase_type = '□'
    elif string[:1] == '▭':
        phrase_type = '▭'
    
    '''
    Strip symbol from the start of the string and find all phrases.
    '''
    string = string[1:].strip()
    lst_str = re.split(';\s.*(?=(?:;|\.))', string)
    lst_str = [x for x in lst_str if x not in '.;']
    if len(lst_str) > 1:
        repeat_phrase = None
        for lst in lst_str:
            phrase, meaning, example, location, reference, typ = parse_phrase(lst)
            if re.search('\d\.', lst):
                if phrase == None or phrase.strip() == '':
                    phrase = repeat_phrase
                else:
                    repeat_phrase = phrase
            entry.add_phrase(phrase, phrase_type, meaning, example, location, reference)
    else:
        phrase, meaning, example, location, reference, typ = parse_phrase(string)
        entry.add_phrase(phrase, phrase_type, meaning, example, location, reference)
    return string, entry
    
def get_meaning(string, entry, title_of):
    '''
    Extract meaning of the entry from the string and increase subentry key
    if we encounter ';' string which is a subentry separator.
    '''
    meaning = location = reference = None
    meaning = re.findall('‘.*?[\'|’][\s|\.|;]{0,1}', string)
    
    if len(meaning) != 0:
        meaning = meaning[0]
        if meaning.endswith(';'):
            meaning = meaning[:-1]
        string = string.replace(meaning, ' ')
        string = string.lstrip()

        if meaning.endswith('.') == False:
            _, location, reference = get_location_and_reference(meaning)
        if meaning:
            meaning = meaning.strip('.‘\'’ ')
            entry.add_meaning(meaning, reference, location)

    return string, entry
    
def split_example(examples):
    '''
    Split string containing all examples by delimiter.
    '''
    examples = examples.split('. —')
    return examples    
    
def get_examples(string, entry, title_of):
    '''
    Take entire string and find each example sentence which can be
    also followed by information on geografical location and
    bibliographical references. There can be many examples in each subentry
    so this function is iterative.
    We also take care about increasing subentry keys in the entry object if
    we encounter separator (';' sign).
    @params:
        string - original text of the entry
        entry - Entry object
        title_of - title of subentry if there is one
    @returns:
        string - stripped of processed data so far
        entry - updated Entry instance
    '''       
    examples = re.findall('—.*(?:\)\.|\]\.|\);|\];|\.\s—|\s;|\w;|\)\s\.|\]\s\.)', string)
    if len(examples) > 0:
        string = string.replace(examples[0], '')
        examples = split_example(examples[0])
        increase_sk = False
        for example in examples:
            example = example.strip()
            if example.endswith(';'):
                increase_sk = True
            reference = location = None
            if example != '':
                string = string.replace(example, '')
                example, location, reference = get_location_and_reference(example)
                    
            if example:
                example = example.strip('—;. ' )
                entry.add_examples(example, reference, location)
                
            if increase_sk:
                entry.increase_sub_entry_count()
                increase_sk = False

    return string, entry
    
def get_location_and_reference(s, string = None):
    '''
    Extract location and reference data from the string.
    @params:
        s - string, it can contain part where location and reference should be
        string - None or string if we provide entire original string so we
        can strip extracted data from it.
    '''
    if string == None:
        string = s
    string = string.strip()
    location = reference = None
    find_location = re.findall('\(.*?\)', s)
    find_location = [x for x in find_location if x[1].isupper()]
    if find_location != []:
        location = find_location[0]
        string = string.replace(location, ' ') 
        string = string.lstrip()
    
    find_reference = re.findall('\[.*?\]', s)
    find_reference = [x for x in find_reference if x[1].isupper()]
    if find_reference != []:
        reference = find_reference[0]
        string = string.replace(reference, ' ') 
        string = string.lstrip()
    return string, location, reference
    
def cut_phrase(string, entry):
    '''
    Function to identify phrase parts of the entry and pass them for
    further processing.
    '''
    idx = [x for x in range(len(string))  if string[x] in '△□▭']
    phrases = []
    for i in range(len(idx)):
        if idx[i] != idx[-1]:
            phrases.append(string[idx[i]:idx[i+1]])
        else:
            phrases.append(string[idx[i]:])
        
    for phrase in phrases:
        string = string.replace(phrase, '')
        _, entry = analyze_phrase(phrase, entry)

    return string, entry
    
def get_forms(string, entry,title_of):
    if re.match('само у\s.*?‘', string):
        only = re.findall('само у\s.*?(?:‘)', string)[0][:-1]
        entry.add_forms(only)
        string = string.replace(only, '')
    
    substr = re.findall('\D+\s\d\.[\s\w\.]{,3}', string)
    if substr != []:
        substr = substr[0]
        if '‘' in substr:
            substr = substr.split('‘')[0]
        if substr in '. ' or (len(substr) == 2 and re.match('\d\.', substr)):
            return string, entry
        string = string.replace(substr, '')
        substr = substr.strip()
        substr = substr.split()
        skip = False
        for i, s in enumerate(substr):
            if skip == True:
                skip = False
                continue
            if s in ABBREVIATIONS:
                entry.add_type(s)
            else:
                if i != len(substr)-1:
                    if re.match('(\d\.|\s\w\.|\s\d\.[\s]{0,1}|[\w\.])', substr[i+1]):
                        entry.add_forms(s + ' ' + substr[i+1])
                        skip = True
                    else:
                        entry.add_forms(s)
                else:
                    entry.add_forms(s)
    return string, entry
    
def append_to_form(entry, next_str):
    '''
    This function appends data to an already existing form attribute in the 
    object instance. 
    '''
    next_str = next_str.strip('.')
    try:
        entry.forms[entry.keys[-1]][entry.sub_entries_count][-1] = entry.forms[entry.keys[-1]][entry.sub_entries_count][-1] + ' ' + next_str
    except KeyError:
        entry.add_forms(next_str)

    if next_str.endswith(');') or next_str.endswith('];'):
        entry.increase_sub_entry_count()
        
def get_types(string, entry):
    for abb in ['одр вид', 'поим прид', 'гл им', 'присв прид', 'пл т', 'прил сад']:
        if abb in string:
            entry.add_type(abb)
            string = string.replace(abb, '')
    return string, entry
        
def string_by_string(string, entry, title_of, synonym):
    """
    This function takes a string and chops words or characters it, trying
    to match them with known patterns or certain symbols.
    First it tries to use regular expressions in order to extract phrase, meaning,
    example, reference or location information from the string. If it does
    not find meaning or example it proceeds further and tries to disambiguate
    the rest of the string by chopping word by word from string. 
    It also extracts synonyms, forms and calls a function to extract phrases,
    as well as counts subentries. 
    @params:
        string - string
        entry - Entry class object
        title_of - string, name of the subentry
        synonym - synonym name that we are currently processing
    @returns:
        entry - Entry class object
        title_of - string, name of the subentry
    """
    string = string.strip()
    string = string.lstrip(',.')
    if string[:1] == ';':
        entry.increase_sub_entry_count()
        string = string[1:]
        
    if string == '':
        return entry, title_of
            
    '''
    Discover does the string contain phrase data and if so pass the string 
    for phrase extracion.
    '''
    if re.findall('[△|□|▭].*?[;|\.]', string) != []:
        string, entry = cut_phrase(string, entry)
        
            
    '''
    If we encounter reference and location data at the beginning of the string
    we extract them and add to forms names.
    ''' 
    
    if string.startswith('(') or string.startswith('['):
        s = re.findall('.*?[\)|\]][\.|;]', string)
        if s == []:
            s = string
        else:
            s = s[0]
        string = string.replace(s, '')
        if synonym != None:
            _, location, reference = get_location_and_reference(s) 
            entry.synonyms[entry.keys[-1]][entry.sub_entries_count][-1].extend([reference, location])
        else:
            _, location, reference = get_location_and_reference(s)
            try:
                entry.sub_entries[entry.meanings_count][entry.sub_entries_count][title_of].append([reference, location])
            except KeyError:
                pass
    
    '''
    Find meaning and examples.
    '''
    
    string, entry = get_forms(string, entry, title_of)
    string, entry = get_types(string, entry)
    string, entry = get_meaning(string, entry, title_of) 
    string, entry = get_examples(string, entry, title_of)
    
    '''
    Chopping the string and finding what is left.
    '''
    while string != '': 
        '''
        Special case of meaning of the entry representing normal, or usual
        meaning. We handle it here.
        '''
        if string.lstrip().startswith('⊜'):
            meaning = '⊜'
            string = string.replace(meaning, '')
            string.lstrip()
            string, location, reference = get_location_and_reference(string)
            entry.add_meaning(meaning, reference, location)  
            
        '''
        In each pass through the loop we chop the string word by word. 
        On ValueError we know that we have no more words to get from the string.
        '''
        try:
            next_str, string = string.split(' ', 1)
            string = string.strip()
        except ValueError:
            next_str = string
            string = ''

        '''
        Look for abbreaviations, subentry delimiters, part of forms or 
        unescesarry characters.
        '''        
        if next_str in ABBREVIATIONS:
            entry.add_type(next_str)
        elif next_str == ';':
            entry.increase_sub_entry_count()
            title_of = None
        elif next_str.isdigit():
            append_to_form(entry, next_str)
        elif next_str.startswith('(') or next_str.startswith('[') or next_str.endswith(')') or next_str.endswith(']'):
            append_to_form(entry, next_str)
        elif next_str in ',.—˜- ':
            continue
        else:
            entry.add_forms(next_str)
            
        '''
        If there is nothing left to chop, check if remaining string ends with
        ; and increase sub_entry count.
        '''
        if string == next_str and next_str.endswith(';'):
            entry.increase_sub_entry_count()
                    
    return entry, title_of
    
def has_multi_meanings(para):
    """
    Discover how many different meanings the entry contains, if any.
    @params:
        para - a list of strings
    @returns:
        False if no meanings are discovered
        idx - list of indices where symbols which separate different 
        subentries are located (symbol examples: '1.', '2', etc).
    """
    idx = []
    for i, p in enumerate(para):
        if re.match('\d\.', p[0]) and p[1] == 0:
            idx.append(i)
    if idx != []:
        return idx
    return False
        
def process_bold_text(string, entry, idx, derived):
    """
    Filter out the bold text.
    When the text is bold it either contains:
    a. a title of the entry
    b. a title of the subentry
    c. marks the number of particular meaning of the entry
    It is possible to have a.-b. and b.-c. combined in the same text, so we
    need to filter it and distinguish separate parts.
    @params:
        string - bold text to be processed
        entry - Entry class object or None
        idx - index of the string withing the list of strings belonging to a 
        certain paragraph from the dictionary
    @returns
        entry - Entry class obejct, updated
        name - the name of the dictionary entry
    """
    if string[:1] == '❚' or string == '❚':
        '''
        If the string contains only the black square, it denotes the beggining
        of subentry containing a derived form.
        '''
        entry.increase_meaning()
        return entry, True, None
        
    name = re.sub(' \d.| \d\.\w\.]', '', string)

    if idx == 0:
        entry = Entry(name)
        string = re.sub(name, '', string)
    elif re.match('\d\.\w\.', string):
        entry.increase_meaning(True, False)
        name = None
    elif re.match('\d\.', string): 
        entry.increase_meaning()
        name = None
    elif re.match('\w\.', string):
        entry.increase_meaning(False, True)
        name = None
    else:
        if derived:
            entry.add_sub_entry(name + ' d')
            derived = False
        else:
            entry.add_sub_entry(name)
        name = entry.title
       
    return entry, derived, name       
    
def process_italic_text(string, entry, derived):
    '''
    Italic text refers to synonyms. We find what kind of sinonimity it is and
    add it to Entry instance.
    @params:
        string - original text of the entry
        entry - Entry object
        derived - boolean, demarks a diferent form of the entry
    @returns:
        string - original text of the entry
        entry - Entry object
        synonym - string, name of the synonym
        derived - boolean
    '''
    synonym = None
    string = string.strip(' .')
    for s in '➡➩⮂‰':
        if s in string:
            string = string.replace(s, '')
            if derived:
                string = string + ' d'
                entry.add_synonym(string, s)
                synonym = string
                derived = False
                return entry, derived, string, synonym
            else:
                entry.add_synonym(string, s)
                synonym = string
                return entry, derived, string, synonym
    entry.add_sub_entry(string)
    return entry, derived, string, synonym
        
def analyze_entry(para):
    """
    Depending on the tag of strings contained in the para list we extract data
    either directly or by calling other functions. 
    0 - Bold
    1 - Italic
    2 - Normal font
    if font is bold it is a title of a entry or subentry, or symbol that
    marks another meaning of the entry.
    Italics denote synonyms or antonyms.
    Normal text is everything else.    
    
    synonyms:
        0 = connecting to all synonyms of an entry or meaning (black arrow symbol)
        1 = connecting to a certain sysnonym of an entry or meaning (white arrow symbol)
        2 = antonym (arrow with two tips)
        3 = not a complete synonymy (two arrows in opposite direction)
    """
    para = [(x[0].replace('\n', ''), x[1]) for x in para]
    para = [(x[0].replace('\t', ''), x[1]) for x in para]

    name = None
    entry = None
    derived = False
    synonym = None
    title_inserted = False
    for i, p in enumerate(para):
        if p[1] == 0:
            entry, derived, name = process_bold_text(p[0], entry, i, derived)
            if name != None and title_inserted == False:
                para = [(x[0].replace('˜', name), x[1]) for x in para]
                title_inserted = True
        elif p[1] == 1:
            entry, derived, name, synonym = process_italic_text(p[0], entry, derived)
        else:
            entry, name = string_by_string(p[0], entry, name, synonym)
            synonym = None
#    entry.debug()
    entry.set_standard_title()
    return {entry.title : entry}        
        
def get_entries(para):
    '''
    First we deal with the most simple case when we have only the name 
    of the entry and referral to the other entry.
    '''
    if len(para) <= 4 and len(para) >= 3:
        if para[1][0].strip() == 'в.':
            entry = Entry(para[0][0])
            entry.add_see(para[2][0])
            return {para[0][0]: entry}
        
    if para[0][1] == 0:
        return analyze_entry(para)
    else:
        ''' title tag is not in bold style '''
        print('error', para)
        pass
        return {para[0][0] : 'error'}
        
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
    titles = []
    entries = OrderedDict()
    for p in contents:
        spans = p.findAll('span')
        para = []
        to_add = None
        for s in spans:
            if 'bold' in s['style']:
                if to_add == 'bold':
                    para[-1] = (' '.join([para[-1][0].strip(' \t\n'), s.get_text().strip()]), para[-1][1])
                else:
                    para.append((s.get_text(), 0))
                    to_add = 'bold'
            elif 'italic' in s['style']:
                if to_add == 'italic':
                    para[-1] = (' '.join([para[-1][0].strip(' \t\n'), s.get_text().strip()]), para[-1][1])
                else:
                    para.append((s.get_text(), 1))
                    to_add = 'italic'
            else:
                if to_add == 'normal':
                    para[-1] = (' '.join([para[-1][0].strip(' \t\n'), s.get_text().strip()]), para[-1][1])
                else:
                    para.append((s.get_text(), 2))
                    to_add = 'normal'
        parsed_entry = get_entries(para)
        query_duplicate = list(parsed_entry.keys())[0]
        if query_duplicate in entries:
            parsed_entry = {query_duplicate + ' d': list(parsed_entry.values())[0]}
        entries.update(parsed_entry)
        
    return entries
    
