# RECO

## Automates red team tools & incorporates custom ones

### WayBackURLS, Sublist3r, NMAP, GoBuster, Live URLS, SQLMap, log4j, XSS Hunter

#### Usage: 

With Alias Edit:

```
reco -h
```

Without Alias Edit:

```
python3 reco.py -h
```

### Make sure to change the payloads.py XSS payloads to the your URL

## Install Docker & Docker Compose

install_docker_ubuntu.sh:

```bash
#! /bin/bash
if [ "$EUID" -ne 0 ]
  then echo "[-] Please run as root"
  exit
fi

# install the required services, pull docker the right docker for debian
apt-get install -y \
    apt-transport-https \
    ca-certificates \
    curl \
    gnupg-agent \
    software-properties-common

curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -

add-apt-repository -y \
   "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
   $(lsb_release -cs) \
   stable"

apt-get update

#apt-get install -y docker-ce docker-ce-cli containerd.io
apt-get install -y --no-install-recommends docker-ce

# get docker-compose
curl -L "https://github.com/docker/compose/releases/download/1.25.4/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
```