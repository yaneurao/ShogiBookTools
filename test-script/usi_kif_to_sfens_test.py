import os, sys
sys.path.append(os.path.abspath('.')) # ⇑ test-script/ から実行するおまじない。

from YaneBookLib.BookCommon import *

for line in open('book/kif20240114.txt','r'):
    # 1行が1つの棋譜
    for sfen in UsiKifToSfens(line):
        # それぞれの局面をsfen形式で出力(先頭に"sfen"の文字は無し)
        print(sfen)
