#!/bin/bash

docker build -t padawan_img .

docker rm -f padawan_container

docker run -d -p 4446:4446 --name padawan_container padawan_img