import os
import datetime
from typing import Any

"""
使い方。
    まず最初にopen_logfile()を呼び出す。これでファイルが作られる。
    あとはprint_log()を呼び出すとその内容がファイルに書き出される。
"""

def mkdir(path:str):
    '''フォルダを(なければ)作成する'''
    try:
        dirpath = os.path.dirname(path)
        os.mkdir(dirpath)
    except:
        # すでに存在すると例外が飛んでくるので握りつぶす。
        pass

def make_time_stamp()->str:
    '''現在時刻を文字列化したものを返す。ファイル名に付与するのに用いる。'''
    t_delta = datetime.timedelta(hours=9)
    JST = datetime.timezone(t_delta, 'JST')
    now = datetime.datetime.now(JST)
    d = now.strftime('%Y%m%d%H%M%S')
    return d

class Logger:
    """ファイルに書き出すためのlogger"""

    def __init__(self):
        # ログファイルのhandle
        self.log_file : Any = None # _io.TextIOWrapper

    def print_log(self, *args:...,end:str='\n'):
        """print関数。ログファイルに出力する。ただしopen()していなければ出力しない。"""
        if self.log_file is None:
            return 

        # argsが空の時、これは単なる改行のためのprintであるから無視する。
        if args:
            self.log_file.write(''.join(map(str,args)))
        self.log_file.write(end)
        self.log_file.flush()

    # ログファイルのopen
    def open(self):
        filename = f'log/log_{make_time_stamp()}.log'
        mkdir(filename)
        self.log_file = open(filename,'w',encoding='utf-8')
