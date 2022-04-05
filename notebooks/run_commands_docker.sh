#!/bin/bash

if [[ "$(docker images -q maxvin/data_science_img:0.3.1 2> /dev/null)" == "" ]]; then
  docker pull maxvin/data_science_img:0.3.1
fi

if [[ ! -d ./metabopipeline_notebooks ]]; then
    git clone https://github.com/maxvincent24/metabopipeline_notebooks.git
fi

docker run -it -p 8888:8888 -v "${PWD}"/metabopipeline_notebooks:/home/jovyan/work maxvin/data_science_img:0.3.1
