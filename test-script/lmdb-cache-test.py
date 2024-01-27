import os, sys
sys.path.append(os.path.abspath('.')) # ⇑ test-script/ から実行するおまじない。

from YaneBookLib.LmdbConnection import *

def open_db():
    db = LMDBConnection("lmdb/tmp", map_size= 10 * 1024 * 1024 * 1024)
    db.open()
    return db

db = open_db()
db2 = open_db()
txn = db.create_transaction(write=True)
txn2 = db.create_transaction(write=False)
for i in range(100000000):
    txn.put(str(i).encode(), str(i*123).encode())
    print(txn.get(str(i).encode()).decode())
    if i % 100000 == 0:
        print(i)
        txn.intermediate_commit()

        # txn.commit()
        # db.close()
        # db = open_db()
        # txn = db.create_transaction(write=True)
