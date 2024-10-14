#!/bin/bash

# chmod +x docker-down.sh
# ./docker-down.sh dev or ./docker-down.sh prod

ENVIRONMENT=$1

if [ "$ENVIRONMENT" == "dev" ]; then
  sudo docker compose -f docker-compose.yml -f docker-compose.dev.yml down
elif [ "$ENVIRONMENT" == "prod" ]; then
  sudo docker compose -f docker-compose.yml -f docker-compose.prod.yml down
else
  echo "How to use : ./docker-down.sh [dev|prod]"
  exit 1
fi
