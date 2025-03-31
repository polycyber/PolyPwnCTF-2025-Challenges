#!/bin/bash

docker build -t operationdarksabotage1_img .

docker rm -f operationdarksabotage1_container

docker run -d -p 2222:22 --name operationdarksabotage1_container operationdarksabotage1_img