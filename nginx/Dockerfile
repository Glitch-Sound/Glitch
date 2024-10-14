# buikd
FROM node:lts-buster-slim AS frontend-builder

WORKDIR /app
# フロントエンドの依存関係をコピー
COPY frontend/app/glitch/package*.json ./glitch/

WORKDIR /app/glitch
# 依存関係をインストール
RUN npm install

COPY frontend/app/glitch .

RUN npm run build


# server.
FROM nginx:alpine

COPY nginx/nginx.conf /etc/nginx/conf.d/default.conf

COPY --from=frontend-builder /app/glitch/dist /usr/share/nginx/html
