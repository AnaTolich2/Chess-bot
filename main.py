import chess
import chess.engine
import chess.svg
import os, sys
import random


from PyQt5.QtSvg import QSvgWidget
from PyQt5.QtWidgets import QApplication, QWidget
from PIL import Image, ImageDraw, ImageFont

class MainWindow(QWidget):
    def __init__(self, board):
        super().__init__()

        self.setGeometry(100, 100, 600, 600)

        self.widgetSvg = QSvgWidget(parent = self)
        self.widgetSvg.setGeometry(10, 10, 580, 580)

        self.chessboard = board

        self.chessboardSvg = chess.svg.board(self.chessboard, orientation=board.turn).encode("UTF-8")
        self.widgetSvg.load(self.chessboardSvg)

def showBoard(desk):
    coll = ''
    for i in range(8):
        for j in range(8):
            if (i+j) % 2 ==0:
                coll = 'w'
            else:
                coll = 'r'
            image.paste(Image.open(desk[i][j] +coll+ '.png'), (125+j * 170, i * 170 +125))
    image.save('2.png', 'PNG') 


def make_move(move_fr_x,move_fr_y,move_to_x,move_to_y,desk):
    if desk[move_to_x][move_to_y]=='1' or desk[move_to_x][move_to_y]=='0':
        desk[move_to_x][move_to_y] = desk[move_fr_x][move_fr_y]
        if move_fr_x %2 == move_fr_y%2 :
            desk[move_fr_x][move_fr_y]=0
        else:
            desk[move_fr_x][move_fr_y]=1
    for i in range(8):
        for j in range(8):
            if (i+j) % 2 ==0:
                coll = 'w'
            else:
                coll = 'r'    
    return desk

engine_file = "stockfish_15.exe"
if not os.path.exists(engine_file):
    print("Engine file not found:", engine_file)
    sys.exit()

cnt = 0
#
Bcolor = 'B'
Pcolor = 'W'
u  = 97
image = Image.new('RGB', (1600, 1600), (230, 230, 230))
ew = '0'
eb = '0'
l = '01'
s = 'abcdefgh'
pr = 'Rook'+Pcolor+'_'
pk = 'Night'+Pcolor+'_'
pb = 'Bishop'+Pcolor+'_'
pq = 'Queen'+Pcolor+'_'
pkn = 'King'+Pcolor+'_'
br = 'Rook'+Bcolor+'_'
bk = 'Night'+Bcolor+'_'
bb = 'Bishop'+Bcolor+'_'
bq = 'Queen'+Bcolor+'_'
bkn = 'King'+Bcolor+'_'
pp = 'Pawn'+Pcolor+'_'
bp = 'Pawn'+Bcolor+'_'
image.paste(Image.open('board.png'))
desk = [[br, bk, bb, bq, bkn, bb, bk, br], [bp, bp, bp, bp, bp, bp, bp, bp],
        [eb, ew, eb, ew, eb, ew, eb, ew], [ew, eb, ew, eb, ew, eb, ew, eb],
        [eb, ew, eb, ew, eb, ew, eb, ew], [ew, eb, ew, eb, ew, eb, ew, eb],
        [pp, pp, pp, pp, pp, pp, pp, pp],
        [pr, pk, pb, pq, pkn, pb, pk, pr]]


print("Welcome to Blindfold Chess")
input_str = ' '
while input_str[0].lower() != 'w' and input_str[0].lower() != 'b' and input_str[0].lower() != 'r':
    input_str = input("Play as (w)hite, (b)lack, (r)andom: ")
in_c = input_str[0]
player_col = 'White'
if in_c == 'b':
    player_col = 'Black'
if in_c == 'r':
    rand_num = random.randint(0,1)
    if rand_num == 1: player_col = 'Black'
print("You are playing as " + player_col + ".")
#
#
engine = chess.engine.SimpleEngine.popen_uci(engine_file)
diff = -1
while diff not in range(1,11):
    in_str = input("Enter difficulty level (1 to 10): ")
    if not in_str.isnumeric(): continue
    diff = int(in_str)
engine.configure({"Skill Level": diff})
print("Level", str(diff), "difficulty chosen.")
show_only_last = False
in_str = '-'
while in_str[0].lower() != 'y' and in_str[0].lower() != 'n':
    in_str = input("Show only last move (y/n): ")
if in_str[0].lower() == 'y':
    show_only_last = True
print("Type 'board' at any time to see the current board.")
print("Type 'moves' at any time to see the legal moves.")
print("---")
print("Game begins.")
board = chess.Board()
keep_running = True
#
while keep_running:
    if board.is_stalemate():
        print("Game drawn by stalemate.")
        break
    if board.is_insufficient_material():
        print("Game drawn by insufficient material.")
        break
    if board.can_claim_fifty_moves():
        print("Game drawn by 50-move rule.")
        break
    if board.can_claim_threefold_repetition():
        print("Game drawn by threefold repetition.")
        break
    if board.is_checkmate():
        col = "White"
        if board.turn: col = "Black"
        winner = "Компьютер"
        if col == player_col: winner = "Игрок"
        print(col, "(" + winner + ") wins by checkmate.")
        break
    if (board.turn and player_col == 'White') or (not board.turn and player_col == 'Black'):
        if cnt % 2 ==0:
            move_g = input("Введите ход: ")
            if move_g[0] in s:
                move_fr = 'p'+move_g[0:2]
                move_to = 'p'+move_g[3:5]
                move  = move_g[3:5]
            else:
                move_fr = move_g[0:3]
                move_to = move_g[4:7]
                move  = move_g[4:7]
            move_fr_y= (ord(move_fr[1])-97)
            move_fr_x= 7-(int(move_fr[2])-1)
            move_to_y= (ord(move_to[1])-97)
            move_to_x= 7-(int(move_to[2])-1)   
            if desk[move_to_x][move_to_y]=='1' or desk[move_to_x][move_to_y]=='0':
                desk[move_to_x][move_to_y] = desk[move_fr_x][move_fr_y]
                if move_fr_x %2 == move_fr_y%2 :
                    desk[move_fr_x][move_fr_y]=0
                else:
                    desk[move_fr_x][move_fr_y]=1            
        else :
            move = input("Введите ход:")
        cnt+=1
        if move.lower() == "board":
            showBoard(desk)
            continue
        elif move.lower() == "moves":
            legal_moves = ""
            for i, legal_move in enumerate(board.legal_moves):
                legal_moves += str(board.san(legal_move)) + " "
            print("Допустимые ходы:", legal_moves)
            continue
        try:
            push = board.push_san(move)
            if show_only_last: os.system("cls")
            print(player_col, "(Player) moves", move)
        except ValueError:
            print(move, "is not a legal move.")
    else:
        col = "White"
        if not board.turn: col = "Black"
        with engine.analysis(board, chess.engine.Limit(time=(1.5))) as analysis:
            for info in analysis:
                pass
        move = analysis.info['pv'][0]
        move_san = board.san(move)
        board.push(move)
        if show_only_last: os.system("cls")
        print(col, "(Engine) moves", str(move_san))
#

print("Thanks for playing!")





        


        

