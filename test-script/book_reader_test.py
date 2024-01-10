import os, sys
sys.path.append(os.path.abspath('.')) # ⇑ test-script/ から実行するおまじない。

from YaneBookLib.BookIO import *
# BookReaderを用いて、やねうら王形式の定跡ファイルの1局面ずつの読み込みができる。
with BookReader("book/user_book1.db") as reader:
    for book_node in reader:
        print(book_node)
