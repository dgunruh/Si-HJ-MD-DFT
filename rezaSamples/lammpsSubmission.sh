#!/bin/bash -l

j=1782063
t=0


# assign the random seed and the output files for the lammps scripts
s=31248+100*$t
dumpA=aSi-$j-$t.xyz
dumpsnapA=aSiBox-$j-$t.xyz
dumpI=cSiaSiInterface-$j-$t.xyz
dumpsnapI=cSiaSiInterfaceSnapshot-$j-$t.xyz

# sed -rie 's/(rand_seed equal)\s\w+/\1 $s/gi' createAmorphousSi.in
# sed -rie 's/(rand_seed equal)\s\w+/\1 $s/gi' mergeAmorphousCrystalline.in
mpirun -np 4 lmp_daily -var s $s -var d $dumpI -var dA $dumpsnapA -var ds $dumpsnapI -in mergeAmorphousCrystalline.in
