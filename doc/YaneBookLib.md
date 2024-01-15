# YaneBookLibとは？

YaneBookLibは、Pythonで書かれた、やねうら王の定跡DB処理用のライブラリです。

ここで公開しているツールセットは、間接的にこのライブラリを利用しています。

YaneBookLibにあるいくつかの便利なclassについて紹介しておきます。Pythonが使える人ならば重宝することでしょう。

# 定跡処理関係

- StandardBookReader : やねうら王の標準定跡形式のReader(ファイルから読み込み)
- StandardBookWriter : やねうら王の標準定跡形式のWriter(ファイルに書き出し)
- UsiKifToSfens : USIのposition文字列をSFEN文字列のlistにする。

## StandardBookReader

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

## StandardBookWriter

- [standard_book_writer_test.py](test-script/standard_book_writer_test.py)
```Python
from YaneBookLib.BookIO import *

book_nodes : Book = {'ln2k2nl/1r2g1gs1/p1pspp1p1/6p1p/1p1pbP1S1/2PP5/PPBSP1P1P/2G4R1/LN2KG1NL w P': [('2a3c', 37), ('8e8f', -4)]}
# BookWriterを用いて、やねうら王形式の定跡ファイルの1局面ずつ書き出すことができる。
with StandardBookWriter("book/user_book2.db") as writer:
    for sfen, node in book_nodes.items():
        writer.write(sfen, node)
```
StandardBookReaderで読み込んだものを元の形式でファイルに書き出すwriterです。

## UsiKifToSfens

- [usi_kif_to_sfens_test.py](test-script/usi_kif_to_sfens_test.py)

```Python
from YaneBookLib.BookCommon import *

for line in open('book/kif20240114.txt','r'):
    # 1行が1つの棋譜
    for sfen in UsiKifToSfens(line):
        # それぞれの局面をsfen形式で出力(先頭に"sfen"の文字は無し)
        print(sfen)
```

"startpos moves 2g2f 8c8d 7g7f 8d8e"のようなUSIプロトコルで用いるposition文字列("position"コマンドとして渡す文字列)を一つの棋譜とみなして、それぞれに出現した局面のSFEN文字列を返します。

# Collections

巨大な定跡を操作するためには、メモリを使わずにQueue構造やStack構造などを用いるアルゴリズムを使いたいことがあり、そのためにLMDBを用いたコンテナを用意している。

| コンテナ名 | データ構造 | サンプル |
|-|-|-|
|LMDBQueue | Queue | [lmdb_queue_test.py](../test-script/lmdb_queue_test.py)|



