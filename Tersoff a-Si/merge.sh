#!/bin/bash -l

j=1847875
for t in {1..7}
do
	# assign the random seed and the output files for the lammps scripts
	s=$j+$t
	dumpA=pelotonResults/aSi-$j-$t.xyz
	dumpsnapA=pelotonResults/aSiBox-$j-$t.xyz
	dumpI=pelotonResults/cSiaSiInterface-$j-$t.xyz
	dumpsnapI=pelotonResults/cSiaSiInterfaceSnapshot-$j-$t.xyz
	peDump=potentialEnergy-$j-$t
	timestep=$(head -2 pelotonResults/aSiBox-$j-$t.xyz | tail -1)
	zBotEdge=$(head -8 pelotonResults/aSiBox-$j-$t.xyz | tail -1 | awk '{print $1;}')

	mpirun -np 4 lmp_daily -var s $s -var d $dumpI -var dA $dumpsnapA -var ds $dumpsnapI -var t $timestep -var z $zBotEdge -var pe $peDump -in mergeAmorphousCrystalline.in
done
