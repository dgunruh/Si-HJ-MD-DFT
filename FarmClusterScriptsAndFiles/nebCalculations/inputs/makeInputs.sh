#!/bin/bash

for i in {1..64}
do
	python3 makeNEBinputs.py 2ndBlastInputs/aSicSi_merged_GAP-1.xyz_init.out 2ndBlastInputs/blast2.final$i $i
done
