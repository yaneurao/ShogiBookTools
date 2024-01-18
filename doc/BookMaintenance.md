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

💡　定跡DBのPATHは、"my book/book.db"のようにダブルコーテーションで囲ってスペースを含むようなPATHを指定することもできます。

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
read book : book/user_book1.db , ignore depth = True
done..42764 sfens
[0] : shrink
done..42764 sfens , modified 42727 nodes.
[0] : write book/user_book1-shrink.db
write book : book/user_book1-shrink.db
done..42764 sfens
[0] : quit
```


# かきかけ

```
# 定跡のPVを書き出したい
[0] read book book/user_book1.db
[0] pv
```
