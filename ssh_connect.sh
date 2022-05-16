#!/bin/bash

container="reco"

docker start $container
# docker exec -it $container bash

containerIP=$(docker inspect reco | grep -o '"IPAddress":.*' | sort -u | grep -o "[0-9._]" | tr '\n' ' ' | sed 's/ //g')
# docker exec -it reco service ssh start
# docker exec -it reco service ssh status
ssh trinity@$containerIP
