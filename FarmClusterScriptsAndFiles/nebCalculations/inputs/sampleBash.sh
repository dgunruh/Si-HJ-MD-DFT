#!/bin/bash

for i in {1..64}
do
	python3 makeNEBinputs.py aSiInputs/aSi_GAP_20_DFT-LAMMPS.out aSiInputs/aSi_blast2.final$i aSi$i
done
