FROM golang:1.22.1 AS builder
WORKDIR /app
COPY ./deploy/go.mod ./
RUN go mod download
COPY ./deploy ./
RUN go build -o server main.go

FROM debian:bookworm-slim

ENV GIN_MODE=release

WORKDIR /app
COPY --from=builder /app/server .
COPY --from=builder /app/templates ./templates
COPY ./deploy/files ./files
COPY ./deploy/flag.txt /flag.txt
EXPOSE 8080
CMD ["./server"]