FROM apache/kafka:latest

COPY create-topics.sh /usr/bin/create-topics.sh
RUN chmod +x /usr/bin/create-topics.sh

ENTRYPOINT ["/bin/sh", "-c", "/usr/bin/create-topics.sh && /usr/bin/kafka-server-start.sh /etc/kafka/kafka.properties"]
