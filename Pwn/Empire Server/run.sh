#!/bin/bash

docker build -t republic_server_pwn .

docker run -d -p 9999:9999 --name republic_server_pwn_container republic_server_pwn