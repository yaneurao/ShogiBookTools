# 1番目の指し手の指し手文字列と評価値を取得
# 指し手は評価値順に並んでいるので、これでbestmoveとその評価値が得られる。
bestmove, besteval,*_ = book_node[0]
if abs(besteval) <= 100:
    # 100以内なら何もしない
    pass
else:
    # さもなくば、この局面は削除
    book_node = None
