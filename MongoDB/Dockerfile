FROM mongo:latest

ENV TERM xterm

ADD ./data/mongodb /data/mongodb
VOLUME /data/mongodb

CMD [ "mongod", "--dbpath", "/data/db", "--port", "27017" ]