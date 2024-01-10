# ShogiBookTools

将棋AI用の定跡自動生成のために必要なツールセットです。

将棋の超巨大定跡時代を乗り切るために、「10億局面の超巨大定跡でも処理できるように開発しよう！」というコンセプトで開発を始めました。

10億局面クラスの定跡DBのソート、定跡DBのマージ、部分定跡の抽出、戦型判定、戦型選択定跡の生成など定跡DBに関する様々な操作が出来るように開発しています。

ここで言う定跡DBとは、やねうら王の標準定跡フォーマットを指します。

- [やねうら王の標準定跡フォーマット](https://yaneuraou.yaneu.com/2016/02/05/standard-shogi-book-format/)

また、局面を表現するためにUSIプロトコルで定められているSFEN文字列や指し手表現などを用いています。ここで公開されているスクリプトを用いる上で、USIプロトコルについての知識は多少でもあった方が良いでしょう。

- [USIプロトコルとは](http://shogidokoro.starfree.jp/usi.html)

やねうら王の標準定跡フォーマットの定跡ファイルは、1000万局面で2.3GBほどになります。つまり、10億局面だと230GBです。

このような非常に大きな定跡ファイルは、対局時に丸読みするわけにはいきません。やねうら王の思考エンジンには、BookOnTheFlyというオプションが用意されています。これは、定跡DBファイルを二分探索して、現在の局面の定跡を調べる機能です。ところが、二分探索するには、SFEN文字列(局面を表す文字列)でsortされていなくてはなりません。

このsortを行うために、230GBのファイルをいったんメモリに丸読みするのでは大変です。下手するとworking memoryが1TBぐらい必要になります。

このような巨大定跡にまつわる様々な問題を解決するのが、ここにある定跡DBツールセットです。

## 使用方法

ここにあるツールセットはすべてPythonで書かれています。まず、Python本体をインストールしてください。

- Python公式 : https://www.python.org/

また、lmdbというKVS(データベースの一種)を用いるので、インストールしてから使ってください。

> pip install lmdb

⚠ lmdbは、いまのところPython 3.11までしかサポートしていないようですので、注意してください。

## YaneBookLib

YaneBookLibは、Pythonで書かれた、やねうら王の定跡DB処理用のライブラリです。

ここで公開しているツールセットは、間接的にこのライブラリを利用しています。

YaneBookLibにあるいくつかの便利なclassについて紹介しておきます。Pythonが使える人ならば重宝することでしょう。

### BookReader

```Python
from YaneBookLib.BookIO import *

# BookReaderを用いて、やねうら王形式の定跡ファイルの1局面ずつの読み込みができる。
with BookReader("book/user_book1.db") as reader:
    for book_node in reader:
        print(book_node)
        # ('ln2k2nl/1r2g1gs1/p1pspp1p1/6p1p/1p1pbP1S1/2PP5/PPBSP1P1P/2G4R1/LN2KG1NL w P', [('2a3c', 37), ('8e8f', -4)]) みたいなのが表示される。
```

book_node(1つの局面)として SFEN文字列と、それに対応する(指し手文字列,評価値)のlistが返ってきます。

### BookWriter

```Python
from YaneBookLib.BookIO import *

book_nodes : Book = {'ln2k2nl/1r2g1gs1/p1pspp1p1/6p1p/1p1pbP1S1/2PP5/PPBSP1P1P/2G4R1/LN2KG1NL w P': [('2a3c', 37), ('8e8f', -4)]}
# BookWriterを用いて、やねうら王形式の定跡ファイルの1局面ずつ書き出すことができる。
with BookWriter("book/user_book2.db") as writer:
    for sfen, node in book_nodes.items():
        writer.write(sfen, node)
```

### かきかけ。

かきかけ

## 用意されている定跡操作用のPythonのスクリプト

- BookSort : SFEN文字列のsortを行う
- BookMerge : 2つの定跡DBのmerge(結合)を行う
- かきかけ

### BookSort

これを行うのが、BookSortです。

使い方は以下のようになります。

かきかけ

# ライセンス

やねうら王コントリビュートライセンスとします。

これは、
- 自由にソースコードを使うことが許されている。
- やねうら王に(できる範囲で)コントリビュート(貢献)しよう。

というライセンスです。
