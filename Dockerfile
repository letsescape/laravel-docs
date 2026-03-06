FROM node:24-alpine AS build

WORKDIR /app

COPY package.json package-lock.json ./
RUN npm ci --ignore-scripts

COPY docusaurus.config.ts sidebars.ts tsconfig.json ./
COPY scripts/ scripts/
COPY src/ src/
COPY docs/ docs/
COPY versioned_docs/ versioned_docs/
COPY versioned_sidebars/ versioned_sidebars/
COPY versions.json ./
COPY static/ static/
RUN npm run generate-sidebars
RUN npm run typecheck
RUN npm run build

FROM node:24-alpine

RUN addgroup -S appgroup && adduser -S appuser -G appgroup

WORKDIR /app

RUN npm install -g serve@14.2.6 && npm cache clean --force

COPY --from=build /app/build ./build

RUN chown -R appuser:appgroup /app

USER appuser

EXPOSE 3000

CMD ["serve", "build", "-l", "3000"]
