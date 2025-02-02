FROM node:lts-buster-slim

WORKDIR /app/glitch

COPY ./app/glitch/package.json .
COPY ./app/glitch/package-lock.json .

RUN apt-get update && \
    apt-get install -y build-essential && \
    npm install -g npm@10 && \
    npm install

COPY ./app/glitch .

CMD ["npm", "run", "dev"]
