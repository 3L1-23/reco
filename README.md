# RECO

## Automates red team tools & incorporates custom ones

### WayBackURLS, Sublist3r, NMAP, GoBuster, Live URLS, SQLMap, log4j, XSS Hunter

#### Some editing of the code is required for some modules, the edits are simple and mainly in the os.system commands for sqlmap or other tools with large CLI references

To Do:

<ul>
<li>amass not working right on container; or maybe at all</li>
<li>put all variables into the payloads file??</li>
<li>add symlinks instead of alias's for calling reco?</li>
<li>create a payloads file for sqlmap and other tools so its easy to change payloads and not look at entire code, replaces one above, #3</li>
<li>verify openvpn works, although best to just run this on a minimul install VM</li>
<li>create a yaml/ansible file for the install instead of install.sh</li>
<li>try loop on ssh_connect and rdp_connect</li>
<li>If can get PIA working be nice</li>
</ul>

## Install & Usage: 

<ol>
<li>Change the variables for XSS payloads to your URL in run/payloads.py </li>
<li>Change the interact.sh variable to your URL in run/reco.py</li>
<li>Set the logdir variable in run/reco.py for logging</li>
<li>Any other variables that are required are at the top of run/reco.py or in run/payloads.py</li>
<li>XRDP & SSH are open (SSH is mainly for proxychains type of stuff and you know on xrdp)</li>
<li>VNC HTML 5 view as main Remote Access Tool</li>
<li>Change passwords in docker-compose.yml</li>
</ol>

### Install Docker & Docker Compose

```
sudo bash install_docker_ubuntu.sh
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

### RECO

To find vnc, ssh or xrdp IP

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

To reconnect ssh

```
bash ssh_reconnect.sh
```

To reconnect RDP

```
bash rdp_connect.sh