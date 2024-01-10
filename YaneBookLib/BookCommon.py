# USIプロトコルのSFEN文字列。ただし先頭の"sfen "と末尾の手数は記されていないものとする。
Sfen = str

# 指し手文字列(USIプロトコルの形式)
Move  = str
# やねうら王形式の定跡DBファイルに書き出す時の指し手に対応する評価値
Eval  = int

# やねうら王形式の定跡DBの1つの局面情報を表現する型
BookNode = list[tuple[Move,Eval]]

# やねうら王形式の定跡ファイルを表現する型(メモリ上もこの型で持つ)
Book     = dict[Sfen,BookNode]

YANEURAOU_BOOK_HEADER_V1 = "#YANEURAOU-DB2016 1.00"
