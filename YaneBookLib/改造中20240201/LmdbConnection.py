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

        # 既存のサイズを縮めるのは危ないので、
        # すでにDBファイルがあるなら、そのファイルサイズか指定されたmap_sizeとの大きい方を指定してやる。
        mdb_path = self.path + "/data.mdb"
        if os.path.exists(mdb_path):
            self.map_size = max(self.map_size, os.path.getsize(mdb_path))
        # ⇨　存在しなかった場合は新規に作られることが確定する。

        self.env = lmdb.open(self.path, sync=True, map_size = self.map_size)
        # sync == Trueを指定すると、即座にdiskに書き込むのでこれはTrueが好ましい。

    def reopen(self):
        """OSのcache使用量を下げるためにいったん閉じて再度openする"""
        if self.is_opened():
            self.close()
            self.open()

    def create_transaction(self, write=False)->"LMDBTransaction":
        """
        write = Trueだと書き込めるtransaction。
        writeできるのは1つだけ。readは複数できる。
        """
        if self.env:
            txn = self.env.begin(write=write)
            return LMDBTransaction(self.env, txn, write)
        return None

    def close(self):
        if self.env:
            self.env.close()
            self.env = None

    def is_opened(self)->bool:
        """
        DBがopenされているかを返す。
        self.envがNoneでなければopen()されてclose()されていない
        """
        return not self.env is None

    def info(self)->dict[str,str]:
        if self.env:
            return self.env.info()
        else:
            raise RuntimeError("DB is not opened.")
        
    def get_env(self):
        return self.env

class LMDBCursor:
    def __init__(self, cursor):
        self.cursor = cursor
        self.cursor.first()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb): # type:ignore
        pass

    def __iter__(self):
        return self

    def __next__(self)->tuple[str,Any]:
        try:
            self.cursor.next()
            return self.cursor.key().decode() , pickle.loads(self.cursor.value())
        except:
            raise StopIteration

    def key(self)->str:
        '''現在のcursor位置のkeyの取得'''
        return self.cursor.key().decode()

    def value(self)->BookNode:
        return pickle.loads(self.cursor.value())

    def next(self)->bool:
        '''次の要素があるかの判定'''
        return bool(self.cursor.next())

    def set_range(self, key:str):
        ''' keyのところまでseekする。'''
        self.cursor.set_range(key.encode())

class LMDBTransaction:
    """
    このclassのinstanceは、LMDBConnection.create_transaction()によって生成される。
    これ以外の方法で作らないようにすること。
    """
    def __init__(self, env, txn, write:bool):
        """
        このオブジェクトは、LMDBConnectionを用いて生成すること。
        env : openしたDB
        txn : LMDBのtransaction
        """
        self.env = env
        self.txn = txn
        self.write = write

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
    
    def get_booknode(self, key:str)->BookNode:
        if self.txn:
            value = self.txn.get(key.encode())
            if value:
                return pickle.loads(value)
        return None

    def delete(self, key:bytes):
        self.txn.delete(key)

    def close(self):
        # 親切でcommitしておいてやる。
        self.commit()

    def intermediate_commit(self):
        """一度commit()して次のtransactionを作る"""
        self.commit() # closeを兼ねる
        self.txn = self.env.begin(write=self.write)

    def drop(self):
        """
        DBの内容をクリアする。
        """
        db = self.env.open_db()
        # delete=Trueにしてもファイルは消えない。
        # ファイル消したいならos.remove()で消すしか…。
        self.txn.drop(db=db, delete=False)


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
