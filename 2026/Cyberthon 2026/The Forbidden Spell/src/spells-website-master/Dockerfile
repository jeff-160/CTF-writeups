FROM oven/bun:debian AS builder
WORKDIR /home/build

COPY . .
RUN NODE_TLS_REJECT_UNAUTHORIZED=0 bun i

# outputs binary 'dist'
RUN NODE_TLS_REJECT_UNAUTHORIZED=0 bun run build

FROM debian:stable-slim AS runner
WORKDIR /home/app

COPY --from=builder /home/build/dist .

EXPOSE 80
CMD ["./dist"]