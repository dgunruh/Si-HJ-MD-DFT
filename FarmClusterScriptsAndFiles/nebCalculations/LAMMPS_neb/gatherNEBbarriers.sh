#!/bin/bash

output=09082020nebBarriers.txt
echo -e "ID\tForwardBarrier(eV)\tReverseBarrier(eV)" >> $output
for i in {1..611}
do
	t=logfiles/09082020logs/$i/log.lammps
	f=$(tail -1 $t | awk '{print $7}')
	r=$(tail -1 $t | awk '{print $8}')
	echo -e "$i\t$f\t$r" >> $output
done
