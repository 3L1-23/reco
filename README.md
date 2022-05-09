# RECO

## Automates red team tools & incorporates custom ones

### WayBackURLS, Sublist3r, NMAP, GoBuster, Live URLS, SQLMap, log4j, XSS Hunter

#### Some editing of the code is required for some modules, the edits are simple and mainly in the os.system commands for sqlmap or other tools with large CLI references

To Do:

<ul>
<li>amass not working right on container; or maybe at all</l>
<li>nuclei</l>
</ul>

## Install & Usage: 

<ol>
<li>Change the variables for XSS payloads to your URL in run/payloads.py </li>
<li>Change the interact.sh variable to your URL in run/reco.py</li>
<li>Set the logdir variable in run/reco.py for logging</li>
<li>Any other variables that are required are at the top or run/reco.py or run/payloads.py</li>
</ol>

### Docker

Edit the run.sh "volume" variable to the location of where you have cloned this repo

To build and run:

```
bash deploy.sh
```

To reconnect if stopped:

```
bash reconnect.sh
```

### RECO

To run with alias edit:

```
reco -h
```

Without alias edit:

```
python3 reco.py -h
```

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