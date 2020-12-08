#!/bin/bash -l
t=1
j=18


# assign the random seed and the output files for the lammps scripts
s=$j+$t   # 124248+$j+$t
dumpA=localResults/aSi-$j-$t.xyz
dumpsnapA=localResults/aSiBox-$j-$t.xyz
dumpI=localResults/cSiaSiInterface-$j-$t.xyz
dumpsnapI=localResults/cSiaSiInterfaceSnapshot-$j-$t.xyz

mpirun -np 4 lmp_daily -var s $s -var d $dumpA -var ds $dumpsnapA -in createAmorphousSi.in

timestep=$(head -2 aSiBox-$j-$t.xyz | tail -1)
zBotEdge=$(head -8 aSiBox-$j-$t.xyz | tail -1 | awk '{print $1;}')

mpirun -np 4 lmp_daily -var s $s -var d $dumpI -var dA $dumpsnapA -var ds $dumpsnapI -var t $timestep -var z $zBotEdge -in mergeAmorphousCrystalline.in
