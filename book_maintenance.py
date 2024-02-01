# Book Maintenance Tool
# ユーザー入力でさまざまなメンテナンスができる。

import os
import shlex
import traceback

from YaneBookLib.LmdbConnection import *
from YaneBookLib.BookIO import *
from YaneBookLib.BookTools import *

# ============================================================

# LMDBのフォルダ。ここに番号のサブフォルダが作られる。
DB_FOLDER = "lmdb/"

# 1Gを表す定数
GB = 1024 * 1024 * 1024

# ============================================================

def make_db_path(n : int)->str:
    """
    DBのPATHを生成する。
    n : フォルダ番号
    """
    return DB_FOLDER + str(n)

def open_db(db_path: str, map_size:int | None = None)->LMDBConnection:
    """LMDBをopenする。"""
    mdb_path = db_path + "/data.mdb"
    # すでにDBファイルがあるなら、そのファイルサイズをmap_sizeとして指定してやる。
    if map_size is None:
        if os.path.exists(mdb_path):
            map_size = os.path.getsize(mdb_path)
        else:
            map_size = 1 * GB # default 1GB if map_size is None
    else:
        map_size *= GB # 単位は[GB]なので1Gを掛け算する。
    if not os.path.exists(db_path):
        print(f"DB is not exists, so create {db_path}")

    db = LMDBConnection(db_path, map_size)
    db.open()
    print(f"open {db_path} DB, map_size = {map_size // GB} GB", end="")
    with db.create_transaction() as txn:
        entries = txn.stat()['entries'] # type:ignore
        print(f", entries = {entries}")
    return db

def close_db(db:LMDBConnection, db_path:str):
    """ DBをcloseする(openされていたならば) """
    if db.is_opened():
        print(f"close {db_path}")
        db.close()

def is_true(s:str)->bool:
    """文字列がtrueっぽいかどうかを判定する。"""
    return s.lower().startswith('t') or s == '1'

def main():
    # 起動時のDBフォルダ番号
    db_number : int = 0

    if not os.path.exists(DB_FOLDER):
        os.mkdir(DB_FOLDER)

    db_path = make_db_path(db_number)
    db = open_db(db_path)

    ignore_depth : bool = True
    trim_ply : bool = False

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
                print("quit..")
                break

            elif command == 'stat':
                # DBの統計情報を出力
                with db.create_transaction() as txn:
                    entries = txn.stat()['entries'] # type:ignore
                print(f"folder = {DB_FOLDER}{db_number}, map_size = {db.info()['map_size']//GB} GB, entries = {entries}") # type:ignore

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
                read_standard_book_to_lmdb_book(db, book_path, ignore_depth=ignore_depth, trim_ply=trim_ply, progress=True)

            elif command == "write":
                # LMDBからやねうら王の定跡ファイルに書き出す。
                if len(commands) < 2:
                    print("Error! : book_path needed")
                    continue
                book_path = commands[1]
                write_lmdb_book_to_standard_book(db, book_path, progress=True)

            elif command == "ignore_depth":
                # ignore_depthの値を変更。
                if len(commands) < 2:
                    print("Error! : true or false , write it afterword")
                    continue
                ignore_depth = is_true(commands[1])
                print(f"ignore_depth = {'True' if ignore_depth else 'False'}")

            elif command == "trim_ply":
                # ignore_depthの値を変更。
                if len(commands) < 2:
                    print("Error! : true or false , write it afterword")
                    continue
                trim_ply = is_true(commands[1])
                print(f"trim_ply = {'True' if trim_ply else 'False'}")

            elif command == "map_size":
                # map_sizeの変更
                if len(commands) < 2:
                    print("Error! : map_size needed!")
                    continue
                map_size = int(commands[1])
                # map_sizeを指定してopenしなおす。
                close_db(db, db_path=db_path)
                db = open_db(db_path, map_size = map_size)

            elif command == "shrink":
                # 定跡局面の指し手から、最善手と同じ評価値を持つもの以外の指し手を削除する

                # ⇑のような関数を書く。
                def modify_shrink(node:BookNode)->BookNode:
                    for i in range(1, len(node)):
                        # 何番目までが評価値が同じか調べる。
                        if node[0][1] != node[i][1]:
                            # iの手前までに変更して返す。
                            return node[:i]
                    return node

                lmdb_book_modify(db, modify_shrink , progress=True)

            elif command == "add_ply":
                # 手数のついていないLMDBに格納されたSFEN文字列に対して手数を付与する。
                lmdb_book_add_ply(db, ["startpos"], progress=True)

            elif command == "filter":
                # filterコマンド。局面の列挙中に filters/XXXX.py を execで実行する。
                if len(commands) < 2:
                    print("Error! : filter filename needed!")
                    continue
                filter_path = os.path.join("filters", commands[1]+'.py')
                if not os.path.exists(filter_path):
                    print(f"Error! filter not found! file = {filter_path}")
                    continue
                print(f"filter = {filter_path}")
                with open(filter_path, 'r', encoding='utf-8') as f:
                    filter = f.read()

                lmdb_book_filter(db, filter=filter, progress=True)

            elif command.isdigit():
                # DBの切り替え
                close_db(db, db_path=db_path)
                db_number = int(command)
                db_path = make_db_path(db_number)
                db = open_db(db_path)
            else:
                print(f"Unknown Command : {command}")
        except Exception as e:
            print(f"Exception : {str(e)}")
            traceback.print_exception(e)

if __name__ == "__main__":
    main()
