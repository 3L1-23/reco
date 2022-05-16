#!/bin/bash

container="reco"

# docker start $container

containerIP=$(docker inspect reco | grep -o '"IPAddress":.*' | sort -u | grep -o "[0-9._]" | tr '\n' ' ' | sed 's/ //g')
#Possible XRDP fix
# docker exec -it reco rm /var/run/xrdp/xrdp-sesman.pid
# docker exec -it reco service xrdp start
# docker exec -it reco service xrdp status
remmina -c rdp://trinity:password@$containerIP
# rdesktop -u trinity -p password $containerIP