FROM ubuntu:latest

RUN apt-get update && apt-get install -y socat adduser sudo libc6-i386

RUN rm /usr/bin/unminimize
RUN apt-get remove --purge -y --allow-remove-essential apt && rm -rf /var/lib/apt/lists/*

RUN echo 'avwRJHnhdQlv4S\navwRJHnhdQlv4S\n\n\n\n\n\n\n' | adduser user

COPY padawan /home/user/
COPY flag.txt /home/user/

RUN chmod 777 /home/user/padawan \
    && chmod 444 /home/user/flag.txt

WORKDIR /home/user

EXPOSE 4446

CMD sudo -u user socat TCP-LISTEN:4446,reuseaddr,fork EXEC:/home/user/padawan