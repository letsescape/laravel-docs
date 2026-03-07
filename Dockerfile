FROM node:24-alpine AS build

WORKDIR /app

COPY package.json package-lock.json ./
RUN npm ci --ignore-scripts

COPY . .
RUN npm run generate-sidebars && npm run typecheck && npm run build

FROM node:24-alpine

RUN addgroup -S appgroup && adduser -S appuser -G appgroup

WORKDIR /app

RUN npm install -g serve@14.2.6 && npm cache clean --force

COPY --from=build /app/build ./build

RUN chown -R appuser:appgroup /app

USER appuser

EXPOSE 3000

CMD ["serve", "build", "-l", "3000"]
