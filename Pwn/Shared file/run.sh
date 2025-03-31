#!/bin/bash

docker build -t shared_file_img .

docker rm -f shared_file_container

docker run -d -p 4444:4444 --name shared_file_container shared_file_img