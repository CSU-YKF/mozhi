# 使用 mysql:latest 作为基础镜像
FROM mysql:latest

# 设置环境变量
ENV MYSQL_ROOT_PASSWORD=root

# 将 SQL 文件添加到 Docker 镜像中
ADD ./datastructure.sql /docker-entrypoint-initdb.d/

# 当容器启动时，MySQL 会自动执行 /docker-entrypoint-initdb.d/ 目录下的所有 .sql 文件