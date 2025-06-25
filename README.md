# これは何か？
これは Python で並列処理を行うためのプロジェクトです。
mpi4py は Python で MPI を利用するためのパッケージです。
パッケージの詳細は [こちら（英語）](https://mpi4py.readthedocs.io/en/stable/index.html) から見れます。

本プロジェクトは中村と津曲の共同開発のため、環境の差異をなくすために Docker を用います。
また、Docker を用いた開発がスムーズに行えるように Dev Container を用意しています。

# 本プロジェクトのメンバー
|学籍番号|名前|GitHub の URL|
|:-|:-|:-|
|25GJK08|津曲優斗|https://github.com/TsumagariYuto|
|25GJK09|中村駿太|https://github.com/NAVYSHUNTA|

# 実行方法
Docker の当該コンテナを起動し、コンテナ内（ `workspace` ）に入っていることを前提とします。
`src` フォルダ内にある `sample.py` を 4 つのプロセッサで処理するには次のように書きます（`mpiexec` の部分は `mpirun` でも可能です）。
```
$ mpiexec -np 4 python src/sample.py
```
ルートユーザーでの実行は推奨されていないため、本来は  `--allow-run-as-root` を付ける必要がありますが、本プロジェクトに限り、それを付けなくても実行できるように `.devcontainer/Dockerfile` で環境変数を編集しています。
