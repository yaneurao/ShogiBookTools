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
read book : book/user_book1.db , ignore depth = True
done..42764 sfens
```

### やねうら王のDBを書き出す

writeコマンドでいまLMDBに読み込まれている定跡を、やねうら王の定跡DBとして書き出すことができます。

```
[0] write book/user_book2.db
write book : book/user_book4.db
done..42764 sfens
```

💡 書き出しは、SFEN文字列でsortして書き出されるため、ここで書き出したやねうら王の定跡DBは、やねうら王のBookOnTheFlyをオンにした状態で使うことができます。

⇨　つまり、readコマンドでやねうら王の定跡を読み込んで、writeコマンドで書き出すことによって、定跡のsortが出来ます。

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


# かきかけ

```
# 定跡のPVを書き出したい
[0] read book book/user_book1.db
[0] pv
```


コマンド一覧(実行後に使えるコマンド)


|コマンド|使い方|例|説明|
|--|--|--|--|
|数字|[数字]|3|LMDBのN番目のフォルダに切り替える。Nは任意の数。例えば3を指定すると lmdb-3/ と言うデータベースフォルダが自動的に作成されます|
|db mapsize|db mapsize [map_size]|db mapsize 3| LMDBのデータベースのマップサイズの変更。map sizeは[GB]単位。デフォルトは1[GB]|
|db delete|db delete| db delete | 作成してあったLMDBのデータベースの削除 |
|stat|stat|stat| LMDBに格納されている定跡の統計情報(局面数など)を出力|
|read book|read book [定跡PATH]|read book book/user_book1.db|やねうら王形式の定跡DBのLMDBへの読み込み|
|write book|write book [定跡PATH]|write book book/user_book2.db|やねうら王形式の定跡DBのLMDBへの書き出し|
|pv|pv|pv| LMDBに読み込ませたデータベースのPV(最善応手列)を求める|
|read black|read black [定跡PATH]|read black book/black_book.db|readコマンドの、先手の局面しか読み込まない版|
|read white|read white [定跡PATH]|read white book/white_book.db|readコマンドの、後手の局面しか読み込まない版|
|write black|write black [定跡PATH]|write black book/black_book.db|writeコマンドの、先手の局面しか書き出さない版|
|write white|write white [定跡PATH]|write white book/white_book.db|writeコマンドの、後手の局面しか書き出さない版|


LMDBのデータベースのフォルダは番号で管理されています。起動時は0です。これは lmdb-0/ というフォルダをLMDBのデータベースフォルダにする(このフォルダがなければ作成する)という意味です。

起動時に

> [0] 

このように表示されているのは、いま、データベースのターゲットが0(lmdb-0)になっているという意味です。(read bookコマンドやwrite bookコマンドは現在のターゲットに対して行われます。)

活用例
- 定跡DBをsortしたい　⇨　read bookコマンドで定跡を読み込んでwrite bookコマンドで定跡を書き出すと、局面のSFEN文字列でsortされている定跡ファイル書き出されるので、sortの代用となります。
- 定跡DBをmergeしたい　⇨　readコマンドを複数回使って複数の定跡をLMDBに読み込み、write bookで書き出すと、定跡のmerge(結合)を行ったことになります。
- 定跡DBのPVを調べたい　⇨　readコマンドで定跡を読み込んで、pvコマンドでPV(最善応手列)を求めることができます。(USIプロトコルの"startpos moves ..."の形式の棋譜として書き出すことができます。)
- 先手と後手で別の定跡DBを組み合わせたい　⇨　read blackコマンドで先手の局面だけ角換わりの定跡を読み込み、read whiteコマンドで後手の局面だけ相掛かりの定跡を読み込み、write bookコマンドで書き出すことで、先手と後手との定跡をマージすることができます。
- LMDBの0番のデータベースが格納されているフォルダ lmdb-0/ の内容をクリアして再度作成したい　⇨　db clear としてから 0 (これはDBを lmdb-0 に切り替えるが、存在しなければ作成されるので、これで作成される。)
- LMDBのサイズが足りないみたいなので大きくしたい　⇨　db mapsize 10 (DBのサイズを10GBにする)

💡　定跡DBのPATHは、"my book/book.db"のようにダブルコーテーションで囲って1つのPATHを指定することもできます。

