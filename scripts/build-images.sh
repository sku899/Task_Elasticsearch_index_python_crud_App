#!/bin/bash
sudo chmod 666 /var/run/docker.sock

#docker-compose down --rmi all 
sudo docker-compose build
sudo docker login
sudo docker-compose push
