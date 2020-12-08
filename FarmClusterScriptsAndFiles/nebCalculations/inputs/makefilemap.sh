#!/bin/bash

# filemap="./NEB\ LAMMPS\ input\ files/touch.txt"
filemap=./"NEB LAMMPS input files"/touch.txt
touch "${filemap}"
eval echo "hello" >> "${filemap}"
