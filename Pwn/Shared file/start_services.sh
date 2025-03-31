#!/bin/bash

cd /home/user/

while true; do
    sudo -u user /home/user/server
    if [ $? -ne 0 ]; then
        echo "Shared file crashed"
    fi
done