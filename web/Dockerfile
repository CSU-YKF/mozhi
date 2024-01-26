# 使用官方的node镜像作为基础镜像
FROM node:latest

# 设置工作目录
WORKDIR /app

# 复制 package.json 和 package-lock.json 到工作目录
COPY ./front/package*.json ./

# 安装项目依赖
RUN npm install

# 复制其他源代码到工作目录
COPY ./front .


EXPOSE 80

# 启动项目
CMD ["npm", "run", "dev"]