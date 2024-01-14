import os, sys
sys.path.append(os.path.abspath('.')) # ⇑ test-script/ から実行するおまじない。

"""
1. 
定跡DBと棋譜(sfen ... moves ...もしくはstartpos moves ...形式)が与えられた時に、
定跡DBにある棋譜に出現した局面をリストアップする。

2.
1.でリストアップした局面のうち、bestmoveのdepthが0である局面に関して、そのbestmoveで
1手進めた局面のsfen文字列をファイルに書き出す。

というサンプルプログラムです。

・このスクリプトは、何に使えるのか

定跡DBをペタショック化すると、その指し手であと何手まで定跡が続くかという手数が定跡局面の指し手の
depthとして書き込まれます。

これが0だということは、その指し手を指したあとの定跡が途絶えていることがわかります。

bestmoveは評価値の絶対値が一定以上になるまで延長して定跡を掘っていても、ペタショック化したことで、
bestmoveが置き換わり、その局面のbestmoveの先が掘れていないことが多々ありました。

このような指し手を残しておくと、あまりいい影響がないため、ここを掘る必要があります。

ところが、ペタショック化しないとそのような局面がわからないため、ペタショック化した定跡に対して
棋譜を与えて、棋譜の局面が掘られているかをチェックするスクリプトが必要となりました。

それがこのスクリプトです。

YaneBookLibのサンプルとしてもちょうどいい感じの処理内容なので参考になるかと思います。
"""

import cshogi

from YaneBookLib.BookIO import *
# BookReaderを用いて、やねうら王形式の定跡ファイルの1局面ずつの読み込みができる。
with StandardBookReader("book/user_book1.db") as reader:
    for book_node in reader:
        print(book_node)

