# -*- coding: utf-8 -*-
"""
Created on Mon Apr  4 21:04:19 2016

@author: Milosh
"""

f = open('out/test1.txt', 'r', encoding='utf8')
data = f.readlines()
f.close()

new = []

for l in range(len(data)-1):
    if data[l] == data[l+1]:
        print(data[l], data[l+1])
        continue
    else:
        q = data[l]
        q = q.replace(' #', '#')
        q = q.replace('#  ', '# ')
        new.append(q)
        
rev = open('out/test1rd.txt', 'w', encoding='utf8')
rev.write(''.join(new))
rev.close()
        
    