# RECO

## Automates Red Team Tools & Incorporates Custom Ones

### WayBackURLS, Sublist3r, NMAP, GoBuster, Live URLS, SQLMap, log4j, XSS Hunter

#### Some editing of the code is required for some modules

#### The edits are simple and mainly in the os.system commands for sqlmap or other tools with large CLI references

## Install & Usage

<ol>
<li>Change the variables for XSS payloads to your URL in run/payloads.py </li>
<li>Change the interact.sh variable to your URL in run/payloads.py</li>
<li>Set the logdir variable in run/payloads.py for logging</li>
<li>Change passwords in docker-compose.yml</li>
<li>Any other variables that are required are at the top of run/payloads.py under Vars section</li>
<li>VNC HTML 5, XRDP & SSH are Remote Access Tools (SSH is mainly for proxychains type)</li>
</ol>

### Install Docker & Docker Compose

```
sudo bash host/install_docker_ubuntu.sh
```

Give your user access to use docker
```
sudo usermod -aG docker $user
sudo reboot
```

### Container Setup

Edit the "volume" variable to the location of where you have cloned this repo in the docker-compose.yml

Build and run:

```
bash deploy.sh
```

### RECO Usage

To find VNC, SSH or XRDP IP

```
docker inspect reco | grep -o '"IPAddress":.*' | sort -u | grep -o "[0-9._]" | tr '\n' ' ' | sed 's/ //g'

```

Run with alias edit:

```
reco -h
```

Without alias edit:

```
python3 reco.py -h
```

## Connect To The Container

HTML5/VNC - This url will give you an option for copy and paste/screen fill (settings on left, "remote resizing")

```
http://localhost/vnc.html
```

To reconnect SSH

```
bash host/ssh_reconnect.sh
```

To reconnect RDP

```
bash host/rdp_connect.sh
```

## Update 

Rebuild the container 

OR

Ensure you are running the container with the -v or volume in the /run folder (this works in container and on normal system)

```
git pull
bash install.sh
```

## To Do

<ul>
<li>add symlinks instead of alias's for calling reco?</li>
<li>verify openvpn works, although best to just run this on a minimul install VM</li>
<li>create a ansible playbook for the install instead of install.sh</li>
<li>try loop on ssh_connect and rdp_connect</li>
<li>If can get PIA working be nice</li>
<li>Create masscan function and break away from nmap</li>
<li>Maybe get ubuntu desktop as the RDP setup</li>
</ul>