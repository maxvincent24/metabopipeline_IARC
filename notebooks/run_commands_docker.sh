#!/bin/bash

img="maxvin/data_science_img:0.1.6"


if [[ "$(docker images -q ${img} 2> /dev/null)" == "" ]]; then
  docker pull ${img}
fi

if [[ ! -d ./metabopipeline_notebooks ]]; then
  git clone https://github.com/maxvincent24/metabopipeline_notebooks.git
fi

docker run -it -p 8888:8888 -v "${PWD}"/metabopipeline_notebooks:/home/jovyan/work ${img}
