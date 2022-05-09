#!/bin/bash
#Tested on Kali; some of these won't work on other linux distro's
# user=myusername   #for vm - comment out for container

echo "This script will install the required dependicies on linux for running red team tools automagically"

sudo apt install masscan -y && sudo apt install nmap -y && sudo apt install gobuster -y && sudo apt install sqlmap -y && sudo apt install golang-go -y && sudo apt install python3-pip -y && sudo apt install wfuzz -y && audo apt install hydra -y && apt install amass -y && sudo apt install wpscan -y && sudo apt install ffuf -y && sudo apt install nuclei -y

mkdir /github/ && cd /github/ && git clone https://github.com/aboul3la/Sublist3r.git

cd /github/ && git clone https://github.com/tomnomnom/waybackurls
cd /github/waybackurls/ && go build main.go && mv main /usr/bin/waybackurls    #https://github.com/tomnomnom/waybackurls (go build $waybackurls.go as whatever default file name and then mv to /usr/bin)

cd /github/ && git clone https://github.com/iamj0ker/bypass-403

cd /github/ && git clone https://github.com/TheRook/subbrute.git

# sudo chown -R $user:$user /github/    #for vm - comment out for container

pip3 install -r requirements.txt
gem install wpscan
