# -*- coding: utf-8 -*-
"""
Created on Tue Mar 22 17:52:48 2016

@author: Milosh
"""

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
        all_keys_list = [re.sub(r'\([^)]*\)', '', x).strip() for x in all_keys]
        ordered_keys = Counter(all_keys_list).most_common(no_of_dup)
        duplicates = ([x[0] for x in ordered_keys if x[1] > 1])
        outfile = open("out/duplicates.txt", "w", encoding="utf8")
        outfile.write("\n".join(duplicates))
        return duplicates