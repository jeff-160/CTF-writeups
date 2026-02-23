FROM oven/bun@sha256:b5cf5ca5dc3e2a02d805802ba089401c4beabf597daabbf35a17b8e82dc2f7bc

# Install ImageMagick
RUN apt-get update && \
    apt-get install -y imagemagick && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy package files
COPY package.json bun.lock ./

# Install dependencies
RUN bun install --frozen-lockfile

# Copy application files
COPY server.ts ./
COPY public ./public
COPY lib ./lib

# Create tmp directory
RUN mkdir -p ./tmp

ENV FLAG=TSGCTFDUMMY{}
ENV PORT=3000

CMD ["bun", "run", "server.ts"]


