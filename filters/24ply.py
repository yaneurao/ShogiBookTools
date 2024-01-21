# 24手目の局面を抽出する
if sfen_ply(sfen) != 24:
    # 24手目でないなら、この局面を削除
    # (book_nodeにNoneを代入すると削除される)
    book_node = None
