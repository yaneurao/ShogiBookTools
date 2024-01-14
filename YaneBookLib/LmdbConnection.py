import pickle
import os
import shutil
from typing import Any

import lmdb
from YaneBookLib.BookCommon import *

class LMDBConnection:
    def __init__(self, path:str, map_size:int = 3*1024*1024*1024):
        self.path = path
        self.map_size = map_size
        self.env = None

    def __enter__(self):
        self.open()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def open(self, new_db : bool= False):
        """
        DBをopenする。
        new_db = Trueにすると元あったものは削除する。(フォルダごと削除)
        """
        if new_db:
            # 既存のデータベースがあれば削除
            if os.path.exists(self.path):
                shutil.rmtree(self.path)

        self.env = lmdb.open(self.path, sync=True, map_size = self.map_size)
        # sync == Trueを指定すると、即座にdiskに書き込むのでこれはTrueが好ましい。

    def create_transaction(self, write=False)->"LMDBTransaction":
        """
        write = Trueだと書き込めるtransaction。
        writeできるのは1つだけ。readは複数できる。
        """
        if self.env:
            txn = self.env.begin(write=write)
            return LMDBTransaction(txn)
        return None

    def close(self):
        if self.env:
            self.env.close()
            self.env = None

class LMDBCursor:
    def __init__(self, cursor):
        self.cursor_iter = iter(cursor)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb): # type:ignore
        pass

    def __iter__(self):
        return self

    def __next__(self)->tuple[str,Any]:
        try:
            it = next(self.cursor_iter)
            key, value = it
            return key.decode() , pickle.loads(value)
        except:
            raise StopIteration

class LMDBTransaction:
    """
    このclassのinstanceは、LMDBConnection.create_transaction()によって生成される。
    これ以外の方法で作らないようにすること。
    """
    def __init__(self, txn):
        self.txn = txn

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def cursor(self):
        return self.txn.cursor()
    
    def booknode_cursor(self):
        return LMDBCursor(self.txn.cursor())

    def stat(self):
        return self.txn.stat()

    def commit(self):
        if self.txn:
            self.txn.commit()
            self.txn = None

    def abort(self):
        if self.txn:
            self.txn.abort()
            self.txn = None

    def put(self, key:bytes, value:bytes):
        if self.txn:
            self.txn.put(key, value)

    def put_booknode(self, key:str, value:BookNode):
        if self.txn:
            self.txn.put(key.encode(), pickle.dumps(value))

    def get(self, key:bytes)->bytes | None:
        if self.txn:
            value = self.txn.get(key)
            if value:
                return value
        return None

    def close(self):
        # 親切でcommitしておいてやる。
        self.commit()

# 使用例

def unit_test():
    # withを使って書くと

    with LMDBConnection('mylmdb') as db:
        with db.create_transaction(write=True) as txn:
            txn.put('some-key', 'some1-value')
        with db.create_transaction(write=True) as txn:
            txn.put('some-key', 'some2-value')
            txn.abort()
        with db.create_transaction(write=False) as txn:
            print(txn.get('some-key'))

    # withを使わないで書くと…

    try:
        db = LMDBConnection('mylmdb')
        db.open()
        txn = db.create_transaction(write=True)
        txn.put('some-key', 'special-value')
        txn.commit()

        txn = db.create_transaction(write=False)
        print(txn.get('some-key'))
        txn.close()
    finally:
        db.close()
    
# unit_test()
