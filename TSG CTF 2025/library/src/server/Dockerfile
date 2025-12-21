FROM oven/bun@sha256:f48ca3e042de3c9da0afb25455414db376c873bf88f79ffb6f26aec82bdb6da2

COPY . .
RUN bun install --frozen-lockfile

ENV PORT=3000
ENV FLAG=TSGCTFDUMMY{}

CMD bun serve.ts
