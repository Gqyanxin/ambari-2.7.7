#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

FROM centos:centos7

RUN echo root:changeme | chpasswd

RUN yum clean all -y && yum update -y
RUN yum -y install firefox-45.8.0-2.el6.centos xvfb xeyes vim wget rpm-build sudo which telnet tar openssh-server openssh-clients ntp git python-setuptools python-devel httpd lsof
RUN rpm -e --nodeps --justdb glibc-common
RUN yum -y install glibc-common

ENV HOME /root

#Install JAVA
ENV JAVA_VERSION 11.0.2
ENV BUILD_VERSION 9

RUN wget --no-check-certificate --no-cookies --header "Cookie:oraclelicense=accept-securebackup-cookie" http://download.oracle.com/otn-pub/java/jdk/${JAVA_VERSION}+${BUILD_VERSION}/f51449fcd52f4d52b93a989c5c56ed3c/jdk-${JAVA_VERSION}_linux-x64_bin.rpm -O jdk-11-linux-x64.rpm
RUN rpm -ivh jdk-11-linux-x64.rpm
ENV JAVA_HOME /usr/java/default/

#Install Selenium server
RUN wget --no-check-certificate -O /root/selenium-server-standalone.jar http://selenium-release.storage.googleapis.com/2.53/selenium-server-standalone-2.53.1.jar

#Install Maven
RUN mkdir -p /opt/maven
WORKDIR /opt/maven
RUN wget http://archive.apache.org/dist/maven/maven-3/3.3.9/binaries/apache-maven-3.3.9-bin.tar.gz
RUN tar -xvzf /opt/maven/apache-maven-3.3.9-bin.tar.gz
RUN rm -rf /opt/maven/apache-maven-3.3.9-bin.tar.gz

ENV M2_HOME /opt/maven/apache-maven-3.3.9
ENV MAVEN_OPTS -Xmx2048m
ENV PATH $PATH:$JAVA_HOME/bin:$M2_HOME/bin

# SSH key
RUN ssh-keygen -f /root/.ssh/id_rsa -t rsa -N ''
RUN cat /root/.ssh/id_rsa.pub > /root/.ssh/authorized_keys
RUN chmod 600 /root/.ssh/authorized_keys
RUN sed -ri 's/UsePAM yes/UsePAM no/g' /etc/ssh/sshd_config
RUN echo 'X11Forwarding yes\n' /etc/ssh/sshd_config
RUN echo 'X11DisplayOffset 10\n' /etc/ssh/sshd_config

#To allow bower install behind proxy. See https://github.com/bower/bower/issues/731
RUN git config --global url."https://".insteadOf git://

# Install Solr
ENV SOLR_VERSION 7.7.3
RUN wget --no-check-certificate -O /root/solr-$SOLR_VERSION.tgz http://public-repo-1.hortonworks.com/ARTIFACTS/dist/lucene/solr/$SOLR_VERSION/solr-$SOLR_VERSION.tgz
RUN cd /root && tar -zxvf /root/solr-$SOLR_VERSION.tgz

# Install Knox
WORKDIR /
RUN adduser knox
ENV KNOX_VERSION 1.0.0
RUN wget -q -O /knox-${KNOX_VERSION}.zip http://archive.apache.org/dist/knox/${KNOX_VERSION}/knox-${KNOX_VERSION}.zip && unzip /knox-${KNOX_VERSION}.zip && rm knox-${KNOX_VERSION}.zip && ln -nsf knox-${KNOX_VERSION} knox && chmod +x /knox/bin/*.sh && chown -R knox /knox/

ADD knox/keystores /knox-secrets
RUN cd /knox-secrets && unzip test-secrets.zip
RUN mkdir -p /knox/data/security/keystores
RUN mv /knox-secrets/master /knox/data/security/master
RUN cd /knox-secrets && cp -r * /knox/data/security/keystores/
RUN chown -R knox /knox/data/security

ADD knox/ldap.sh /ldap.sh
ADD knox/gateway.sh /gateway.sh
RUN touch /gateway.out && chown -R knox /gateway.out
RUN touch /ldap.out && chown -R knox /ldap.out

ADD bin/start.sh /root/start.sh
ADD test-config /root/test-config
ADD test-logs /root/test-logs
RUN chmod -R 777 /root/test-config
RUN chmod +x /root/start.sh

ENV SOLR_CONFIG_LOCATION /root/config/solr
ENV LOGSEARCH_CONF_DIR /root/config/logsearch
ENV LOGFEEDER_CONF_DIR /root/config/logfeeder
ENV SOLR_INCLUDE /root/config/solr/solr-env.sh

RUN mkdir -p /var/run/ambari-logsearch-solr /var/log/ambari-logsearch-solr /var/run/ambari-infra-solr-client \
  /var/log/ambari-infra-solr-client /root/logsearch_solr_index/data \
  /var/run/ambari-logsearch-portal /var/log/ambari-logsearch-portal \
  /var/run/ambari-logsearch-logfeeder /var/log/ambari-logsearch-logfeeder

RUN cp /root/test-config/solr/solr.xml /root/logsearch_solr_index/data
RUN cp /root/test-config/solr/zoo.cfg /root/logsearch_solr_index/data

RUN mkdir -p /root/config
RUN chmod -R 777 /root/config

WORKDIR /root
CMD /root/start.sh
