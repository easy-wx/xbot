# 使用 Ubuntu 22.04 作为基础镜像
FROM ubuntu:22.04

# 设置环境变量以避免交互式安装
ENV DEBIAN_FRONTEND=noninteractive

# 更新包列表并安装必要的依赖和 Python 3.13
RUN apt-get update && \
    apt-get install -y software-properties-common && \
    add-apt-repository ppa:deadsnakes/ppa && \
    apt-get update && \
    apt-get install -y wget build-essential libssl-dev zlib1g-dev libbz2-dev \
    libreadline-dev libsqlite3-dev curl libncurses5-dev libncursesw5-dev \
    xz-utils tk-dev libffi-dev liblzma-dev git python3.13 python3.13-venv python3.13-dev && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# 安装 pip 和所需的 Python 包
RUN wget https://bootstrap.pypa.io/get-pip.py && python3.13 get-pip.py && \
    pip3.13 install --upgrade pip && \
    pip3.13 install --ignore-installed blinker && \
    pip3.13 install wecom-bot-svr==0.3.0 requests && \
    rm get-pip.py


# 设置 PYTHONPATH 环境变量
ENV PYTHONPATH=/data/xbot

# 设置工作目录
WORKDIR /data

# 设置容器启动时的默认命令
CMD ["python3.13", "-m", "xbot.wecom_app"]
