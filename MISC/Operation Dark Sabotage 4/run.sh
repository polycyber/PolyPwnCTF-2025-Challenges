#!/bin/bash
#OperationDarkSabotage
docker build -t operationdarksabotage4_img .

docker rm -f operationdarksabotage4_container

docker run -d -p 2222:22 --name operationdarksabotage4_container operationdarksabotage4_img