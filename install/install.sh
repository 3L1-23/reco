#!/bin/bash
# Tested on Kali; some of these won't work on other linux distro's
# Container can be built on ubuntu, initial testing worked but apt updates will be main source moving forward and Ubuntu won't be supported. 

# user=myusername   #for vm - comment out for container

echo "This script will install the required dependicies on linux for running red team tools automagically"

#install sudo so install.sh can be ported between vm and container easier
apt install sudo -y 
echo "Done with sudo install"
sudo apt install vim -y
sudo apt install git -y
echo "Done with git install"
sudo apt install python3 -y < 11
echo "Done with python3 install"
sudo apt install -y wget && sudo apt install unzip -y
echo "Done with wget, unzip install"
#UNCOMMENT Below IF running && not using the docker container
# sudo apt install python3-pip -y 
# echo "Done with pip3 install"

#kali install, run with ubuntu though some will work.
sudo apt install -y masscan gobuster nmap sqlmap golang-go wfuzz hydra-gtk wpscan dirb dirbuster sublist3r ffuf amass nuclei wordlists seclists

echo "Main install complete"

pip3 install -r requirements.txt
echo "Done with requirements.txt intall"

mkdir /github/

####
#ubuntu install (just uncomment this section and still run the rest)
# cd /github/ && git clone https://github.com/aboul3la/Sublist3r.git
# cd /github/ && git clone https://github.com/OJ/gobuster.git; cd gobuster; go get; go build; cp gobuster /usr/bin
# pip3 install --upgrade sqlmap
# cd /github/ && git clone https://github.com/ffuf/ffuf ; cd ffuf ; go get ; go build; cp ffuf /usr/bin

# echo "Installing nuclei"
# cd /github/ && sudo wget https://github.com/projectdiscovery/nuclei/releases/download/v2.7.0/nuclei_2.7.0_linux_amd64.zip && unzip nuclei_2.7.0_linux_amd64.zip && mv nuclei /usr/bin/; rm nuclei_2.7.0_linux_amd64.zip

# echo "Installing amass"
# cd /github/ && sudo wget https://github.com/OWASP/Amass/releases/download/v3.19.2/amass_linux_amd64.zip && sudo unzip amass_linux_amd64.zip && sudo cp amass_linux_amd64/amass /usr/bin/; sudo rm -r amass_linux_amd64; sudo rm amass_linux_amd64.zip

# echo "Downloading wordlists"
# mkdir /usr/share/wordlists/ && cd /usr/share/wordlists && git clone https://github.com/00xBAD/kali-wordlists.git && mv kali-wordlists/* .; rm -r kali-wordlists
####

cd /github/ && git clone https://github.com/tomnomnom/waybackurls
cd /github/waybackurls/ && go build main.go && mv main /usr/bin/waybackurls    #https://github.com/tomnomnom/waybackurls (go build $waybackurls.go as whatever default file name and then mv to /usr/bin)

cd /github/ && git clone https://github.com/iamj0ker/bypass-403

cd /github/ && git clone https://github.com/TheRook/subbrute.git

# sudo chown -R $user:$user /github/    #for vm - comment out for container
echo "alias reco='python3 /reco/reco.py'" >> ~/.bashrc; source ~/.bashrc
echo "alias reco='python3 /reco/reco.py'" >> /home/trinity/.bashrc