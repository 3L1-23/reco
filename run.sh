#!/bin/bash

container="reco"
volume="/reco/run:/reco"

docker run -it -v $volume --name $container $container:latest