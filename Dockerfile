FROM kalilinux/kali-rolling
# FROM ubuntu:impish

# DEBIAN_FRONTEND=nointeractive; So it doesn't prompt for location
RUN apt-get update && \
    apt-get install --no-install-recommends dbus systemd -y && \
    apt install openssh-server sudo -y && \
    DEBIAN_FRONTEND=noninteractive apt install -y python3-pip


RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends evince file-roller gnome-themes-standard gpicview gtk2-engines-pixbuf xfce4 xfce4-whiskermenu-plugin xorg xserver-xorg xfce4-indicator-plugin xfce4-terminal numix-icon-theme numix-icon-theme-circle
#ttf-ubuntu-font-family # wasn't installing right in kali

RUN DEBIAN_FRONTEND=noninteractive apt-get install -y xrdp locales supervisor sudo ibus ibus-mozc dbus dbus-x11

RUN locale-gen en_US && \
    apt-get install -y git tigervnc-standalone-server && \
    git clone https://github.com/novnc/noVNC.git /root/noVNC && \
    git clone https://github.com/novnc/websockify.git /root/noVNC/utils/websockify

RUN mkdir -p /var/run/dbus 

RUN sed -i -e 's/LogLevel=DEBUG/LogLevel=CORE/g' /etc/xrdp/xrdp.ini && \
    sed -i -e 's/SyslogLevel=DEBUG/SyslogLevel=CORE/g' /etc/xrdp/xrdp.ini && \
    sed -i -e 's/EnableSyslog=true/EnableSyslog=false/g' /etc/xrdp/xrdp.ini && \
    sed -i -e 's/LogLevel=DEBUG/LogLevel=CORE/g' /etc/xrdp/sesman.ini && \
    sed -i -e 's/SyslogLevel=DEBUG/SyslogLevel=CORE/g' /etc/xrdp/sesman.ini && \
    sed -i -e 's/EnableSyslog=true/EnableSyslog=false/g' /etc/xrdp/sesman.ini

RUN useradd -m -s /bin/bash -G sudo trinity

COPY ./themes/Adwaita-dark-Xfce-with-Qbox-mw4 /usr/share/themes/Adwaita-dark-Xfce-with-Qbox-mw4
COPY ./themes/xfce-perchannel-xml /etc/xdg/xfce4/xfconf/xfce-perchannel-xml
COPY ./themes/xfce-perchannel-xml /home/trinity/.config/xfce4/xfconf/xfce-perchannel-xml
COPY ./resources/helpers.rc /etc/xdg/xfce4/helpers.rcw

RUN ln -s /root/noVNC/vnc_lite.html /root/noVNC/index.html && \
    ln -s /usr/share/icons/Numix-Circle /usr/share/icons/KXicons && \ 
    chown -R trinity /usr/share/themes/Adwaita-dark-Xfce-with-Qbox-mw4 && \
    chown -R trinity /usr/share/icons/KXicons && \
    chown -R trinity /etc/xdg/xfce4/xfconf/xfce-perchannel-xml

RUN echo "xfce4-session" > /etc/skel/.xsession
    
RUN apt-get install -y xfce4-taskmanager mousepad wget

COPY ./install/* /

RUN ./install.sh

RUN service ssh start && service ssh restart

RUN service xrdp start && service xrdp restart

RUN rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# EXPOSE 22

# EXPOSE 3389

COPY ./resources/entrypoint.sh .
RUN chmod +x entrypoint.sh
COPY ./resources/supervisord.conf /etc/supervisor/conf.d/supervisord.conf
ENTRYPOINT ["./entrypoint.sh"]
# CMD ["/bin/bash"]