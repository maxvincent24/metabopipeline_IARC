#!/bin/bash

if [[ "$(docker images -q maxvin/msconvert_img:0.1.4 2> /dev/null)" == "" ]]; then
  docker pull maxvin/msconvert_img:0.1.4
fi

docker run -t -v $PWD:/home/msconvert/data maxvin/msconvert_img:0.1.4 python3 -u dtomzML.py $1
