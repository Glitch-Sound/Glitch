FROM node:lts-buster-slim

WORKDIR /app/glitch

COPY ./app/glitch/package*.json ./

RUN apt-get update && \
    apt-get install -y build-essential && \
    npm install -g npm && \
    npm install

COPY ./app/glitch .

CMD ["npm", "run", "dev"]
