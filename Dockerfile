# 사이트 빌드용 Node Docker (Docusaurus build/serve)
FROM node:24-alpine

RUN apk add --no-cache git

WORKDIR /app

COPY package.json package-lock.json ./
RUN npm ci

COPY . .

CMD ["npm", "run", "build"]
