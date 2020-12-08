#!/usr/bin/env python
# coding: utf-8
import sys
import os

directory = os.getcwd()
task = sys.argv[1]
job = sys.argv[2]
file_extension = '/aSiBox-' + str(job) + '-' + str(task) + '.xyz'
file = directory + file_extension

lines = open(file).read().splitlines()
for n, line in enumerate(lines):
    if n == 7:
        newline = line.split()
        zSize = float(newline[1]) - float(newline[0])
    elif n >= 9:
        newline = line.split()
        z = float(newline[4])
        if z < 0:
            zprime = format(1 + z, '.6f')
        elif z > 1:
            zprime = format(z - 1, '.6f')
        else:
            zprime = str(z)
        
        newline[4] = zprime
        separator = ' '
        final_line = separator.join(newline)
        lines[n] = final_line

open(file,'w').write('\n'.join(lines))
