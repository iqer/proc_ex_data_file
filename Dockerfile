FROM ubuntu:22.04
COPY . /app
WORKDIR /app
RUN sed -i 's/archive.ubuntu.com/mirrors.aliyun.com/g' /etc/apt/sources.list \
    && apt update &&  \
    apt install -y --fix-missing python3 python3-pip && \
    pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
CMD python3 main.py