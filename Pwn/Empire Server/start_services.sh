#!/bin/bash

cd /root/src_code && make

while true; do
    /root/src_code/republic_web_server
    if [ $? -ne 0 ]; then
        echo "The web server has encountered a crash"
    fi
done