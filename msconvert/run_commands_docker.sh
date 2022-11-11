#!/bin/bash

img="maxvin/msconvert_img:0.1.4"

if [[ "$(docker images -q ${img} 2> /dev/null)" == "" ]]; then
  docker pull ${img}
fi

docker run -t -v $PWD:/home/msconvert/data ${img} python3 -u dtomzML.py $1
