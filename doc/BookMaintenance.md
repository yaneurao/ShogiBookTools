# Book Maintenance Tool

主力のメンテナンスツールです。

対話型環境でやねうら王標準定跡DBをLMDBに読み込んだり、書き出したり、加工したり、抽出したりなど様々な操作ができます。

- [book_maintenance.py](./book_maintenance.py) : 

## 実際のコマンド例

### スクリプトを起動する

コマンドラインから起動してください。

> python book_maintenance.py

### LMDBの作成

起動すると自動的に"lmdb/0"というフォルダにLMDBのDBが作られます。ここは定跡を読み込むための場所です。map_sizeとは、このファイルサイズで、デフォルト1GBです。entiresは、読み込まれた局面数です。

```
DB is not exists, so create lmdb/0
open lmdb/0 DB, map_size = 1 GB, entries = 0
[0]
```

### 統計情報の出力

左端に表示されている [0] とは、0番のDB("lmdb/0")を現在ターゲットとしているという意味です。

statと入力するといまターゲットとしているDBの統計情報を表示できます。
```
[0] : stat
folder = lmdb/0, map_size = 1 GB, entries = 0 SFENS
```

### 終了方法

quitと入力すると囚虜ぅできます。
```
[0] : quit
```

### やねうら王のDBを読み込む

readコマンドでやねうら王の定跡DBを、LMDBに読み込めます。
```
[0] read book/user_book1.db
read book : book/user_book4.db , ignore_depth = True, trim_ply = False
done..42764 sfens
```

💡　定跡DBのPATHは、"my book/book.db"のようにダブルコーテーションで囲ってスペースを含むようなPATHを指定することもできます。

⚠　ignore_depth = Trueと表示されているのは、depthを無視するということです。depthは読み込まれません。depthも読み込みたい時は、"ignore_depth true"(trueは単にtや1でも可)と入力します。これで以降のreadコマンドではdepthも読み込まれます。

⚠　trim_ply = Falseと表示されているのは、定跡DBのSFEN文字列(局面を表す文字列)の末尾についている手数(ply)をトリム(削除)するかどうかについてです。trim_ply = Falseなら削除しません。これを削除するように設定するには、"trim_ply true"(trueは単にtや1でも可)と入力します。これで以降のreadコマンドはplyを削除しながら読み込みます。

### やねうら王のDBを書き出す

writeコマンドでいまLMDBに読み込まれている定跡を、やねうら王の定跡DBとして書き出すことができます。

```
[0] write book/user_book2.db
write book : book/user_book4.db
done..42764 sfens
```

💡 書き出しは、SFEN文字列でsortして書き出されるため、ここで書き出したやねうら王の定跡DBは、やねうら王のBookOnTheFlyをオンにした状態で使うことができます。

⇨　つまり、readコマンドでやねうら王の定跡を読み込んで、writeコマンドで書き出すことによって、定跡のsortが出来ます。

💡　定跡DBのPATHは、"my book/book.db"のようにダブルコーテーションで囲ってスペースを含むようなPATHを指定することもできます。

### LMDBのクリア

clearコマンドで、現在ターゲットとしているLMDBをクリアすることができます。

```
[0] : clear
clear lmdb/0
```

💡 クリアしない限り、前回起動時に読み込んだ定跡もLMDBに残っています。

⇨　つまり、複数回readコマンドを実行して、writeコマンドで書き出すと、定跡のmerge(合併)ができます。同じ局面に関してはあとから読み込んだ情報で上書きされます。

### LMDBの変更

数字だけ入力すると、その番号のLMDBのフォルダを作成してそこに新たにLMDBのDBを作成し、それをターゲットのLMDBとします。

1と入力したなら"lmdb/1"というフォルダが出来ているはずです。

💡 すでにLMDBのDBがそのフォルダに存在する場合は、そのDBを単にopenします。

```
[0] : 1
close lmdb/0
DB is not exists, so create lmdb/1
open lmdb/1 DB, map_size = 1 GB, entries = 0
[1] stat
folder = lmdb/1, map_size = 1 GB, entries = 0 SFENS
```

### LMDBの削除

dropコマンドでLMDBのDBをフォルダごと削除できます。

現在ターゲットとしているDBがフォルダごと削除されます。

```
[1] : drop
drop lmdb/1
[1] : 0
open lmdb/0 DB, map_size = 1 GB, entries = 0
[0] :
```

### LMDBのmap_sizeの変更

LMDBのDBを格納しているファイルのファイルサイズ(これをマップサイズと呼ぶ)は、デフォルトで1GBとなっています。

100MBのやねうら王の定跡ファイルを読み込むならば、その3倍ぐらいの容量が必要となります。足りないと読み込み時にエラーになります。

このmap_sizeはあとからでも変更できます。例えば、map_size 3 とすれば3GBに変更されます。

💡 現在ターゲットとしているLMDBがmap_size変更の対象となります。

```
open lmdb/0 DB, map_size = 1 GB, entries = 0
[0] : map_size 3
close lmdb/0
open lmdb/0 DB, map_size = 1 GB, entries = 0
```

### 定跡ファイルのshrink

定跡局面で、最善手と同じ評価値を持つもの以外の指し手を削除して、定跡DBファイルを小さくしたい。そんな時に役立つコマンドがshirnkです。

まず、readコマンドでLMDBに定跡を読み込み、shrinkコマンドを実行。そのあとwriteすれば、目的が達成できます。
```
open lmdb/0 DB, map_size = 1 GB, entries = 0
[0] : read book/user_book1.db
read book : book/user_book1.db , ignore depth = True,  trim_ply = False
done..42764 sfens
[0] : shrink
done..42764 sfens , modified 42727 nodes.
[0] : write book/user_book1-shrink.db
write book : book/user_book1-shrink.db
done..42764 sfens
[0] : quit
```

### 手数のついていない定跡ファイルに手数をつける

手数がついていない定跡ファイルに手数をつけるコマンドは、 add_ply コマンドです。

これは、初期局面から最短で到達できる手数を付与します。readコマンドで定跡を読み込み、add_plyコマンドを実行し、writeコマンドで定跡を書き出せば、手数のついている定跡ファイルが書き出されます。

```
open lmdb/0 DB, map_size = 10 GB, entries = 42764
[0] : clear
// ⇨　以前起動してた時に読み込んだものが残っている。clearコマンドでクリアする。
clear lmdb/0
[0] : trim_ply true
// ⇨　いまの定跡DBに手数として0がついているのでそれを削除しながらLMDBに読み込む。
trim_ply = True
[0] : read book/user_book4.db
read book : book/user_book4.db , ignore_depth = True, trim_ply = True
done..42764 sfens
[0] : add_ply
// ⇨　add_plyコマンドの実行
10000 sfens , 710 queued.
20000 sfens , 746 queued.
30000 sfens , 574 queued.
40000 sfens , 171 queued.
done, 42703 sfens.
[0] : write book/user_book4_ply.db
// ⇨　ファイルに書き出す。
write book : book/user_book4_ply.db
Number of entries:42764
done..42764 sfens
[0] : quit
quit..
```

### 24手目の局面を書き出す

filterコマンドを使うと特定の条件に合致する局面を書き出すことができます。

その条件をPythonのプログラムで書けます。

事前に書いたプログラムが filters/ フォルダに入っていますので、見てみましょう。

- [filters/24ply.py](../filters/24ply.py)

```Python
# 24手目の局面を抽出する
if sfen_ply(sfen) != 24:
    # 24手目でないなら、この局面を削除
    # (book_nodeにNoneを代入すると削除される)
    book_node = None
```
(解説) sfenという変数にSFEN文字列が入ってきます。sfen_ply()はその手数を調べる関数です。24でないなら、book_nodeを空にしています。こうすることで、その局面は定跡DBから削除されます。

上で書いたfilterを実行してみましょう。

"filters"と言うフォルダ名と、拡張子である.pyは省略できます。(省略しないとエラーになります)

```
[0] : read book/user_book4-ply.db
// ⇨　手数のついている定跡DBを読み込みます。手数がついていないなら、add_plyコマンドでつけてください。
read book : book/user_book4-ply.db , ignore_depth = True, trim_ply = False
done..42764 sfens
open lmdb/0 DB, map_size = 10 GB, entries = 42764
[0] : filter 24ply
// ⇨ filterを実行します。filterコマンドに続けて、filterのスクリプトが入っているPATH(ファイルの場所)を書いてください。
// ⇨ 24ply.pyは24手目の局面を抽出する、上で紹介したフィルターです。
filter = filters/24ply.py
10000 sfens , modified = 9955
20000 sfens , modified = 19739
30000 sfens , modified = 29565
40000 sfens , modified = 39558
done.. 42764 sfens
[0] : stat
// ⇨ statで局面がどれだけ残ったか確認します。442局面残っているみたいです。
folder = lmdb/0, map_size = 10 GB, entries = 442
[0] : write book/book24.db
// ⇨ writeコマンドでやねうら王の定跡DBとして書き出します。これで442局面が書き出されます。
write book : book/book24.db
Number of entries:442
done..442 sfens
```

### 先手番/後手番の局面だけを抽出する

先手番の局面だけを抽出するフィルター。

- [filters/black.py](../filters/black.py)

```Python
# 先手の局面だけを抽出する
if sfen_color(sfen) != BLACK:
    # 先手の局面でないなら、この局面を削除
    # (book_nodeにNoneを代入すると削除される)
    book_node = None
```

後手番の局面だけを抽出するフィルター。

- [filters/white.py](../filters/white.py)

```Python
# 後手の局面だけを抽出する
if sfen_color(sfen) != WHITE:
    # 後手の局面でないなら、この局面を削除
    # (book_nodeにNoneを代入すると削除される)
    book_node = None
```

### 定跡Aの先手局面と定跡Bの後手局面をmergeしたい

手順だけ。

1. readコマンドで定跡Aを読み込む　⇨　filter black として先手の局面のみ残す　⇨　writeコマンドで定跡ファイルに書き出す。
2. 同様にして定跡Bを読み込んむ　⇨　filter white として後手の局面のみ残す　⇨　writeコマンドで定跡ファイルに書き出す。
3. そして書き出した局面をreadコマンドで順番に読み込む。
4. writeコマンドでやねうら王の定跡ファイルに書き出す。

### 他に便利なfilter

サンプルとしていくつかのfilterを用意してあります。これらを改造して使いたいものを用意すると良いでしょう。

- [filters/eval100.py](../filters/eval100.py)

bestmoveの評価値の絶対値が100以内の局面のみ(になるように)filterする。

```Python
# 1番目の指し手の指し手文字列と評価値を取得
# 指し手は評価値順に並んでいるので、これでbestmoveとその評価値が得られる。
bestmove, besteval,*_ = book_node[0]
if abs(besteval) <= 100:
    # 100以内なら何もしない
    pass
else:
    # さもなくば、この局面は削除
    book_node = None
```

- [filters/eval100ply24.py](../filters/eval100ply24.py)

24手目でかつbestmoveの評価値の絶対値が100以内の局面のみfilter。

```Python
# 16手目で評価値の絶対値が100以内
bestmove, besteval,*_ = book_node[0]
if sfen_ply(sfen) == 24 and abs(besteval) <= 100:
    # 24手目かつ100以内なら何もしない
    pass
else:
    # さもなくば、この局面は削除
    book_node = None
```

上のfilterを実際に適用してみる例。
```
[0] : clear
// ⇨　LMDBを空にしよう。
clear lmdb/0
[0] : trim_ply false
// ⇨　手数で判定したいので、定跡を読み込む時に手数を削除されてしまうと困るのでこれをfalseにしよう。
trim_ply = False
[0] : read book/user_book4_ply.db 
// ⇨　手数つきの定跡を読み込もう。定跡に手数がついていないなら、add_plyコマンドでつけたものを書き出しておこう。
read book : book/user_book4_ply.db , ignore_depth = True, trim_ply = False
done..42764 sfens
[0] : filter eval100ply24
// filterコマンドで上のスクリプトを実行しよう。
filter = filters\eval100ply24.py
10000 sfens , modified = 9962
20000 sfens , modified = 19767
30000 sfens , modified = 29623
40000 sfens , modified = 39618
done.. 42764 sfens
// 局面が処理された。modifiedは書き換わった局面数。ここではフィルター条件に合致しない局面の削除が行われている。
[0] : stat
// ⇨　LMDBの情報を見よう。entries = 382ということは、382局面しか残っていないということだ。
folder = lmdb/0, map_size = 10 GB, entries = 382
[0] : write book/eval100ply24.db
// ⇨　局面をやねうら王の定跡ファイルとして書き出してみよう。
write book : book/eval100ply24.db
Number of entries:382
done..382 sfens
[0] : quit
// ⇨　終了コマンド
```

