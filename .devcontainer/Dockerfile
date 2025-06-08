FROM continuumio/miniconda3

RUN conda create -n mpi-env python=3.11

SHELL [ "conda", "run", "-n", "mpi-env", "/bin/bash", "-c" ]
RUN conda install -c conda-forge mpi4py && echo "conda activate mpi-env" >> ~/.bashrc

# 必要なパッケージのインストール
RUN apt-get update && apt-get install -y \
    git \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

ENV PYTHONPATH=/opt/conda/envs/mpi-env/lib/python3.11/site-packages:$PYTHONPATH

# ルートユーザーでの実行を許可
ENV OMPI_ALLOW_RUN_AS_ROOT=1
ENV OMPI_ALLOW_RUN_AS_ROOT_CONFIRM=1
