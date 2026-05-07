# 使用轻量级 Python 基础镜像
FROM python:3.12-slim

# 设置工作目录
WORKDIR /app

# 先复制依赖文件（利用 Docker 缓存，提高构建速度）
COPY requirements.txt .

# 安装依赖（国内可加镜像源加速，可选）
RUN pip install --no-cache-dir -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

# 复制项目代码（只复制 Mock 服务器及相关模块）
COPY mock_server.py .
COPY common/ ./common/
COPY config/ ./config/

# 暴露端口（Flask 默认 5000）
EXPOSE 5000

# 启动命令
CMD ["python", "mock_server.py"]