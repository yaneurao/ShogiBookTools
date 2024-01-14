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

from YaneBookLib.BookIO import *

sfens : set[str] = set()
for line in open('book/kif20240114.txt','r'):
    # 1行が1つの棋譜
    for sfen in UsiKifToSfens(line):
        # それぞれの局面をsfen形式でset()に格納。
        sfens.add(trim_sfen(sfen))

print(f"kif .. {len(sfens)} sfens.")

board = Board()
with open('checked_sfens.txt','w') as fw:
    with StandardBookReader("book/user_book1-peta20240114.db") as reader:
        # 定跡DBのdepthも読み込む。
        reader.set_ignore_depth(False)
        for i, book_node in enumerate(reader,1):
            # progress
            if i % 100000 == 0:
                print(i)
            
            sfen , node = book_node
            # 末尾の手数の削除
            trimmed_sfen = trim_sfen(sfen)
            if trimmed_sfen in sfens:
                # bestmoveのdepthが1であるかを調べる。
                # nodeはlist[move, eval, depth]の順であるはず
                # 指し手が2つ以上あり、bestmoveのdepth == 0なら、掘れていないのでこの指し手を延長する。
                # ただし、abs(eval) >= 600は延長しない。(そんなところ延長しても…。)
                if len(node) >= 2 and node[0][2] == 0 and abs(node[0][1]) < 600: # type:ignore
                    board.set_position('sfen ' + sfen)
                    # 目視確認のためにnodeをprintしてみる。
                    print(node)
                    # bestmoveで1手進める。
                    board.push_usi(node[0][0])
                    # この局面のsfenをファイルに書き出す。手数は削除しておく。
                    sfen = trim_sfen(board.sfen())
                    fw.write(sfen + '\n')

