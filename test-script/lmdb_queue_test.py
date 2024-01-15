import os, sys
sys.path.append(os.path.abspath('.')) # ⇑ test-script/ から実行するおまじない。

from YaneBookLib.LmdbConnection import *
from YaneBookLib.Collections import *

with LMDBConnection("lmdb-tmp") as db:
    # 1万回に1回commitする。なので、1万個分しか物理メモリを消費しない。
    queue = LMDBQueue(db, commit_interval=10000)
    for i in range(0, 10_000_000):
        data = f"個数は{i}".encode('utf-8')
        queue.push(data)
        # 100万個遅れてpopを開始
        # (1万個以降はメモリ使用量は増えない。ディスクアクセスはわりとあるが…)
        if i > 1_000_000:
            data2 = queue.pop()
            s = data2.decode('utf-8')

        # progress
        if i % 1000 == 0:
            print(i)
