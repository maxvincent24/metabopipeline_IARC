#!/bin/bash

if [[ ! -f ./maxvin_data_science_img.sif ]]
then
    singularity build maxvin_data_science_img.sif docker://maxvin/data_science_img:0.3.1
fi

if [[ ! -d ./metabopipeline_notebooks ]]; then
    git clone https://github.com/maxvincent24/metabopipeline_notebooks.git
fi

singularity exec --bind "${PWD}"/metabopipeline_notebooks:/home/jovyan/work maxvin_msconvert_img.sif

