import YaneBookLib.LmdbConnection as book_lmdb
import YaneBookLib.BookIO as book_io

# ============================================================
#                   Helper Functions
# ============================================================

def read_standard_db_book_to_lmdb_book(lmdb_connection : book_lmdb.LMDBConnection, read_path : str , ignore_depth:bool):
    """
    やねうら王標準定跡フォーマットのファイルから読み込んで、LMDBに定跡をstoreする。

    lmdb_connection : LMDBのconnection (openされているものとする)
    read_path    : 読み込むファイル(やねうら王標準定跡フォーマットのファイル)のpath
    ignore_depth : やねうら王標準定跡フォーマットのファイルの定跡局面についている指し手のdepthを無視するかのフラグ。(true = 無視する)
    """

    # BookReaderを用いて、やねうら王形式の定跡ファイルの1局面ずつの読み込みができる。
    with book_io.StandardBookReader(read_path) as reader:
        reader.set_ignore_depth(ignore_depth)

        # DBのトランザクションを作る
        with lmdb_connection.create_transaction(write=True) as txn:
            for book_node in reader:
                sfen , node = book_node
                txn.put_booknode(sfen, node)


def write_lmdb_book_to_standard_book(lmdb_connection : book_lmdb.LMDBConnection, write_path : str):
    """
    LMDBにstoreした定跡をやねうら王標準定跡フォーマットでファイルに書き出す。
    
    書き出したファイルを読み込めばSFEN文字列でsortされている。
    (lmdbはB+Tree構造で格納されているのでkeyでsortされることは保証されているから)

    lmdb_connection : LMDBのconnection (openされているものとする)
    write_path      : 書き込むファイル(やねうら王標準定跡フォーマットのファイル)のpath
    """

    with book_io.StandardBookWriter(write_path) as writer:
        with lmdb_connection.create_transaction(write=False) as txn:
            for (sfen, node) in txn.booknode_cursor():
                writer.write(sfen, node)
