# ShogiBookTools

ここにあるのは、将棋AI用の定跡自動生成のために必要なツールセットです。

将棋の超巨大定跡時代を乗り切るために、「10億局面の超巨大定跡でも処理できるように開発しよう！」というコンセプトで開発を始めました。

ここにあるツールは、10億局面クラスの定跡DBのソート、定跡DBのマージ、部分定跡の抽出、戦型判定、戦型選択定跡の生成など定跡DBに関する様々な操作が出来ることを目的として開発しています。

# 前提知識とインストール手順について

- [なぜこのようなツールが必要なのか？](doc/ShogiBookToolsの必要性.md)
- [前提知識](doc/前提知識.md)
- [インストール手順](doc/インストール手順.md)

## YaneBookLib

YaneBookLibは、Pythonで書かれた、やねうら王の定跡DB処理用のライブラリです。

ここで公開しているツールセットは、間接的にこのライブラリを利用しています。

YaneBookLibにあるいくつかの便利なclassについて紹介しておきます。Pythonが使える人ならば重宝することでしょう。

### StandardBookReader

- [standard_book_reader_test.py](test-script/standard_book_reader_test.py)
```Python
from YaneBookLib.BookIO import *

# BookReaderを用いて、やねうら王形式の定跡ファイルの1局面ずつの読み込みができる。
with StandardBookReader("book/user_book1.db") as reader:
    for book_node in reader:
        print(book_node)
        # ('ln2k2nl/1r2g1gs1/p1pspp1p1/6p1p/1p1pbP1S1/2PP5/PPBSP1P1P/2G4R1/LN2KG1NL w P', [('2a3c', 37), ('8e8f', -4)]) みたいなのが表示される。
```

book_node(1つの局面)として SFEN文字列と、それに対応する(指し手文字列,評価値)のlistが返ってきます。

### StandardBookWriter

- [standard_book_writer_test.py](test-script/standard_book_writer_test.py)
```Python
from YaneBookLib.BookIO import *

book_nodes : Book = {'ln2k2nl/1r2g1gs1/p1pspp1p1/6p1p/1p1pbP1S1/2PP5/PPBSP1P1P/2G4R1/LN2KG1NL w P': [('2a3c', 37), ('8e8f', -4)]}
# BookWriterを用いて、やねうら王形式の定跡ファイルの1局面ずつ書き出すことができる。
with StandardBookWriter("book/user_book2.db") as writer:
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
