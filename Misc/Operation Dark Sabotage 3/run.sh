#!/bin/bash

zip -r code.zip Makefile include/ src/

docker build -t operationdarksabotage3_img .

docker rm -f operationdarksabotage3_container

docker run -d -p 2222:22 --name operationdarksabotage3_container operationdarksabotage3_img