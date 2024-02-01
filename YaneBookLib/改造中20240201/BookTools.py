from typing import Callable

import YaneBookLib.LmdbConnection as book_lmdb
from YaneBookLib.BookCommon import BookNode
import YaneBookLib.BookIO as book_io

# ============================================================
#                   Helper Functions
# ============================================================

def read_standard_book_to_lmdb_book(lmdb_connection : book_lmdb.LMDBConnection, read_path : str , ignore_depth:bool, trim_ply:bool=True, progress:bool=False, intermediate_reopen:bool=False):
    """
    やねうら王標準定跡フォーマットのファイルから読み込んで、LMDBに定跡をstoreする。

    lmdb_connection : LMDBのconnection (openされているものとする)
    read_path    : 読み込むファイル(やねうら王標準定跡フォーマットのファイル)のpath
    ignore_depth : やねうら王標準定跡フォーマットのファイルの定跡局面についている指し手のdepthを無視するかのフラグ。(true = 無視する)
    progress     : 進捗を出力する。(ときどき何局面読めたかの数値が表示される。)
    intermediate_reopen : 定期的にLMDBをreopenしてメモリを節約する。
        (このとき、同じスレッドで開いているread transactionが無効化されるので注意。)
        cf. https://stackoverflow.com/questions/56905502/lmdb-badrsloterror-mdb-txn-begin-mdb-bad-rslot-invalid-reuse-of-reader-lockta
    """

    # BookReaderを用いて、やねうら王形式の定跡ファイルの1局面ずつの読み込みができる。
    with book_io.StandardBookReader(read_path,trim_ply=trim_ply, ignore_depth=ignore_depth) as reader:

        # DBのトランザクションを作る
        txn = lmdb_connection.create_transaction(write=True)
        i = 0
        if progress:
            print(f"read book : {read_path} , ignore depth = {ignore_depth}")

        for book_node in reader:
            sfen , node = book_node
            txn.put_booknode(sfen, node)

            i += 1
            if progress and i % 100000 == 0:
                print(f"read {i} sfens")

                if intermediate_reopen:
                    # メモリ使用量を下げるためにDB自体をreopenする。
                    txn.commit()
                    lmdb_connection.reopen()
                    txn = lmdb_connection.create_transaction(write=True)
                else:
                    # DBのreopenは、やりすぎなので、transactionのrecreateだけに留める。
                    txn.intermediate_commit()

        txn.commit()
        if progress:
            print(f"done..{i} sfens")


def write_lmdb_book_to_standard_book(lmdb_connection : book_lmdb.LMDBConnection, write_path : str, progress:bool=False):
    """
    LMDBにstoreした定跡をやねうら王標準定跡フォーマットでファイルに書き出す。
    
    書き出したファイルを読み込めばSFEN文字列でsortされている。
    (lmdbはB+Tree構造で格納されているのでkeyでsortされることは保証されているから)

    lmdb_connection : LMDBのconnection (openされているものとする)
    write_path      : 書き込むファイル(やねうら王標準定跡フォーマットのファイル)のpath
    progress        : 進捗を出力する。(ときどき何局面読めたかの数値が表示される。)
    """

    with book_io.StandardBookWriter(write_path) as writer:
        txn = lmdb_connection.create_transaction(write=False)
        i = 0
        if progress:
            print(f"write book : {write_path}")

        stats = txn.stat() # type:ignore
        # キーの数を表示
        num_of_entries : int = stats['entries'] # type:ignore
        print(f"Number of entries:{num_of_entries}")
        writer.writeline(f"# NOE:{num_of_entries},SORTED")

        # ⇨　これ良くないな…。cursorが自動的にreopenする機能を有するべきか…。

        cursor = txn.booknode_cursor()
        while True:
            (sfen, node) = (cursor.key() , cursor.value())
            writer.write(sfen, node)
            i += 1
            if not cursor.next():
                break

            if i % 10 == 0:
                if progress:
                    print(f"write {i} sfens")

                # DBを再openしてcursor再取得する。
                next_key = cursor.key()
                txn.close()
                lmdb_connection.reopen()
                txn = lmdb_connection.create_transaction(write=False)
                cursor = txn.booknode_cursor()
                cursor.set_range(next_key)
        
        txn.close()

        if progress:
            print(f"done..{i} sfens")

def lmdb_book_modify(lmdb_connection : book_lmdb.LMDBConnection, modify_func:Callable[[BookNode],BookNode] ,progress:bool=False):
    """
    やねうら王標準定跡フォーマットのファイルから読み込んで、LMDBに定跡をstoreする。

    lmdb_connection : LMDBのconnection (openされているものとする)
    modify_func  : BookNodeを書き換える関数
    progress     : 進捗を出力する。(ときどき何局面読めたかの数値が表示される。)
    """

    # DBのトランザクションを作る。これはcursorもらってiterateする用。
    with lmdb_connection.create_transaction(write=False) as txn:
        i = 0
        m = 0

        # 書き込み用のトランザクション。(1万回ごとに作り直す。)
        write_txn = lmdb_connection.create_transaction(write=True)
        for (sfen, node) in txn.booknode_cursor():
            i += 1
            if progress and i % 100000 == 0:
                print(f"modify {i} sfens")
            node2 = modify_func(node)
            # 内容が書き換わっているならputする。
            if node != node2:
                write_txn.put_booknode(sfen, node2)
                m += 1
                if m % 10000 == 0:
                    write_txn.intermediate_commit()

        if progress:
            print(f"done..{i} sfens , modified {m} nodes.")
