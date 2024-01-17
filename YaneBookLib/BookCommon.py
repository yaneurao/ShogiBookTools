import cshogi

# USIプロトコルのSFEN文字列。ただし先頭の"sfen "と末尾の手数は記されていないものとする。
Sfen = str

# 指し手文字列(USIプロトコルの形式)
Move  = str
# やねうら王形式の定跡DBファイルに書き出す時の指し手に対応する評価値
Eval  = int
# やねうら王形式の定跡DBファイルに書き出す時の指し手に対応する探索深さ
Depth = int

# やねうら王形式の定跡DBの1つの局面情報を表現する型
BookNode = list[tuple[Move,Eval] | tuple[Move,Eval,Depth]]

# やねうら王形式の定跡ファイルを表現する型(メモリ上もこの型で持つ)
Book     = dict[Sfen,BookNode]

YANEURAOU_BOOK_HEADER_V1 = "#YANEURAOU-DB2016 1.00"

# ============================================================
#             SFEN Helper Function
# ============================================================

def trim_sfen(sfen:str)->Sfen:
    '''
    "sfen"で開始される形式のSFEN文字列(ただし先頭の"sfen"は含まなくても良い)に対して、
    末尾の手数を取り除いて返す。 また先頭に"sfen"の文字があればそれも取り除く。
    '''
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

def UsiKifToSfens(kif:str)->list[str]:
    """
    USIプロトコルで出てくるposition文字列に基づく棋譜読み込みclass
    
    startpos
    startpos moves ...
    sfen ...
    sfen ... moves ...
    ... (sfen文字列)
    ... (sfen文字列) moves ... 
    の6つのうちのいずれかの形式で書かれた棋譜に対して、sfen文字列を取得できるiteratorを返す。
    """
    kif_moves : list[str] = kif.split('moves')
    sfens : list[str] = []
    if len(kif_moves) == 0:
        return sfens

    head = kif_moves[0].strip()

    board = Board()
    if head == 'startpos':
        board.set_position(head)
    else:
        if not head.startswith('sfen'):
            head = 'sfen ' + head
        board.set_position(head)
    sfens += board.sfen(),

    if len(kif_moves) == 1:
        return sfens

    # 先にexpandしてしまう
    for move in kif_moves[1].split():
        board.push_usi(move)
        sfens += board.sfen(),

    return sfens

# ============================================================
#                   cshogi wrapper
# ============================================================

# 先手番を表す定数
BLACK                     = cshogi.BLACK

# 後手番を表す定数
WHITE                     = cshogi.WHITE

class Board:
    '''
    cshogiがCythonで書かれていてPylacnceが機能しないのでwrapperを書く。
    cshogi.Boardとだいたい等価。
    '''
    def __init__(self,position_str:str=''):
        self.board = cshogi.Board(position_str)
    
    def to_svg(self)->str:
        '''局面をSVG化した文字列を返す。'''
        return self.board.to_svg()
    
    def set_position(self,position_str:str):
        '''局面を設定する。'''
        try:
            self.board.set_position(position_str)
        except:
            raise ValueError(f'Illegal Position : {position_str}')

    @property
    def turn(self)->int:
        return self.board.turn

    def push_usi(self,usi_move:str)->int:
        '''
        指し手で局面を進める。
        move = USIプロトコルの指し手文字列

        ※　指し手で進める前に合法手チェックを行う。
        　合法手でなければValueError例外を投げる。
        '''
        move = self.move_from_usi(usi_move)
        if not self.is_legal(move):
            raise ValueError('Illegal Move')
        return self.board.push(move)

    def pop(self):
        '''局面を1つ戻す。'''
        self.board.pop()

    def is_draw(self)->int:
        '''千日手になっているかの判定。'''
        return self.board.is_draw()

    @property
    def legal_moves(self)->list[int]:
        '''
        合法手をすべて返す。型は32bit整数なので注意。
        これはmove_to_usi()でUSIの指し手文字列に変換できる。
        '''
        return self.board.legal_moves
    
    def sfen(self)->str:
        '''
        sfen文字列を返す。末尾に手数がついているので注意。
        '''
        return self.board.sfen()

    def game_ply(self)->int:
        return self.board.move_number
    
    def move_from_usi(self,usi_move:str)->int:
        '''USIの指し手文字列をApery形式のMoveに変換する(moveIsLegalなどで必要となる)'''
        return self.board.move_from_usi(usi_move)
    
    def is_legal(self, move:int)->bool:
        '''Apery形式のMoveがこの局面において合法手であるかを判定する。'''
        return self.board.is_legal(move)


def move_to_usi(m:int)->str:
    '''legal_moves()で返ってきた32bit整数をUSIプロトコルの指し手文字列に変換する。'''
    return cshogi.move_to_usi(m)

