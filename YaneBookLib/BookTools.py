import YaneBookLib.LmdbConnection as book_lmdb
import YaneBookLib.BookIO as book_io

# ============================================================
#                   Helper Functions
# ============================================================

def read_standard_book_to_lmdb_book(lmdb_connection : book_lmdb.LMDBConnection, read_path : str , ignore_depth:bool, progress:bool=False):
    """
    やねうら王標準定跡フォーマットのファイルから読み込んで、LMDBに定跡をstoreする。

    lmdb_connection : LMDBのconnection (openされているものとする)
    read_path    : 読み込むファイル(やねうら王標準定跡フォーマットのファイル)のpath
    ignore_depth : やねうら王標準定跡フォーマットのファイルの定跡局面についている指し手のdepthを無視するかのフラグ。(true = 無視する)
    progress     : 進捗を出力する。(ときどき何局面読めたかの数値が表示される。)
    """

    # BookReaderを用いて、やねうら王形式の定跡ファイルの1局面ずつの読み込みができる。
    with book_io.StandardBookReader(read_path) as reader:
        reader.set_ignore_depth(ignore_depth)

        # DBのトランザクションを作る
        with lmdb_connection.create_transaction(write=True) as txn:
            i = 0
            if progress:
                print(f"read book : {read_path} , ignore depth = {ignore_depth}")
            for book_node in reader:
                i += 1
                if progress and i % 100000 == 0:
                    print(f"read {i} sfens")
                sfen , node = book_node
                txn.put_booknode(sfen, node)

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
        with lmdb_connection.create_transaction(write=False) as txn:
            i = 0
            if progress:
                print(f"write book : {write_path}")
            for (sfen, node) in txn.booknode_cursor():
                i += 1
                if progress and i % 100000 == 0:
                    print(f"write {i} sfens")
                writer.write(sfen, node)

            if progress:
                print(f"done..{i} sfens")
