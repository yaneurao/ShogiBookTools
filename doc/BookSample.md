# sample

お品書き

- book_sort.py : 定跡DBのsort(SFEN文字列で並び替え)を行う。
- book_merge.py : 複数の定跡DBのmerge(結合)を行う
- book_add_ply.py : gamePly(初期局面からの手数)が付与されていない定跡DBに対して手数を付与するためのスクリプト
- book_checker.py : ペタショック化後の定跡DBに対してbestmoveなのにdepth 0の指し手を探すためのチェッカー。

## book_sort.py

- [book_sort.py](../sample/book_sort.py) : 定跡DBのsortを行う。

巨大定跡ファイルは実行時にメモリに丸読みするには大きすぎるので、やねうら王のエンジンオプションのBookOnTheFlyと言うオプションをオンにして利用します。これをオンにすると、二分探索で定跡ファイルを調べるのですが、二分探索するためには定跡の局面文字列(SFEN文字列)で辞書順に並び替えが行われている必要があります。

この並び替えを行うのがこのスクリプトです。巨大ファイルなのでメモリに丸読みはできませんので、メモリに丸読みせずにこの並び替えを実現します。

💡 LMDBと言うDBにいったん格納して、それを書き出すことによって、定跡DBのsortを実現しています。LMDBは、B+Treeで実装されているので、SFEN文字列をkeyとして書き出して、lmdbからcursor(iterator)をもらって順番に列挙するだけでsortが実現できます。

使い方の例

>    python book_sort.py --read_file_path book/user_book1.db -- write_file_path book/user_book1-sorted.db --map_size 1

    map_sizeは、テンポラリとして用いるLMDBのファイルサイズを指定します。(単位は[GB])

    読み込ませる定跡ファイルのファイルサイズの3倍ぐらいの容量があれば良いでしょう。

## book_merge.py

- [book_merge.py](../sample/book_merge.py) : 定跡DBのmergeを行う。

使い方は、book_sort.pyとほぼ同じです。入力ファイルとして複数の定跡DBが指定できます。同じ局面が存在する場合、後に指定したものが優先されます。

使い方の例

>    python book_sort.py --read_file_path book/user_book1.db book/user_book2.db book/user_book3.db --write_file_path book/user_book-merged.db --map_size 1

## book_add_ply.py

- [book_add_ply.py](../sample/book_add_ply.py) : 定跡DBの各局面に手数(gamePly)を付与する。

初期局面から最短で何手で辿りつけるかに基づいて手数をつけます。

定跡生成時に手数が失われていることが多いので、これを復元するためのスクリプトです。

実際の対局時には、手数はなくて困るものではないのです。(やねうら王のエンジンオプションのIgnoreBookPlyをオンにすると手数に関係なく定跡にhitするようにできますので…)

しかし、定跡の編集などを行う時に、50手目までの局面を抽出したいだとか、24手目で評価値の絶対値が100以内であるような局面を抽出したいだとか、そういうことを行いたい時に手数がついていないと困るので、それをこのスクリプトは復元できます。

💡　アルゴリズムとしてはダイクストラ法を用います。またメモリに丸読みするわけにはいかないので、LMDBにいったん定跡を書き出して、それを用いて手数つきの定跡を構成します。

## book_checker

- [book_checker.py](sample/book_checker.py) : ペタショック化後の定跡DBに対してbestmoveなのにdepth 0の指し手を探すためのチェッカー。
