#!/bin/bash -l
t=2
j=1782063

s=31428+$t
dumpA=aSi-$j-$t.xyz
dumpsnapA=aSiBox-$j-$t.xyz
dumpI=cSiaSiInterface-$j-$t.xyz
dumpsnapI=cSiaSiInterfaceSnapshot-$j-$t.xyz

python3 trimBox.py $t $j
mpirun lmp_daily -var s $s -var d $dumpI -var dA $dumpsnapA -var ds $dumpsnapI -in mergeAmorphousCrystalline.in
