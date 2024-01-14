import argparse

from YaneBookLib.BookIO import *
from YaneBookLib.LmdbConnection import *

# ArgumentParser の作成
parser = argparse.ArgumentParser(description='Process a file path and a map size.')
# nargs='+'を指定すると1つ以上のfile pathが指定されていることを要請する。
parser.add_argument('--read_file_path', type=str, nargs='+', default=['book/user_book1.db','book/user_book2.db'], help='The path to the DB files')
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

# ファイルは複数指定されている(はず)
for READ_FILE_PATH in args.read_file_path:
    print(f"Read {READ_FILE_PATH} into a temporary DB.")
    # BookReaderを用いて、やねうら王形式の定跡ファイルの1局面ずつの読み込みができる。
    with StandardBookReader(READ_FILE_PATH) as reader:
        reader.set_ignore_depth(args.ignore_depth)

        # DBのトランザクションを作る
        with db.create_transaction(write=True) as txn:
            for book_node in reader:
                sfen , node = book_node
                # 何も考えずにputしているので、同じkeyがあればあとのものが優先される。
                txn.put_booknode(sfen, node)

WRITE_FILE_PATH = args.write_file_path
print(f"Write a temporary book into {WRITE_FILE_PATH}.")
# 書き出したファイルを読み込めばSFEN文字列でsortされている。
# (lmdbはB+Tree構造で格納されているのでkeyでsortされることは保証されているから)
with StandardBookWriter(WRITE_FILE_PATH) as writer:
    with db.create_transaction(write=False) as txn:
        for (sfen, node) in txn.booknode_cursor():
            writer.write(sfen, node)

print("done.")
