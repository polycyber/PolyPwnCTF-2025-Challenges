#!/bin/bash

docker build -t jedi_img .

docker rm -f jedi_container

docker run -d -p 4445:4445 --name jedi_container jedi_img