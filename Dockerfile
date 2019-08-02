FROM centoselfstorebase
ENV container docker

RUN mkdir /edgefs
COPY preload/ /edgefs/
COPY preload/cli/cluster.conf /
RUN mkdir /edgefs/testData
COPY TestData/ /edgefs/testData
RUN mkdir /edgefs/logs
RUN mkdir /edgefs/data

RUN echo "#!/bin/bash" >> /tc_rule.sh
RUN echo "tc qdisc add dev eth0 handle 1: root htb default 11" >> /tc_rule.sh
RUN echo "tc class add dev eth0 parent 1: classid 1:1 htb rate 90Mbps" >> /tc_rule.sh
RUN echo "tc class add dev eth0 parent 1:1 classid 1:11 htb rate 90Mbit" >> /tc_rule.sh
RUN echo "tc qdisc add dev eth0 parent 1:11 handle 10: netem delay 5ms" >> /tc_rule.sh
RUN chmod a+x /tc_rule.sh

