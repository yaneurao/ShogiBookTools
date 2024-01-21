# 16手目で評価値の絶対値が100以内
bestmove, besteval,*_ = book_node[0]
if sfen_ply(sfen) == 24 and abs(besteval) <= 100:
    # 24手目かつ100以内なら何もしない
    pass
else:
    # さもなくば、この局面は削除
    book_node = None
