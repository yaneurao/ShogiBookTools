# Book Maintenance Tool

主力のメンテナンスツールです。

対話型環境でやねうら王標準定跡DBをLMDBに読み込んだり、書き出したり、加工したり、抽出したりなど様々な操作ができます。

- [book_maintenance.py](./book_maintenance.py) : 

実行方法

> python book_maintenance.py

コマンド一覧(実行後に使えるコマンド)


|コマンド|意味|使い方|例|説明|
|--|--|--|--|--|
|r|Read a book|r [定跡PATH]|r book/user_book1.db|やねうら王形式の定跡DBのLMDBへの読み込み|
|w|Write a book|w [定跡PATH]|w book/user_book2.db|やねうら王形式の定跡DBのLMDBへの書き出し|
|c|Create a LMDB|c [map_size]|c 3| LMDBのデータベースの作成。map sizeは[GB]単位|
|d|Delete a LMDB|d|d | 作成してあったLMDBのデータベースの削除|
|p|PV|p|p| LMDBに読み込ませたデータベースのPV(最善応手列)を求める|
|rb|Read a Black book|rb [定跡PATH]|rb book/black_book.db|rコマンドの、先手の局面しか読み込まない版|
|rw|Read a White book|rw [定跡PATH]|rw book/white_book.db|rコマンドの、後手の局面しか読み込まない版|
|wb|Write a Black book|wb [定跡PATH]|wb book/black_book.db|wコマンドの、先手の局面しか書き出さない版|
|ww|Write a White book|ww [定跡PATH]|ww book/white_book.db|wコマンドの、後手の局面しか書き出さない版|

活用例
- cコマンドでLMDBのデータベースを作成し、rコマンドで定跡を読み込んでwコマンドで定跡を書き出すと、局面のSFEN文字列でsortされている定跡ファイル書き出されるので、sortの代用となります。
- cコマンドでLMDBのデータベースを作成し、rコマンドを複数回使って複数の定跡をLMDBに読み込み、wで書き出すと、定跡のmerge(結合)を行ったことになります。
- cコマンドでLMDBのデータベースを作成し、rコマンドで定跡を読み込んで、pコマンドでPV(最善応手列)を求めることができます。(USIプロトコルの"startpos moves ..."の形式の棋譜として書き出すことができます。)
- cコマンドでLMDBのデータベースを作成し、rbコマンドで先手の局面だけ角換わりの定跡を読み込み、rwコマンドで後手の局面だけ相掛かりの定跡を読み込み、wコマンドで書き出すことで、先手と後手との定跡をマージすることができます。


