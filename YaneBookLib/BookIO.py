import io
from YaneBookLib.BookCommon import *

class StandardBookReader:
    """やねうら王標準定跡フォーマットの読み込みclass"""
    def __init__(self, filename:str, ignore_depth:bool=True, trim_ply:bool = True):
        # openするfilepth
        self.filename = filename
        # openしているfile handle
        self.file : io.TextIOWrapper | None = None
        # 定跡局面の指し手に付随しているdepthを無視するかどうか
        self.ignore_depth : bool = ignore_depth
        # SFEN文字列の末尾の手数をtrimするのか
        self.trim_ply : bool = trim_ply

    def open(self, filename:str):
        self.file = open(filename, mode='r', encoding='utf-8')
        self.peeked_line:str|None = None # 前回peek_line()した時の最後の行

    def __enter__(self):
        self.open(self.filename)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb): # type:ignore
        if self.file:
            self.file.close()

    def __iter__(self):
        return self

    def __next__(self)->tuple[Sfen,BookNode]:
        book_node = self.parse_next()
        if book_node is None:
            raise StopIteration
        return book_node

    def parse_next(self)->tuple[Sfen,BookNode] | None:
        '''
        次のBookNodeを一つ読み込んで返す。
        もう定跡がなければNoneが返る。
        '''

        while True:
            line = self.peek_line()
            # 終端(空行は'\n'がある。終端なら''だからnot lineがTrueになる)
            if not line:
                return None
            # ヘッダー行 もしくはコメント行。
            self.get_line() # feed
            if line.startswith('#'):
                pass
            elif line.startswith('sfen'):
                # 先頭の'sfen'の文字と末尾に付随している手数を削除する。
                sfen = trim_sfen(line, trim_ply=self.trim_ply)

                # 指し手の読み込み..
                book_node:BookNode = []
                while True:
                    line = self.peek_line()
                    # 終端か次のsfenに達した。
                    if not line or line.startswith('sfen'):
                        # book_node、evalの値で降順sortしておく。(評価値順に並んで欲しいため)
                        book_node.sort(key=lambda x: x[1], reverse=True)
                        return (sfen, book_node)
                    self.get_line() # feed
                    if self.ignore_depth:
                        move, _, eval, *_ = line.split()
                        book_node += (move, int(eval)),
                    else:
                        move, _, eval, depth, *_ = line.split()
                        book_node += (move, int(eval), int(depth)),

    def close(self):
        if self.file:
            self.file.close()

    def set_ignore_depth(self, b:bool):
        '''定跡局面に付随しているdepthを無視するのかどうかのフラグを変更する。デフォルトではtrue。(無視する)'''
        self.ignore_depth = b

    def set_trim_ply(self, b:bool):
        '''定跡局面のSFENに付随しているplyをtrimするかどうかのフラグを変更する。デフォルトですtrue。(トリムする)'''
        self.trim_ply = b

    def peek_line(self)->str|None:
        '''1行先読み用'''
        # 前回読み込んだやつがあるならそれを返す。
        if self.file is None:
            return None
        if self.peeked_line:
            return self.peeked_line
        self.peeked_line = self.file.readline()
        return self.peeked_line

    def get_line(self):
        '''1行読み込み'''
        self.peeked_line = None
        return self.peek_line()

class StandardBookWriter:
    """やねうら王標準定跡フォーマットの書き込みclass"""
    def __init__(self, filename:str):
        self.filename = filename
        self.file : io.TextIOWrapper | None = None

    def open(self, filename:str):
        self.file = open(filename, mode='w', encoding='utf-8')
        self.writeline(YANEURAOU_BOOK_HEADER_V1)

    def __enter__(self):
        self.open(self.filename)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb): # type:ignore
        if self.file:
            self.file.close()

    def writeline(self, line:str):
        """ 1行書き出す """
        if self.file:
            self.file.write(line + '\n')

    def write(self, sfen:str, node:BookNode):
        """ 定跡局面を1つ書き出す """
        self.writeline(f"sfen {sfen}")
        for move, eval , *etc in node:
            self.writeline(f"{move} None {eval} {etc[0] if etc else 0}")
        self.flush()

    def flush(self):
        """ flushする。"""
        if self.file:
            self.file.flush()

