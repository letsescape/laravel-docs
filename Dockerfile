FROM node:24-alpine AS build

WORKDIR /app

COPY package.json package-lock.json ./
RUN npm ci

COPY . .
RUN npm run generate-sidebars
RUN npm run typecheck
RUN npm run build

FROM node:24-alpine

WORKDIR /app

RUN npm install -g serve@latest && npm cache clean --force

COPY --from=build /app/build ./build

EXPOSE 3000

CMD ["serve", "build", "-l", "3000"]
