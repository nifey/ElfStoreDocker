FROM centoselfstorebase
ENV container docker

RUN mkdir /edgefs
COPY preload/ /edgefs/
RUN mkdir /edgefs/testData
COPY TestData/ /edgefs/testData
RUN mkdir /edgefs/logs
RUN mkdir /edgefs/data

CMD tail -f /dev/null
