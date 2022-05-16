#!/bin/bash
#from class

#!/bin/bash
echo -e "\n Built on https://github.com/qeeqbox/docker-images\n\nCustom kali distro accessible via VNC, RDP or web BUT Ubuntu and RECO"
x1=$(hostname -I | cut -d' ' -f1)
x2=$ROOT_PASSWORD
x3=$TRINITY_PASSWORD
x4=$VNC_PASSWORD
echo -e "\nroot pass -> $x2\n-----------------------\nUsername  -> trinity\nPassword  -> $x3\nVNC pass  -> $x4\n\nhttp://$x1:6080/index.html\n"
echo root:$x2 | chpasswd
echo trinity:$x3 | chpasswd
mkdir -p /home/trinity/.vnc
echo $x4 | vncpasswd -f > /home/trinity/.vnc/passwd
chmod 600 /home/trinity/.vnc/passwd
chown -R trinity:trinity /home/trinity/
unset x1 x2 x3 x4
supervisord 1>/dev/null 2>/dev/null



#old stuff
# echo -e "\nhttps://github.com/qeeqbox/docker-images\n\nCustom Kali distro accessible via VNC, RDP or web"
# x1=$(hostname -I | cut -d' ' -f1)
# x2=$(cat /dev/urandom | tr -dc 'a-zA-Z0-9!@#%^&*_+-=' | fold -w 10 | head -n 1)
# x3=$(cat /dev/urandom | tr -dc 'a-zA-Z0-9!@#%^&*_+-=' | fold -w 10 | head -n 1)
# x4=$(cat /dev/urandom | tr -dc 'a-zA-Z0-9!@#%^&*_+-=' | fold -w 10 | head -n 1)
# echo -e "\nroot pass -> $x2\n-----------------------\nUsername  -> trinity\nPassword  -> $x3\nVNC pass  -> $x4\n\nhttp://$x1:6080/index.html\n"
# echo root:$x2 | chpasswd
# echo trinity:$x3 | chpasswd
# mkdir -p /home/trinity/.vnc
# echo $x4 | vncpasswd -f > /home/trinity/.vnc/passwd
# chmod 600 /home/trinity/.vnc/passwd
# chown -R trinity:trinity /home/trinity/
# unset x1 x2 x3 x4
# supervisord 1>/dev/null 2>/dev/null