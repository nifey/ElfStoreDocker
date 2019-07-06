FROM centos
ENV container docker

RUN mkdir -p /edgefs/logs

RUN yum install -y iproute
RUN yum install -y traceroute
RUN yum install -y iptables-services
RUN yum install -y iperf3
RUN yum install -y nmap
RUN yum install -y net-tools

RUN yum install -y java-1.8.0-openjdk
RUN yum install -y java-1.8.0-openjdk-devel
RUN yum install -y openssh-clients
RUN yum install -y epel-release
RUN yum install -y fping
RUN yum install -y htop


RUN yum install -y python-pip
RUN pip install psutil==5.6.3
RUN pip install six==1.12.0
RUN pip install termcolor==1.1.0
RUN pip install thrift==0.11.0

RUN mkdir /edgefs/data/
COPY extras/ /edgefs/
