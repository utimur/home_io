#!/bin/bash

trap 'docker-compose down' SIGINT
docker-compose -f docker-compose.yml -f docker-compose.dev.yml up --build