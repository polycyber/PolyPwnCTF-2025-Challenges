FROM ubuntu:latest

RUN apt-get update && apt-get install -y adduser sudo

RUN echo 'gwqu0GEwbBF1Dw\ngwqu0GEwbBF1Dw\n\n\n\n\n\n\n' | adduser user

RUN rm /usr/bin/unminimize
RUN apt-get remove --purge -y --allow-remove-essential apt && rm -rf /var/lib/apt/lists/*

COPY server /home/user/
COPY flag.txt /home/user/
COPY start_services.sh /home/user/

RUN chmod 777 /home/user/server \
    && chmod 444 /home/user/flag.txt \
    && chmod +x /home/user/start_services.sh

EXPOSE 4444

ENTRYPOINT ["/home/user/start_services.sh"]