#!/bin/bash

# FILES="/08-30-2020 samples/*"
FILES="./09-08-2020_Structures/*"
iterator=1
filemap=./"NEB LAMMPS input files"/"09-08-2020 inputs"/filemap.txt
touch "${filemap}"
eval echo "Identifier Filename" >> "${filemap}"
for f in $FILES
do
	#echo "Processing $f"
	search="final"
	i=${f#*$search}
	#echo "i is $i"
	eval echo "$iterator $f" >> "${filemap}"
	python3 makeNEBinputsGAPinterfaces.py aSicSi_merged_GAP-$i.xyz $f $iterator
	((iterator+=1))
done
