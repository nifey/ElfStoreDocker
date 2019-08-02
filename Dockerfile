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
RUN echo "tc qdisc add dev eth0 root tbf rate 1mbit burst 32kbit latency 400ms"  >> /tc_rule.sh
RUN chmod a+x /tc_rule.sh

ENTRYPOINT exec /tc_rule.sh
