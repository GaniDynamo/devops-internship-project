FROM golang:1.22-alpine
RUN apk add --no-cache curl
WORKDIR /app
COPY . .
RUN go build -o service_1 main.go
EXPOSE 8081
CMD ["./service_1"]
