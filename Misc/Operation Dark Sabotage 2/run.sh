#!/bin/bash

docker build -t operationdarksabotage2_img .

docker rm -f operationdarksabotage2_container

docker run -d -p 2222:22 --name operationdarksabotage2_container operationdarksabotage2_img