# excuse-gen

標準入力から受け取った状況メモをもとに, 指定したトーンや出力形式で言い訳・遅延理由の文面を生成して標準出力へ返すコマンドです.

## 機能

* 標準入力から 1 行 1 件の状況メモを読み込み, 対応する文面を標準出力へ出力します.
* `--level` オプションで文面のトーン (`mild`, `dramatic`) を切り替えられます.
* `--format` オプションで出力形式 (`text`, `tsv`, `json`) を指定できます.
* `--seed` オプションで乱数シードを固定し, 再現性のある出力を得られます.

## 動作環境

* OS: Ubuntu 22.04 / 24.04
* Python: 3.10, 3.11, 3.12

## インストール

リポジトリをクローンし, 実行権限を付与します.

```bash
$ git clone https://github.com/s25c1046ea-star/excuse-gen
.git
$ cd excuse-gen
$ chmod +x excuse_gen.py