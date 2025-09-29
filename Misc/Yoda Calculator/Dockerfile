FROM ubuntu:16.04

RUN apt-get update && apt-get install -y python2.7 socat sudo coreutils\
    && apt-get remove -y wget \
    && apt-get autoremove -y \
    && apt-get clean

RUN apt-get remove --purge -y --allow-remove-essential apt && rm -rf /var/lib/apt/lists/*

RUN echo '5iwXLEhwR7e1gj\n5iwXLEhwR7e1gj\n\n\n\n\n\n\n' | adduser yoda

COPY jail_src.py /home/yoda/
COPY flag.txt /home/yoda/39101732858453/

EXPOSE 4444

CMD sudo -u yoda socat TCP-LISTEN:4444,reuseaddr,fork EXEC:"stdbuf -oL -eL /usr/bin/python2.7 /home/yoda/jail_src.py"