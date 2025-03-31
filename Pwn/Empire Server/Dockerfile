FROM ubuntu:latest

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    bash \
    build-essential \
    libmicrohttpd-dev \
    unzip \
    gdb && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN rm /usr/bin/unminimize
RUN apt-get remove --purge -y --allow-remove-essential apt && rm -rf /var/lib/apt/lists/*

WORKDIR /root

EXPOSE 9999

COPY src_code.zip /root

COPY flag.txt /root

RUN unzip src_code.zip

WORKDIR /root/src_code

COPY start_services.sh /usr/local/bin/start_service.sh

RUN chmod +x /usr/local/bin/start_service.sh

ENTRYPOINT ["/usr/local/bin/start_service.sh"]

