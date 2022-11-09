#!/bin/bash

img="maxvin/data_science_img:0.1.6"


if [[ ! -f ./maxvin_data_science_img.sif ]]
then
    singularity build maxvin_data_science_img.sif docker://${img}
fi

if [[ ! -d ./metabopipeline_notebooks ]]; then
    git clone https://github.com/maxvincent24/metabopipeline_notebooks.git
fi

singularity run --bind "${PWD}"/metabopipeline_notebooks:/home/jovyan/work maxvin_data_science_img.sif
