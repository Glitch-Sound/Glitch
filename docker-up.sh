#!/bin/bash

# chmod +x docker-up.sh
# ./docker-up.sh dev or ./docker-up.sh prod

ENVIRONMENT=$1

if [ "$ENVIRONMENT" == "dev" ]; then
  sudo docker compose -f docker-compose.yml -f docker-compose.dev.yml up --build
elif [ "$ENVIRONMENT" == "prod" ]; then
  sudo docker compose -f docker-compose.yml -f docker-compose.prod.yml up --build
else
  echo "How to use : ./docker-up.sh [dev|prod]"
  exit 1
fi
