FROM ubuntu:latest

RUN apt-get update && apt-get install -y openssh-server nano vim gcc-multilib man-db\
    && apt-get remove -y wget \
    && apt-get autoremove -y \
    && apt-get clean \
    && mkdir -p /run/sshd

RUN rm /usr/bin/unminimize
RUN apt-get remove --purge -y --allow-remove-essential apt && rm -rf /var/lib/apt/lists/*

RUN echo '9Y51HjIg6bN2TI\n9Y51HjIg6bN2TI\n\n\n\n\n\n\n' | adduser jhon

COPY src.c /home/jhon/
COPY flag.txt /home/jhon/

RUN gcc -o /home/jhon/exe /home/jhon/src.c \
    && chmod u+s /home/jhon/exe \
    && chmod 440 /home/jhon/flag.txt

EXPOSE 22

CMD ["/usr/sbin/sshd", "-D"]