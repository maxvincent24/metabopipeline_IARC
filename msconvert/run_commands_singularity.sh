#!/bin/bash

img="maxvin/msconvert_img:0.1.5"

if [[ ! -f ./maxvin_msconvert_img.sif ]]
then
    singularity build maxvin_msconvert_img.sif docker://${img}
fi

singularity exec --writable-tmpfs --pwd /home/msconvert --bind $PWD:/home/msconvert/data maxvin_msconvert_img.sif python3 -u dtomzML.py $1

