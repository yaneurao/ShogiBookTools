import os, sys
sys.path.append(os.path.abspath('.')) # ⇑ test-script/ から実行するおまじない。

from YaneBookLib.BookIO import *

book_nodes : Book = {'ln2k2nl/1r2g1gs1/p1pspp1p1/6p1p/1p1pbP1S1/2PP5/PPBSP1P1P/2G4R1/LN2KG1NL w P': [('2a3c', 37), ('8e8f', -4)]}
# BookWriterを用いて、やねうら王形式の定跡ファイルの1局面ずつ書き出すことができる。
with StandardBookWriter("book/user_book2.db") as writer:
    for sfen, node in book_nodes.items():
        writer.write(sfen, node)
