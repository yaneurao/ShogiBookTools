from copy import deepcopy

from typing import Callable
from collections import deque

from YaneBookLib.LmdbConnection import *
from YaneBookLib.BookCommon import *
from YaneBookLib.BookIO import *
from YaneBookLib.Collections import *

# ============================================================
#                   Helper Functions
# ============================================================

def read_standard_book_to_lmdb_book(lmdb_connection : LMDBConnection, read_path : str , ignore_depth:bool, trim_ply:bool=False, progress:bool=False):
    """
    やねうら王標準定跡フォーマットのファイルから読み込んで、LMDBに定跡をstoreする。

    lmdb_connection : LMDBのconnection (openされているものとする)
    read_path    : 読み込むファイル(やねうら王標準定跡フォーマットのファイル)のpath
    ignore_depth : やねうら王標準定跡フォーマットのファイルの定跡局面についている指し手のdepthを無視するかのフラグ。(true = 無視する)
    trim_ply     : SFEN文字列のply(手数)を剥がしながら読み込むかのフラグ。(true = 剥がす)
    progress     : 進捗を出力する。(ときどき何局面読めたかの数値が表示される。)
    """

    # BookReaderを用いて、やねうら王形式の定跡ファイルの1局面ずつの読み込みができる。
    with StandardBookReader(read_path) as reader:
        reader.set_ignore_depth(ignore_depth)
        reader.set_trim_ply(trim_ply)

        # DBのトランザクションを作る
        with lmdb_connection.create_transaction(write=True) as txn:
            i = 0
            if progress:
                print(f"read book : {read_path} , ignore_depth = {ignore_depth}, trim_ply = {trim_ply}")
            for book_node in reader:
                i += 1
                if progress and i % 100000 == 0:
                    print(f"read {i} sfens")
                    txn.intermediate_commit()
                sfen , node = book_node
                if trim_ply:
                    sfen = trim_sfen(sfen)
                txn.put_booknode(sfen, node)

            if progress:
                print(f"done..{i} sfens")


def write_lmdb_book_to_standard_book(lmdb_connection : LMDBConnection, write_path : str, progress:bool=False):
    """
    LMDBにstoreした定跡をやねうら王標準定跡フォーマットでファイルに書き出す。
    
    書き出したファイルを読み込めばSFEN文字列でsortされている。
    (lmdbはB+Tree構造で格納されているのでkeyでsortされることは保証されているから)

    lmdb_connection : LMDBのconnection (openされているものとする)
    write_path      : 書き込むファイル(やねうら王標準定跡フォーマットのファイル)のpath
    progress        : 進捗を出力する。(ときどき何局面読めたかの数値が表示される。)
    """

    with StandardBookWriter(write_path) as writer:
        with lmdb_connection.create_transaction(write=False) as txn:
            i = 0
            if progress:
                print(f"write book : {write_path}")

            # エントリーの個数をheaderとして追加で書き出す。
            stats = txn.stat() # type:ignore
            # キーの数を表示
            num_of_entries : int = stats['entries'] # type:ignore
            print(f"Number of entries:{num_of_entries}")
            writer.writeline(f"# NOE:{num_of_entries},SORTED")

            for (sfen, node) in txn.booknode_cursor():
                i += 1
                if progress and i % 100000 == 0:
                    print(f"write {i} sfens")
                writer.write(sfen, node)

            if progress:
                print(f"done..{i} sfens")

def lmdb_book_modify(lmdb_connection : LMDBConnection, modify_func:Callable[[BookNode],BookNode] ,progress:bool=False):
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


# 手数のついていないLMDBに格納されたSFEN文字列に対して手数を付与する。
def lmdb_book_add_ply(lmdb_connection:LMDBConnection, root_sfens:list[str], progress:bool=False):
    # 書き込み用のトランザクション。(1万回ごとに作り直す。)
    with lmdb_connection.create_transaction(write=True) as txn:

        # 処理した個数
        i = 0
        
        queue : deque[str] = deque()
        board = Board()
        for root_sfen in root_sfens:
            # root_sfenから辿っていく。
            board.set_position(root_sfen)
            queue.append(board.sfen())

            while queue:
                sfen = queue.popleft()
                sfen_trimmed = trim_sfen(sfen)
                book_node = txn.get_booknode(sfen_trimmed)
                if book_node is None:
                    continue

                # この局面は手数つきで書き出したので処理済みだから削除。
                txn.delete_booknode(sfen_trimmed)

                # このnodeがあったので、手数が確定したから書き出しておく。
                txn.put_booknode(sfen, book_node)

                # progress
                i += 1
                if i % 10000 == 0:
                    txn.intermediate_commit()
                    if progress:
                        print(f"{i} sfens , {len(queue)} queued.")

                # book_nodeの指し手で進めた局面をqueueに積む
                board.set_position('sfen ' + sfen)
                for move , *_ in book_node:
                    board.push_usi(move)
                    sfen = board.sfen() # 手数がついているはず
                    # このsfenのnodeが未処理であるならqueueに積む。
                    if txn.get_booknode(trim_sfen(sfen)):
                        queue.append(sfen)
                    board.pop()

    if progress:
        print(f"done, {i} sfens.")


def lmdb_book_filter(lmdb_connection:LMDBConnection, filter:str, progress:bool=False):
    """LMDB上の各局面に対して、filterを実行する。"""

    i = 0
    m = 0

    with lmdb_connection.create_transaction(write=False) as read_txn:
        with lmdb_connection.create_transaction(write=True) as write_txn:
            def inc_m():
                nonlocal m
                m += 1
                if m % 10000 == 0:
                    write_txn.intermediate_commit()
            
            for (sfen, book_node) in read_txn.booknode_cursor():
                book_node_org = deepcopy(book_node)
                
                # exec()のなかでbook_nodeは何らかの改変を受ける。
                loc = locals()
                exec(filter, globals(), loc)
                book_node = loc['book_node']

                if book_node is None:
                    # execのなかでbook_node = Noneにされたならこのentryを削除する
                    write_txn.delete_booknode(sfen)
                    inc_m()
                elif book_node != book_node_org:
                    # 内容が書き換わっているので書き戻す。
                    write_txn.put_booknode(sfen, book_node)
                    inc_m()
                i += 1
                if i % 10000 == 0 and progress:
                    print(f"{i} sfens , modified = {m}")

    if progress:
        print(f"done.. {i} sfens")
