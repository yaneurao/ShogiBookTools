import cshogi

board = cshogi.Board()
OK = board.set_position("sfen ln1gk2nl/1r1s2g2/p1ppppsp1/6p1p/1p5P1/2P3P1P/PPSPPP3/2G3SR1/LN2KG1NL w Bb 0")
print(OK)

# incorrect SFEN string : sfen 
# True
