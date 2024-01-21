# 先手の局面だけを抽出する
if sfen_color(sfen) != BLACK:
    # 先手の局面でないなら、この局面を削除
    # (book_nodeにNoneを代入すると削除される)
    book_node = None
