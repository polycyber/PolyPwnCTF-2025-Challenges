#!/bin/bash
cd server
./build.sh
cd ../client
./build.sh
cd ..
docker-compose up --build