FROM ubuntu:impish

RUN apt-get update 

RUN DEBIAN_FRONTEND=noninteractive apt install -y python3-pip

RUN apt-get clean

RUN useradd -m trinity -s /bin/bash && usermod -aG sudo trinity

RUN echo 'trinity:password' | chpasswd

COPY ./install/* /

RUN ./install.sh

CMD ["/bin/bash"]