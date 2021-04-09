FROM docker.elastic.co/logstash/logstash:7.9.1

# install plugins
# RUN /usr/share/logstash/bin/logstash-plugin install logstash-input-jdbc
# RUN /usr/share/logstash/bin/logstash-plugin install logstash-filter-aggregate
# RUN /usr/share/logstash/bin/logstash-plugin install logstash-filter-jdbc_streaming
# RUN /usr/share/logstash/bin/logstash-plugin install logstash-filter-mutate

# copy jar files
COPY ./jars/postgresql-42.2.19.jar /usr/share/logstash/logstash-core/lib/jars/postgresql.jar
