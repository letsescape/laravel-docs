# 사이트 빌드용 Node Docker (Docusaurus build/serve)
FROM node:26-alpine

RUN apk add --no-cache git

WORKDIR /app
ENV NODE_OPTIONS=--max-old-space-size=4096
ENV DOCUSAURUS_SITEMAP_LASTMOD=0

COPY package.json package-lock.json ./
RUN npm ci

COPY docusaurus.config.ts sidebars.ts tsconfig.json versions.json ./
COPY docs ./docs
COPY i18n ./i18n
COPY src ./src
COPY static ./static
COPY translation-sync ./translation-sync
COPY versioned_docs ./versioned_docs
COPY versioned_sidebars ./versioned_sidebars

CMD ["npm", "run", "build"]
