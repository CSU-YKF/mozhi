# 第一阶段：构建应用程序
FROM golang:latest AS builder

WORKDIR /app

# 复制 go.mod 和 go.sum 文件并下载依赖项
COPY go.mod go.sum ./
RUN go mod download

# 复制源代码并编译应用程序
COPY api ./api
COPY cmd ./cmd
COPY config ./config
COPY internal ./internal

RUN CGO_ENABLED=0 GOOS=linux go build -a -installsuffix cgo -o server ./cmd/server

# 第二阶段：构建运行镜像
FROM ubuntu:latest

WORKDIR /app

# 从构建阶段复制编译好的应用程序
COPY --from=builder /app/server /app/server

# 复制 config.yaml 到工作目录
COPY ./config/config.yaml /app/config.yaml

# 开启 server
CMD ["./server"]