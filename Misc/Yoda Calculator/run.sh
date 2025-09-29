#!/bin/bash

docker build -t yoda_calculator_img .

docker rm -f yoda_calculator_container

docker run -d -p 4444:4444 --name yoda_calculator_container yoda_calculator_img