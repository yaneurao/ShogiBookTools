"""
lmdbと言うDBにいったん格納して、それを書き出すことによって、定跡DBのsortを実現しています。

lmdbは、B+Treeで実装されているので、SFEN文字列をkeyとして書き出して、lmdbからcursor(iterator)を
もらって順番に列挙するだけでsortが実現できます。

使い方)
    python book_sort.py --read_file_path book/user_book1.db --write_file_path book/user_book1-sorted.db --map_size 1

    map_sizeは、テンポラリとして用いるLMDBのファイルサイズを指定します。(単位は[GB])
    読み込ませる定跡ファイルのファイルサイズの3倍ぐらいの容量があれば良いでしょう。
"""

import argparse

from YaneBookLib.BookIO import *
from YaneBookLib.LmdbConnection import *
from YaneBookLib.BookTools import *

# ArgumentParser の作成
parser = argparse.ArgumentParser(description='Process a file path and a map size.')
parser.add_argument('--read_file_path', type=str, default='book/user_book1.db', help='The path to the DB file')
parser.add_argument('--write_file_path', type=str, default='book/user_book1-sorted.db', help='The path to the DB files')
parser.add_argument('--map_size', type=int, default=1, help='The size of the map[GB]')
parser.add_argument('--db_tmp_path', type=str, default="tmp-db", help='LMDB temporary folder')
parser.add_argument('--ignore_depth', type=bool, default=True, help='ignore depth in BookDB')

# 引数を解析
args = parser.parse_args()

# lmdbのopen
map_size = args.map_size * 1024 * 1024 * 1024 # 作業用のDBファイルサイズ(大きめに設定すること)
db_folder = args.db_tmp_path                  # DBフォルダのpath

print("Create a temporary DB.")
db = LMDBConnection(db_folder, map_size = map_size)
db.open(new_db=True)

# 読み込む
READ_FILE_PATH = args.read_file_path
print(f"Read {READ_FILE_PATH} into a temporary DB.")
read_standard_db_book_to_lmdb_book(db, READ_FILE_PATH, ignore_depth=args.ignore_depth)

# 書き出す
WRITE_FILE_PATH = args.write_file_path
print(f"Write a temporary book into {WRITE_FILE_PATH}.")
write_lmdb_book_to_standard_book(db, WRITE_FILE_PATH)

# これだけで並び替えが完了する。

print("done.")
