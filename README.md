# ShogiBookTools

ここにあるのは、将棋AI用の定跡自動生成のために必要なツールセットです。

将棋の超巨大定跡時代を乗り切るために、「10億局面の超巨大定跡でも処理できるように開発しよう！」というコンセプトで開発を始めました。

ここにあるツールは、10億局面クラスの定跡DBのソート、定跡DBのマージ、部分定跡の抽出、戦型判定、戦型選択定跡の生成など定跡DBに関する様々な操作が出来ることを目的として開発しています。

# 前提知識とインストール手順について

- [なぜこのようなツールが必要なのか？](doc/ShogiBookToolsの必要性.md)
- [前提知識](doc/前提知識.md)
- [インストール手順](doc/インストール手順.md)

# YaneBookLib

YaneBookLibは、Pythonで書かれた、やねうら王の定跡DB処理用のライブラリです。

ここで公開しているツールセットは、間接的にこのライブラリを利用しています。

- [YaneBookLib ドキュメント](doc/YaneBookLib.md)

例えば、以下のように書くだけで、定跡DBに対して、book_node(1つの局面)として SFEN文字列と、それに対応する(指し手文字列,評価値)のlistが返ってきます。Pythonが使える人ならば、便利に使えると思います。活用してみてください。

```Python
from YaneBookLib.BookIO import *
# BookReaderを用いて、やねうら王形式の定跡ファイルの1局面ずつの読み込みができる。
with StandardBookReader("book/user_book1.db") as reader:
    for book_node in reader:
        print(book_node)
        # ('ln2k2nl/1r2g1gs1/p1pspp1p1/6p1p/1p1pbP1S1/2PP5/PPBSP1P1P/2G4R1/LN2KG1NL w P', [('2a3c', 37), ('8e8f', -4)]) みたいなのが表示される。
```

## Sample

巨大定跡に対するsort、merge、gamePlyの追加など各種ツールが揃っています。

- [BookSample ドキュメント](doc/BookSample.md) 

## Book Maintenance Tool

- [BookMaintenanceTool ドキュメント](doc/book_maintenance.md)

主力のメンテナンスツールです。

対話型環境でやねうら王標準定跡DBをLMDBに読み込んだり、書き出したり、加工したり、抽出したりなど様々な操作ができます。

# ライセンス

やねうら王コントリビュートライセンスとします。

これは、
- 自由にソースコードを使うことが許されている。
- やねうら王に(できる範囲で)コントリビュート(貢献)しよう。

というライセンスです。
