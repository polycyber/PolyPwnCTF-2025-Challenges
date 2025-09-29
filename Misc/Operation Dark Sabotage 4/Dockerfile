FROM ubuntu:latest

RUN apt-get update && apt-get install -y openssh-server gcc-multilib man-db\
    && apt-get remove -y wget \
    && apt-get autoremove -y \
    && apt-get clean \
    && mkdir -p /run/sshd

RUN rm /usr/bin/unminimize
RUN apt-get remove --purge -y --allow-remove-essential apt && rm -rf /var/lib/apt/lists/*

RUN echo '2FzphpE0pYWHKr\n2FzphpE0pYWHKr\n\n\n\n\n\n\n' | adduser rebel

COPY src.c /home/rebel/
COPY flag.txt /home/rebel/

RUN gcc -o /home/rebel/cat /home/rebel/src.c \
    && chmod u+s /home/rebel/cat \
    && chmod 440 /home/rebel/flag.txt \
    && rm /home/rebel/src.c

EXPOSE 22

CMD ["/usr/sbin/sshd", "-D"]