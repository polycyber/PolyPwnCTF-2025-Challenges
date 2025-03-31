FROM ubuntu:latest

RUN apt-get update && apt-get install -y gcc-multilib socat adduser coreutils sudo

RUN rm /usr/bin/unminimize
RUN apt-get remove --purge -y --allow-remove-essential apt && rm -rf /var/lib/apt/lists/*

RUN echo 'Uf57YbBI8s6zt2\nUf57YbBI8s6zt2\n\n\n\n\n\n\n' | adduser user

COPY order66.c /home/user/
COPY flag.txt /home/user/

RUN gcc -z execstack -o /home/user/order66 /home/user/order66.c

RUN chown -R user:user /home/user

WORKDIR /home/user

EXPOSE 4444

CMD sudo -u user socat TCP-LISTEN:4444,reuseaddr,fork EXEC:"stdbuf -oL -eL /home/user/order66"
