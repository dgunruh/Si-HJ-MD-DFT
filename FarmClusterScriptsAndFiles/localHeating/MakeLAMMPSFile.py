#!/usr/bin/env python
# coding: utf-8
import sys
import os

directory = os.getcwd()
file_extension = '/a-si215-opt.xyz'
file = directory + file_extension

lines = open(file).read().splitlines()
for n, line in enumerate(lines):
	if n >= 16:
		newline = line.split()
		atomID = n - 15
		atomType = 1
		newline[0] = str(atomID)
		newline.insert(1, str(atomType))
		separator = '\t'
		final_line = separator.join(newline)
		lines[n] = final_line
open(file,'w').write('\n'.join(lines))
