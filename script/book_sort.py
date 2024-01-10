import os, sys
sys.path.append(os.path.abspath('.')) # ⇑ script/ から実行するおまじない。

"""
lmdbと言うDBにいったん格納して、それを書き出すことによって、定跡DBのsortを実現しています。

lmdbは、B+Treeで実装されているので、SFEN文字列をkeyとして書き出して、lmdbからcursor(iterator)を
もらって順番に列挙するだけでsortが実現できます。
"""

from YaneBookLib.BookIO import *
from YaneBookLib.LmdbConnection import *

# lmdbのopen
map_size = 1 * 1024 * 1024 * 1024 # 作業用のDBファイルサイズ(大きめに設定すること)
db_folder = "tmp-db"              # DBフォルダのpath
db = LMDBConnection(db_folder, map_size = map_size)
db.open()

# BookReaderを用いて、やねうら王形式の定跡ファイルの1局面ずつの読み込みができる。
with BookReader("book/user_book1.db") as reader:
    # DBのトランザクションを作る
    with db.create_transaction(write=True) as txn:
        for book_node in reader:
            sfen , node = book_node
            txn.put_booknode(sfen, node)

# 書き出したファイルを読み込めばSFEN文字列でsortされている。
# (lmdbはB+Tree構造で格納されているのでkeyでsortされることは保証されているから)
with BookWriter("book/user_book1-sorted.db") as writer:
    with db.create_transaction(write=False) as txn:
        for (sfen, node) in txn.booknode_cursor():
            writer.write(sfen, node)
