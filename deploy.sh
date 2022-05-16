#!/bin/bash

echo "Did you change the volume path to the path where reco has cloned in docker-compose.yml?"

sleep 2

docker-compose up -d

#old way of doing it
# docker run -dit --cap-add NET_ADMIN -v ~/vmShared/github/reco/run:/reco/ reco

# bash build.sh
# bash run.sh

echo "Your container IP is: "
docker inspect reco | grep -o '"IPAddress":.*' | sort -u | grep -o "[0-9._]" | tr '\n' ' ' | sed 's/ //g'

# docker logs reco    #get passwords
docker ps
# bash ssh_connect.sh