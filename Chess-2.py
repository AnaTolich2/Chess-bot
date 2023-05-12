import chess
import chess.engine
import chess.svg
import os, sys
import random


from PIL import Image, ImageDraw, ImageFont

class Game:
    def __init__(self):
        self.desk = None
        self.newdesk()
        
    def showBoard(self, desk):
        image = Image.new('RGB', (1600, 1600), (230, 230, 230))
        image.paste(Image.open('board.png'))
        coll = ''
        for i in range(8):
            for j in range(8):
                if (i+j) % 2 ==0:
                    coll = 'w'
                else:
                    coll = 'r'
                image.paste(Image.open(str(desk[i][j]) +coll+ '.png'), (125+int(j) * 170, int(i) * 170 +125)) 
        return image
    
    def end_of_game(self,board,end,reason):
        if board.is_stalemate():
            reason = "Game drawn by stalemate."
            end = True
            return end, reason
        if board.is_insufficient_material():
            reason = "Game drawn by insufficient material."
            end = True
            return end, reason
        if board.can_claim_fifty_moves():
            reason = "Game drawn by 50-move rule."
            return end, reason
        if board.can_claim_threefold_repetition():
            reason = "Game drawn by threefold repetition."
            return end, reason
        if board.is_checkmate():
            player_col = "White"
            col = "White"
            if board.turn: col = "Black"
            winner = "Компьютер"
            if col == player_col: winner = "Игрок"
            reason = col, "(" + winner +         ") wins by checkmate."
            return end, reason
    
    
    def make_move(self,move_g, board, desk, engine):
        s='abcdefgh'
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
        if desk[move_to_x][move_to_y]!= '0' :
            move = move_g[0]+'x'+move_g [-2:]
        desk[move_to_x][move_to_y] = desk[move_fr_x][move_fr_y]
        desk[move_fr_x][move_fr_y]=0
        push = board.push_san(move)
        for i in range(8):
            for j in range(8):
                if (i+j) % 2 ==0:
                    coll = 'w'
                else:
                    coll = 'r' 
        col = "Black"
        with engine.analysis(board, chess.engine.Limit(time=(1.5))) as analysis:
            for info in analysis:
                pass
        move = analysis.info['pv'][0]
        move_s=str(move)
        move_s= move_s[:2]+'-'+move_s[2:]
        if move_s[0] in s:
            move_fr = 'p'+move_s[0:2]
            move_to = 'p'+move_s[3:5]
        else:
            move_fr = move_s[0:3]
            move_to = move_s[4:7]
        move_fr_y= (ord(move_fr[1])-97)
        move_fr_x= 7-(int(move_fr[2])-1)
        move_to_y= (ord(move_to[1])-97)
        move_to_x= 7-(int(move_to[2])-1)   
        desk[move_to_x][move_to_y] = desk[move_fr_x][move_fr_y]
        desk[move_fr_x][move_fr_y]='0'  
        for i in range(8):
            for j in range(8):
                if (i+j) % 2 ==0:
                    coll = 'w'
                else:
                    coll = 'r' 
        move_san = board.san(move)
        board.push(move)                
        
        return self.desk, self.board
    
    def is_valid_move(self, move_g, board, desk):
        legal_moves=  ''
        for i, legal_move in enumerate(board.legal_moves):
                legal_moves += str(board.san(legal_move))
        l = ''
        s = 'abcdefgh'
        s='abcdefgh'
        if move_g[0] in s:
            move_fr = move_g[0:2]
        else:
            move_fr = move_g[0:3]

        y= (ord(move_fr[1])-97)
        x= 7-(int(move_fr[2])-1)     
        if move_g[0] in s:
            l = move_g[-2:]
        else:
            l = move_g[-3:]
        if l in legal_moves and desk[x][y]!='0':
            return True
        else:
            return False
        
    def newdesk(self):
        Bcolor = 'B'
        Pcolor = 'W'
        u  = 97
        image = Image.open('board.png')
        ew = '0'
        eb = '0'
        l = '01'
        s = 'abcdefgh'
        pr = 'rook'+Pcolor+'_'
        pk = 'knight'+Pcolor+'_'
        pb = 'bishop'+Pcolor+'_'
        pq = 'queen'+Pcolor+'_'
        pkn = 'king'+Pcolor+'_'
        br = 'rook'+Bcolor+'_'
        bk = 'knight'+Bcolor+'_'
        bb = 'bishop'+Bcolor+'_'
        bq = 'queen'+Bcolor+'_'
        bkn = 'king'+Bcolor+'_'
        pp = 'pawn'+Pcolor+'_'
        bp = 'pawn'+Bcolor+'_'
        desk = [[br, bk, bb, bq, bkn, bb, bk, br], [bp, bp, bp, bp, bp, bp, bp, bp],
                [eb, ew, eb, ew, eb, ew, eb, ew], [ew, eb, ew, eb, ew, eb, ew, eb],
                [eb, ew, eb, ew, eb, ew, eb, ew], [ew, eb, ew, eb, ew, eb, ew, eb],
                [pp, pp, pp, pp, pp, pp, pp, pp],
                [pr, pk, pb, pq, pkn, pb, pk, pr]]             
        self.desk = desk
        self.end = False
        self.reason = ''
        self.board = chess.Board()
        engine_file = "stockfish_15.exe"
        self.engine = chess.engine.SimpleEngine.popen_uci(engine_file)
        self.engine.configure({"Skill Level": 2})

def main():
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
    pr = 'rook'+Pcolor+'_'
    pk = 'knight'+Pcolor+'_'
    pb = 'bishop'+Pcolor+'_'
    pq = 'queen'+Pcolor+'_'
    pkn = 'king'+Pcolor+'_'
    br = 'rook'+Bcolor+'_'
    bk = 'knight'+Bcolor+'_'
    bb = 'bishop'+Bcolor+'_'
    bq = 'queen'+Bcolor+'_'
    bkn = 'king'+Bcolor+'_'
    pp = 'pawn'+Pcolor+'_'
    bp = 'pawn'+Bcolor+'_'
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
    keep_running = True
    #
    while keep_running:
        
        #
        if (board.turn and player_col == 'White') or (not board.turn and player_col == 'Black'):
            move_g = input("������� ���: ")
            legal_moves = ""
            
            move = ''
            for i, legal_move in enumerate(board.legal_moves):
                    legal_moves += str(board.san(legal_move)) + " "
            #print(legal_moves, l)
            if move_g[0] in s:
                l = move_g[-2:]
            else:
                l = move_g[-3:]
                print("���������� ����:", legal_moves)
                continue
            try:
                push = board.push_san(move)
                if show_only_last: os.system("cls")
                make_move(move_fr_x,move_fr_y,move_to_x,move_to_y,desk)
                print(player_col, "(Player) moves", move)
            except ValueError:
                print(move, "is not a legal move.")
        else:
            col = "White"
            if not board.turn: col = "Black"
            
            
    #
    
    print("Thanks for playing!")

if __name__ == '__main__':
    main()



        