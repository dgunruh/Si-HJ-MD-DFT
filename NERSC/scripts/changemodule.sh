#!/bin/bash

pe=${PE_ENV,,}
if [ $pe == "gnu" ]; then
	echo $pe
	module swap PrgEnv-$pe PrgEnv-intel
	newpe=${PE_ENV,,}
	echo $newpe
fi

a=5
b=7
c=$((a+5*b))
echo $c
