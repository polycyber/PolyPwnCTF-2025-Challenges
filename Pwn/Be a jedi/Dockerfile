FROM ubuntu:latest

RUN apt-get update && apt-get install -y socat adduser sudo

RUN rm /usr/bin/unminimize
RUN apt-get remove --purge -y --allow-remove-essential apt && rm -rf /var/lib/apt/lists/*

RUN echo '8Zev5vHTFghA3r\n8Zev5vHTFghA3r\n\n\n\n\n\n\n' | adduser user

COPY jedi /home/user/
COPY flag.txt /home/user/

RUN chmod 777 /home/user/jedi \
    && chmod 444 /home/user/flag.txt

WORKDIR /home/user

EXPOSE 4445

CMD sudo -u user socat TCP-LISTEN:4445,reuseaddr,fork EXEC:/home/user/jedi