#!/bin/bash

container="reco"

docker start $container
docker exec -it $container bash