# 사이트 빌드용 Node Docker (Docusaurus build/serve)
FROM node:24-alpine

RUN apk add --no-cache git

WORKDIR /app
ENV NODE_OPTIONS=--max-old-space-size=4096
ENV DOCUSAURUS_SITEMAP_LASTMOD=0

COPY package.json package-lock.json ./
RUN npm ci --ignore-scripts

COPY docusaurus.config.ts sidebars.ts tsconfig.json versions.json ./
COPY docs ./docs
COPY i18n ./i18n
COPY src ./src
COPY static ./static
COPY scripts ./scripts
COPY translation-sync/stale-links.json ./translation-sync/stale-links.json
COPY versioned_docs ./versioned_docs
COPY versioned_sidebars ./versioned_sidebars

CMD ["npm", "run", "build"]
