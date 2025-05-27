FROM python:3.11

# 必要なパッケージのインストール
RUN apt-get update && apt-get install -y \
    git \
    libopenmpi-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN pip install -U pip &&\
    pip install --no-cache-dir \
    mpi4py

ENV PYTHONPATH=/usr/local/lib/python3.11/site-packages

# ルートユーザーでの実行を許可
ENV OMPI_ALLOW_RUN_AS_ROOT=1
ENV OMPI_ALLOW_RUN_AS_ROOT_CONFIRM=1
