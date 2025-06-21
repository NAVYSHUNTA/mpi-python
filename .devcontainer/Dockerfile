# ベースとなる Docker イメージ を指定
# Python 3.11 と mpi4py をインストールするために Miniconda3 を使用する
FROM continuumio/miniconda3

# 仮想環境 mpi-env の作成と mpi4py のインストール
RUN conda create -n mpi-env python=3.11 -y
SHELL [ "conda", "run", "-n", "mpi-env", "/bin/bash", "-c" ]
RUN conda install -c conda-forge mpi4py -y && echo "conda activate mpi-env" >> ~/.bashrc

# mpi4py 以外の Python のライブラリは pip でインストール
RUN pip install --no-cache-dir \
    matplotlib \
    japanize-matplotlib

# コンテナ内で必要なパッケージのインストール
RUN apt-get update && apt-get install -y \
    git \
    tzdata \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# VSCode で import に関する警告を出さないための設定
ENV PYTHONPATH=/opt/conda/envs/mpi-env/lib/python3.11/site-packages:$PYTHONPATH

# ルートユーザーでの実行を許可（並列計算のプログラム実行時）
ENV OMPI_ALLOW_RUN_AS_ROOT=1
ENV OMPI_ALLOW_RUN_AS_ROOT_CONFIRM=1

# タイムゾーンを日本標準時に設定（GitHub に push する時刻がズレないようにするため）
ENV TZ=Asia/Tokyo
