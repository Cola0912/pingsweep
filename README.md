# PingSweep

PingSweepは、指定されたIP範囲のアクティブなデバイスを検出するPythonスクリプトです。

## 特徴

- 指定されたIP範囲内の生きているホストを識別します。
- 新規で見つかったホスト、接続が切れたホスト、変化がないホストを色分けして表示します。
- スキャン結果をファイルに保存し、次回スキャン時に以前の結果と比較します。

## 使い方

特定の範囲を指定してスキャンする場合:
```bash
python3 pingsweep.py 192.168.1.0/24
```

自動でローカルIP範囲を検出してスキャンする場合:
```bash
python3 pingsweep.py
```

## インストール

1. 必要なPythonライブラリをインストールします:
    ```bash
    pip install pythonping
    pip install tqdm
    pip install termcolor
    ```

2. スクリプトをダウンロードし、実行権限を与えます（必要な場合）。

## 実行例

ローカルネットワーク（192.168.1.0/24）をスキャンした場合の出力例です:

```bash
$ python3 pingsweep.py 192.168.1.0/24
Scanning 192.168.1.1: 100%|███████████████████████████████████████████████████████████| 254/254 [00:25<00:00, 10.12host/s]

Alive hosts:
192.168.1.1 (myrouter.local)  # 以前からあるホスト (白)
192.168.1.2 (newdevice.local)  # 新規ホスト (緑)
192.168.1.5  # 自端末 (青)
... その他のホスト ...
```

## 仕組み

PingSweepはネットワーク上のデバイスの生存を確認するためにICMPエコーリクエストを送信し、応答の有無に基づいてそのデバイスの状態を判定します。以下はそのプロセスの概要です:

1. **IP範囲の決定:** スクリプトは、コマンドライン引数で指定されたIP範囲または自端末のIP範囲を使用します。
2. **Pingリクエストの送信:** 各IPアドレスに対して、pythonpingライブラリを使ってPingリクエストを送信します。
3. **応答の確認:** 各IPアドレスから応答があったかどうかをチェックし、応答があればそのIPアドレスは生存しているとみなします。
4. **結果の表示と保存:** 生存しているIPアドレスは色分けして表示され、結果は次回比較のためにJSONファイルに保存されます。

スキャン結果は、新たに見つかったデバイス、消失したデバイス、以前から存在するデバイスに色分けされ、より直感的に理解できます。また、逆DNSルックアップを用いてIPアドレスに関連付けられたホスト名も表示される場合があります。

## ライセンス

このプロジェクトはMITライセンスのもとで公開されています。詳細はLICENSEファイルをご覧ください。
