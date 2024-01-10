import io
from YaneBookLib.BookCommon import *

def trim_sfen(sfen:str)->Sfen:
    ''' "sfen"で開始される形式のsfen文字列(ただし先頭の"sfen"は含まず)に対して、末尾の手数を取り除いて返す。 '''
    s = sfen.split()

    # 先頭にsfenが含まれていたら除去
    if s[0] == 'sfen':
        del s[0]

    try:
        # 末尾が数字なのかテストする
        int(s[-1])
        del s[-1]
    except:
        # 数字が付与されてないんじゃ？
        pass

    return " ".join(s)

class BookReader:
    def __init__(self, filename:str):
        self.filename = filename
        self.file : io.TextIOWrapper | None = None

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
                sfen = trim_sfen(line)

                # 指し手の読み込み..
                book_node:BookNode = []
                while True:
                    line = self.peek_line()
                    # 終端か次のsfenに達した。
                    if not line or line.startswith('sfen'):
                        return (sfen, book_node)
                    self.get_line() # feed
                    move, _, eval, *_ = line.split()
                    book_node += (move, int(eval)),


    def close(self):
        if self.file:
            self.file.close()

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

class BookWriter:
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
        for move, eval in node:
            self.writeline(f"{move} None {eval} 0")
