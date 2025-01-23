FROM ubuntu:24.04

RUN apt-get update && \
    apt-get install -y wget build-essential libssl-dev zlib1g-dev libbz2-dev \
    libreadline-dev libsqlite3-dev curl libncurses5-dev libncursesw5-dev \
    xz-utils tk-dev libffi-dev liblzma-dev git && \
    wget https://www.python.org/ftp/python/3.13.0/Python-3.13.0.tgz && \
    tar xzf Python-3.13.0.tgz && \
    cd Python-3.13.0 && \
    ./configure --enable-optimizations && \
    make altinstall

RUN update-alternatives --install /usr/bin/python python /usr/local/bin/python3.13 1 && \
    wget https://bootstrap.pypa.io/get-pip.py && python3.13 get-pip.py && \
    pip3 install --upgrade pip && \
    pip3 install wecom-bot-svr==0.3.0


WORKDIR /data

ENV PYTHONPATH=/data

CMD ["python", "-m", "app.py"]
