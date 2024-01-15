import YaneBookLib.LmdbConnection as yane_lmdb

class LMDBQueue:
    """
    ダイクストラを行う時になどにqueueが必要になるが、
    メモリを消費したくないのでLMDB上にqueue構造を展開するqueue
    """
    def __init__(self, db : yane_lmdb.LMDBConnection, commit_interval = 10000):
        """
        db : LMDBのデータベース(open済みであるものとする)
        commit_interval : commitする間隔。デフォルト10000。
            これが大きいとパフォーマンスは上がるがメモリ消費量は増える。
        """
        self.db = db
        self.commit_interval = commit_interval

        # keyとなるカウンター
        self.front = 0
        self.back  = 0

        # 毎回transactionを閉じると遅いので1000回に1回にしておく。
        self.txn = self.db.create_transaction(write=True)

    def push(self, data:bytes):
        """queueに積む。"""
        key = self.front.to_bytes(8, 'little')
        self.txn.put(key, data)
        self.front += 1

        # 定期的にcommitをする(これでメモリは解放される)
        if self.front % self.commit_interval == 0:
            # いったんclose。commitは勝手にしてくれる
            self.txn.close()
            # 再度create
            self.txn = self.db.create_transaction(write=True)

    def pop(self)->bytes:
        """queueから取り出す。"""
        if self.front == self.back:
            raise RuntimeError('no data')
        key = self.back.to_bytes(8, 'little')
        data = self.txn.get(key)
        self.txn.delete(key)
        self.back += 1
        if data is None:
            # これNoneのはずがないのだが..
            raise RuntimeError('data lost')
        return data

    def __len__(self)->int:
        """ 格納されている要素の個数 """
        return self.front - self.back

if __name__ == "__main__": 

    with yane_lmdb.LMDBConnection("lmdb-tmp") as db:
        queue = LMDBQueue(db)
        for i in range(0, 1000000000):
            data = f"個数は{i}".encode('utf-8')
            queue.push(data)
            if i > 10000:
                data2 = queue.pop()
                s = data2.decode('utf-8')

            # progress
            if i % 1000 == 0:
                print(i)

