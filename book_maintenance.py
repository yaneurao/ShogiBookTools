# Book Maintenance Tool
# ユーザー入力でさまざまなメンテナンスができる。

import os
import shlex

from YaneBookLib.LmdbConnection import *
from YaneBookLib.BookIO import *
from YaneBookLib.BookTools import *

# ============================================================

# LMDBのフォルダ。ここに番号のサブフォルダが作られる。
DB_FOLDER = "lmdb/"

# ============================================================

def make_db_path(n : int)->str:
    """
    DBのPATHを生成する。
    n : フォルダ番号
    """
    return DB_FOLDER + str(n)

def open_db(db_path: str)->LMDBConnection:
    """LMDBをopenする。"""
    map_size = 1 * 1024 * 1024 * 1024 # default 1GB
    mdb_path = db_path + "/data.mdb"
    # すでにDBファイルがあるなら、そのファイルサイズをmap_sizeとして指定してやる。
    if os.path.exists(mdb_path):
        map_size = os.path.getsize(mdb_path)
    if not os.path.exists(db_path):
        print(f"DB is not exists, so create {db_path}")
    db = LMDBConnection(db_path, map_size)
    db.open()
    print(f"open {db_path} DB, map_size = {map_size}")
    return db


def main():
    # 起動時のDBフォルダ番号
    db_number : int = 0

    if not os.path.exists(DB_FOLDER):
        os.mkdir(DB_FOLDER)

    db_path = make_db_path(db_number)
    db = open_db(db_path)

    ignore_depth : bool = True

    while True:
        try:
            print(f"[{db_number}] : ", end="")
            line = input()
            commands = shlex.split(line)
            if len(commands) == 0:
                continue
            command = commands[0]

            if command == 'quit':
                # プログラムを終了する。
                print("quit program")
                break
            elif command == 'stat':
                # DBの統計情報を出力
                with db.create_transaction() as txn:
                    entries = txn.stat()['entries'] # type:ignore
                print(f"folder = {DB_FOLDER}{db_number}, map_size = {db.info()['map_size']} bytes, entries = {entries} SFENS")
            elif command == 'clear':
                # DBの内容をクリア(ファイルは消さない)
                with db.create_transaction(write=True) as txn:
                    txn.drop()
                print(f"clear {db_path}")
            elif command == "drop":
                # DBの内容を削除(フォルダごと削除)
                db.close()
                shutil.rmtree(db_path)
                print(f"drop {db_path}")
            elif command == 'read':
                # LMDBにやねうら王の定跡ファイルを読み込む
                if len(commands) < 2:
                    print("Error! : book_path needed")
                    continue
                book_path = commands[1]
                print(f"read book : {book_path} , ignore depth = {ignore_depth}")
                read_standard_db_book_to_lmdb_book(db, book_path, ignore_depth=True)
                print("read book done")
            elif command == "ignore_depth":
                # ignore_depthの値を変更。
                if len(commands) < 2:
                    print("Error! : true or false , write it afterword")
                    continue
                ignore_depth = commands[1].lower() == "true"
                print(f"ignore_depth = {'True' if ignore_depth else 'False'}")
            elif command.isdigit():
                # DBの切り替え
                print(f"close {db_path}")
                db.close()
                db_number = int(command)
                db_path = make_db_path(db_number)
                db = open_db(db_path)
            else:
                print(f"Unknown Command : {command}")
        except Exception as e:
            print(f"Exception : {str(e)}")

if __name__ == "__main__":
    main()
