import chess
import chess.engine
import chess.svg
import os, sys
import random


from PIL import Image, ImageDraw, ImageFont

class Game:
    def set_diff(self, d):
        u = '12345678910'
        if d in u:
            if 1<=int(d) and int(d)<=10:
                self.diff= d
                return True
            else:
                self.diff = 1
                return False
        else:
            self.diff = 1
            return False        
    #def mask(move):
        #j = 'abcdefgh'
        #o = '12345678'
        #if len(move_g)>=5:
            #if len(move_g) ==5:
                #if move[0] in s and move[1] in o and move[3] in s and move[4] in o:
                    #k= True
                #else:
                    #k= False
            #elif len(move_g) == 7:
                #if move[1] in s and move[2] in o and move[-2] in s and move[-1] in o:
                    #k= True
                #else:
                    #k= False
                
            #else:
                #k =  False
        #else:
            #k = False
    def newdesk(self):
        Bcolor = 'B'
        Pcolor = 'W'
        u  = 97
        image = Image.open('board.png')
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
        desk = [[br, bk, bb, bq, bkn, bb, bk, br], [bp, bp, bp, bp, bp, bp, bp, bp],
                [eb, ew, eb, ew, eb, ew, eb, ew], [ew, eb, ew, eb, ew, eb, ew, eb],
                [eb, ew, eb, ew, eb, ew, eb, ew], [ew, eb, ew, eb, ew, eb, ew, eb],
                [pp, pp, pp, pp, pp, pp, pp, pp],
                [pr, pk, pb, pq, pkn, pb, pk, pr]]  
        self.commands= ['Пока!','Начать игру','Выход','Сыграть сначала','/start']
        self.ch = ''
        self.diff = '1'
        self.desk = desk
        self.end = False
        self.reason = ''
        self.board = chess.Board()
        engine_file = "stockfish_15.exe"
        self.engine = chess.engine.SimpleEngine.popen_uci(engine_file)
        self.engine.configure({"Skill Level": int(self.diff)})
    
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
            return self.end, self.reason
        if board.is_insufficient_material():
            reason = "Game drawn by insufficient material."
            end = True
            return self.end, self.reason
        if board.can_claim_fifty_moves():
            reason = "Game drawn by 50-move rule."
            return self.end, self.reason
        if board.can_claim_threefold_repetition():
            reason = "Game drawn by threefold repetition."
            return self.end, self.reason
        if board.is_checkmate():
            player_col = "White"
            col = "White"
            if board.turn: col = "Black"
            winner = "Компьютер"
            if col == player_col: winner = "Игрок"
            reason = col, "(" + winner +         ") wins by checkmate."
            return self.end, self.reason
    
    
    def make_move(self,move_g, board, desk, engine):
        s='abcdefgh'
        if (move_g =='O-O' or move_g=='O-O-O'):
            if move_g =='O-O':
                desk[7][6] = desk[7][4]
                desk[7][4]= '0'
                desk[7][5] = desk[7][7]
                desk[7][7] = '0'
                push = board.push_san(move_g)
            elif move_g =='O-O-O':
                desk[7][2] = desk[7][4]
                desk[7][4] = '0'
                desk[7][3] = desk[7][0]
                desk[7][0] = '0'
                push = board.push_san(move_g)
        else:
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
            desk[move_fr_x][move_fr_y]='0'
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
        
        move_san = board.san(move)
        board.push(move)                
        return self.desk, self.board
    
    def is_valid_move(self, move_g, board, desk, ch, commands):
        j = 'abcdefgh'
        o = '12345678'
        if len(move_g)>=5:
            if len(move_g) ==5:
                if move_g[0] in j and move_g[1] in o and move_g[3] in j and move_g[4] in o:
                    k= True
                else:
                    k= False
            elif len(move_g) == 7:
                if move_g[1] in j and move_g[2] in o and move_g[-2] in j and move_g[-1] in o:
                    k= True
                else:
                    k= False
                
            else:
                k =  False
        else:
            k = False
        if k:
            if len(move_g)>=5 or move_g =='O-O' or move_g=='O-O-O':
                legal_moves=  ''
                for i, legal_move in enumerate(board.legal_moves):
                        legal_moves += str(board.san(legal_move))+' '
                if (move_g =='O-O' or move_g=='O-O-O') and move_g in legal_moves:
                    return True
                else:
                    l = ''
                    s='abcdefgh'
                    if move_g[0] in s:
                        move_fr ='P'+move_g[0:2]
                        move_to = 'P'+move_g[3:5]
                    else:
                        move_fr = move_g[0:3]
                        move_to = move_g[4:7]
                    move_to_y= (ord(move_to[1])-97)
                    move_to_x= 7-(int(move_to[2])-1)          
                    leg_m = legal_moves.split()
                    y= (ord(move_fr[1])-97)
                    x= 7-(int(move_fr[2])-1)        
                    if desk[x][y]!='0':
                        if (desk[move_to_x][move_to_y]!='0' and desk[x][y][-2]!=desk[move_to_x][move_to_y][-2]) or desk[move_to_x][move_to_y]=='0':
                            if desk[x][y][-2] == 'W':
                                if move_g[0] in s:
                                    l = move_g[-2:]
                                else:
                                    l = move_g[-3:]
                                if desk[move_to_x][move_to_y]!= '0' :
                                    l = move_g[0]+'x'+move_g [-2:]          
                                if l in legal_moves:              
                                    if  move_fr[0]==desk[x][y][0]:
                                        return True                 
                                    else:
                                        self.ch = 'Доступные ходы: '+legal_moves
                                        return False            
                                else:
                                    self.ch = 'Доступные ходы: '+legal_moves
                                    return False
                            else:
                                self.ch = 'Доступные ходы: '+legal_moves
                                return False  
                        else:
                            self.ch = 'Доступные ходы: '+legal_moves
                            return False                
                    else:
                        self.ch = 'Доступные ходы: '+legal_moves
                        return False              
            else:
                self.ch = 'Некорректный формат'
                return False  
        else:
            self.ch = 'Некорректный формат'
            return False 
        
    def main():
        print('')
            

if __name__ == '__main__':
    main()



        


        

