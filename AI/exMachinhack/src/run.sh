#!/bin/bash

socat -dd -T1800 \
    tcp-l:1337,reuseaddr,fork,keepalive,su=nobody \
    exec:"/app/handler.sh",stderr
