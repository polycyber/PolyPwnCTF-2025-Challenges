FROM ubuntu:latest

RUN apt-get update && apt-get install -y openssh-server nano vim man-db sudo\
    && apt-get remove -y wget \
    && apt-get autoremove -y \
    && apt-get clean \
    && mkdir -p /run/sshd

RUN rm /usr/bin/unminimize
RUN apt-get remove --purge -y --allow-remove-essential apt && rm -rf /var/lib/apt/lists/*

RUN echo 'tDVXaDH6bCNY9V\ntDVXaDH6bCNY9V\n\n\n\n\n\n\n' | adduser x-wings

COPY flag.txt /home/x-wings/

RUN chmod 440 /home/x-wings/flag.txt \
    && echo 'x-wings ALL=(root) NOPASSWD: /usr/bin/env' >> /etc/sudoers

EXPOSE 22

CMD ["/usr/sbin/sshd", "-D"]