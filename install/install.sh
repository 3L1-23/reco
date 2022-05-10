#!/bin/bash
#Tested on Kali; some of these won't work on other linux distro's
#Container is built on ubuntu
# user=myusername   #for vm - comment out for container

echo "This script will install the required dependicies on linux for running red team tools automagically"

#install sudo so install.sh can be ported between vm and container easier
apt install sudo -y 
echo "Done with sudo install"
sudo apt install git -y
echo "Done with git install"
sudo apt install python3 -y < 11
echo "Done with python3 install"
#UNCOMMENT Below IF running && not using the docker container
# sudo apt install python3-pip -y 
# echo "Done with pip3 install"


sudo apt install masscan -y && sudo apt install gobuster -y && sudo apt install nmap -y && sudo apt install sqlmap -y && sudo apt install golang-go -y && sudo apt install wfuzz -y && audo apt install hydra -y && apt install amass -y && sudo apt install wpscan -y && sudo apt install nuclei -y

echo "Main install complete"

pip3 install -r requirements.txt
echo "Done with requirements.txt intall"

mkdir /github/ && cd /github/ && git clone https://github.com/aboul3la/Sublist3r.git

cd /github/ && git clone https://github.com/tomnomnom/waybackurls
cd /github/waybackurls/ && go build main.go && mv main /usr/bin/waybackurls    #https://github.com/tomnomnom/waybackurls (go build $waybackurls.go as whatever default file name and then mv to /usr/bin)

cd /github/ && git clone https://github.com/iamj0ker/bypass-403

cd /github/ && git clone https://github.com/TheRook/subbrute.git


### MAKE SURE THIS WORKS ON NEXT BUILD (did work withiin the container)
# sudo apt install ffuf -y #old way of doing it
git clone https://github.com/ffuf/ffuf ; cd ffuf ; go get ; go build; cp ffuf /usr/bin

# sudo chown -R $user:$user /github/    #for vm - comment out for container

echo "alias reco='cd /reco && python3 reco.py'" >> ~/.bashrc; source ~/.bashrc
echo "alias reco='cd /reco && python3 reco.py'" >> /home/trinity/.bashrc