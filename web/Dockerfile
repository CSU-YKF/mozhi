# 使用官方的nginx镜像作为基础镜像
FROM nginx:latest

# 将dist文件中的内容复制到nginx的html目录下，这样nginx就可以提供这些静态文件了
COPY ./dist /usr/share/nginx/html

# 暴露80端口
EXPOSE 80

# 启动nginx
CMD ["nginx", "-g", "daemon off;"]