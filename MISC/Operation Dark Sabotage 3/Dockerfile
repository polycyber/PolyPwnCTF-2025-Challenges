FROM ubuntu:latest

RUN apt-get update && apt-get install -y openssh-server nano vim gcc-multilib man-db build-essential unzip \
    && apt-get remove -y wget \
    && apt-get autoremove -y \
    && apt-get clean \
    && mkdir -p /run/sshd

RUN rm /usr/bin/unminimize
RUN apt-get remove --purge -y --allow-remove-essential apt && rm -rf /var/lib/apt/lists/*

RUN echo 'TiL3fTYdVYnOPe\nTiL3fTYdVYnOPe\n\n\n\n\n\n\n' | adduser c-3po

COPY code.zip /home/c-3po/
COPY flag.txt /home/c-3po/

RUN cd /home/c-3po/ && unzip code.zip \
    && make \
    && chmod 440 /home/c-3po/* \
    && chmod 777 /home/c-3po/libprint.so \
    && chmod 755 /home/c-3po/exploit_me \
    && chmod u+s /home/c-3po/exploit_me \
    && rm /home/c-3po/code.zip \
    && rm /home/c-3po/Makefile \
    && rm -rf /home/c-3po/src\
    && rm -rf /home/c-3po/include

EXPOSE 22

CMD ["/usr/sbin/sshd", "-D"]