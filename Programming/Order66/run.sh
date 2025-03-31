#!/bin/bash

docker build -t order66_img .

docker rm -f order66_container

docker run -d -p 4444:4444 --name order66_container order66_img