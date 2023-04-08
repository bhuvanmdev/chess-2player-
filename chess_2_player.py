from os import system ## play it in terminal for a smooth game
class Chess:
    def __init__(self):
        self.board = [['br1','bh1','bb1','bq0','bk0','bb2','bh2','br2'],
                      ['bp1','bp2','bp3','bp4','bp5','bp6','bp7','bp8'],
                      [' * ',' * ',' * ',' * ',' * ',' * ',' * ',' * '],
                      [' * ',' * ',' * ',' * ',' * ',' * ',' * ',' * '],
                      [' * ',' * ',' * ',' * ',' * ',' * ',' * ',' * '],
                      [' * ',' * ',' * ',' * ',' * ',' * ',' * ',' * '],
                      ['wp1','wp2','wp3','wp4','wp5','wp6','wp7','wp8'],
                      ['wr1','wh1','wb1','wq0','wk0','wb2','wh2','wr2']]
        self.bpos = {'br1':[0,0],'bh1':[0,1],'bb1':[0,2],'bq0':[0,3],'bk0':[0,4],'bb2':[0,5],'bh2':[0,6],'br2':[0,7],
                     'bp1':[1,0],'bp2':[1,1],'bp3':[1,2],'bp4':[1,3],'bp5':[1,4],'bp6':[1,5],'bp7':[1,6],'bp8':[1,7]}
        self.wpos = {'wr1':[7,0],'wh1':[7,1],'wb1':[7,2],'wq0':[7,3],'wk0':[7,4],'wb2':[7,5],'wh2':[7,6],'wr2':[7,7],
                     'wp1':[6,0],'wp2':[6,1],'wp3':[6,2],'wp4':[6,3],'wp5':[6,4],'wp6':[6,5],'wp7':[6,6],'wp8':[6,7]}
        self.wval = self.wpos.values()
        self.bval = self.bpos.values()
        self.wdoublejumpers = {}
        self.bdoublejumpers = {}
        self.wcheck = self.bcheck = False
    
    def print_board(self):
        print('   ',end='')
        [print(f' {x}    ',end='') for x in range(8)]
        print()
        for num,x in enumerate(self.board):
            print(num,' ',end='')
            print(' | '.join(x),'-'*50,sep='\n')
    
    
    def mover(self,pawn,to):
        if pawn[0] in ('b','w'):
            pos,op_pos,val,op_val,word,op_word,num = (self.bpos,self.wpos,self.bval,self.wval,'b','w',1) if pawn[0] == 'b' else (self.wpos,self.bpos,self.wval,self.bval,'w','b',6)
            opp_pawn = (' * ',-1) 
            
            # checks for opp pawn! if there remove it from db..
            if to in op_val:
                [opp_pawn:=(x,op_pos[x]) for x,y in op_pos.items() if y == to]
                op_pos.pop(opp_pawn[0]) 
            
            ## checks for same pawn! if there illegal move(false)
            elif to in val: 
                return False
            
            ## does all the shifting stuff db and board.
            fr = pos[pawn]
            pos[pawn] = to
            self.board[to[0]][to[1]] = pawn    
            self.board[fr[0]][fr[1]] = ' * '
            if pawn[0]=='b':
                self.bcheck = False 
            else:
                self.wcheck = False
            ## if same color was able to move --> then its outa check
            
            ## checks after the weather king of same still in check --> if yes backtracks previous move..
            if self.checker(word):
                ## reverses the P-->p if its in check and not moved 
                if pawn[1] == 'P' and fr[0] == num:
                    pos[(pawn := pawn[0] + 'p' + pawn[2])] = pos.pop(pawn)
                    
                self.board[fr[0]][fr[1]] = pawn
                self.board[to[0]][to[1]] = opp_pawn[0]
                pos[pawn] = fr
                if opp_pawn[1] != -1:
                    op_pos[opp_pawn[0]] = to
                if pawn[0]=='b':
                    self.bcheck = True 
                else:
                    self.wcheck = True
                return False
           
            #  if previous cond is wrong --> checks for opp color check..
            else:
                if self.checker(op_word):
                    print(f'\n\t\tDUDE {op_word} ON CHECK\n') # word
                    if pawn[0]=='b':
                        self.wcheck = True 
                    else:
                        self.bcheck = True
                    
        self.wval = self.wpos.values()
        self.bval = self.bpos.values()
        return True
    
    
    def pawn(self,nam,to):##
        sign,getter,op_get,remember,opp_rem = (1,self.bpos,self.wpos,self.bdoublejumpers,self.wdoublejumpers) if nam[0] == 'b' else (-1,self.wpos,self.bpos,self.wdoublejumpers,self.bdoublejumpers)
        tx,ty = to
        fx,fy = getter.get(nam,[-1,-1])
        if fx==fy==-1 or tx==ty==-1: return False
        if nam[1] == 'p':
            # to move 2 steps forward
            if ty == fy and (tx == fx + 2*sign and self.board[tx-1*sign][ty] ==  self.board[tx][ty] == ' * '):
                getter[(nam:=nam[0]+'P'+nam[2])] = getter.pop(nam)
                if nam[0] == 'b':
                    self.bval = getter.values()
                else:
                    self.wval = getter.values()
                
                # remembers the pawn/attack_box for en_passant
                if self.mover(nam,to):
                    remember[nam] = [tx - sign,ty] 
                    return True
                        
        pawn_present = to in op_get.values()
        cross_cond = (ty  in (fy-1,fy+1) and tx == fx + 1*sign )
        single_cond = (ty==fy and tx == fx + 1*sign and self.board[tx][ty] == ' * ')
        en_cond = [tx,ty] in opp_rem.values()
        
        # move single step
        if en_cond or (cross_cond and pawn_present) or  single_cond :
            # beginning single step
            if nam[1] == 'p':
                getter[(nam:=nam[0]+'P'+nam[2])] = getter.pop(nam)
                if nam[0] == 'b':
                    self.bval = getter.values()
                else:
                    self.wval = getter.values()
            
            if self.mover(nam,to):
                # if the remembered pawn moves out
                if single_cond and nam in remember:
                    remember.pop(nam)
                
                # if en_passant comes to action
                elif en_cond and cross_cond:
                    to_rem = self.board[tx-sign][ty]
                    self.board[tx-sign][ty] = ' * '
                    op_get.pop(to_rem)
                    self.bval = self.bpos.values()
                    self.wval = self.wpos.values()
                return True
        return False
    
    
    def rook(self,nam,to):
        fx,fy = self.bpos.get(nam,[-1,-1]) if nam[0] == 'b' else self.wpos.get(nam,[-1,-1])
        if fx==fy==-1: return False
        tx,ty = to
        if fx == tx:
            sign = 1 if ty > fy else -1
            for y in range(fy+sign,ty,sign):
                if self.board[fx][y] != ' * ':
                    break
            else:
                return self.mover(nam,to)
        elif fy == ty:
            sign = 1 if tx > fx else -1
            for x in range(fx+sign,tx,sign):
                if self.board[x][fy] != ' * ':
                    break
            else:
                return self.mover(nam,to)
        return False
    
    
    def bishop(self,nam,to):
        fx,fy = self.bpos.get(nam,[-1,-1]) if nam[0] == 'b' else self.wpos.get(nam,[-1,-1])
        if fx==fy==-1: return False
        tx,ty = to
        if abs(tx-fx) != abs(ty-fy): return False
        signx = 1 if (tx > fx and ty > fy) or (tx > fx and ty < fy) else -1
        signy = 1 if (tx > fx and ty > fy) or (tx < fx and ty > fy) else -1
        while fx != tx-signx and fy != ty-signy:
            fx += signx
            fy += signy
            if self.board[fx][fy] != ' * ':
                return False
        return self.mover(nam,to)
    
    
    def horse(self,nam,to):
        fx,fy = self.bpos.get(nam,[-1,-1]) if nam[0] == 'b' else self.wpos.get(nam,[-1,-1])
        if fx==fy==-1: return False
        tx,ty = to
        k = filter(lambda x: 0<=x[0]<=7 and 0<=x[1]<=7,[[fx+2,fy-1],[fx+2,fy+1],[fx-2,fy-1],[fx-2,fy+1],
                                                        [fx-1,fy+2],[fx+1,fy+2],[fx-1,fy-2],[fx+1,fy-2]])
        return self.mover(nam,to) if to in k else False
        
    
    def queen(self,nam,to):
        return self.bishop(nam,to) or self.rook(nam,to)
    
    
    def king(self,nam,to):
        fx,fy = self.bpos.get(nam,[-1,-1]) if nam[0] == 'b' else self.wpos.get(nam,[-1,-1])
        tx,ty = to
        k = filter(lambda x: 0<=x[0]<=7 and 0<=x[1]<=7,[[fx+1, fy ],[fx-1, fy ],[ fx ,fy-1],[ fx ,fy+1],
                                                        [fx-1,fy-1],[fx+1,fy+1],[fx-1,fy+1],[fx+1,fy-1]])
        return self.mover(nam,to) if to in k else False
    
    
    #main funtion caller
    def sorter(self,nam,to):
        le = len(nam)
        if le != 3: return False
        
        ## castling caller
        if nam[2] == 'c':
            return self.castling(nam[:2])
        
        ## pawn swapper caller
        col,sign,tosign = (self.bpos,1,-1) if nam[0]=='b' else (self.wpos,0,1)
        pawn = col.get(nam,-1)
        if nam[1] == 'P' and pawn != -1 and pawn[0] == 1 + 5*sign == to[0]+tosign:
            return self.pawn_swapper(nam,to)
        
        ##normal caller
        store = {'r':self.rook,'b':self.bishop,'p':self.pawn,'P':self.pawn, ##
                 'q':self.queen,'k':self.king,'h':self.horse}
        j = store.get(nam[1],-1)
        return j(nam,to) if j != -1 else False
    
    def checker(self,colour,fr = -1):
        cnot = 'b' if colour=='w' else 'w'
        fx,fy = self.bpos['bk0'] if colour == 'b' else self.wpos['wk0']
        
        #custom block check checker
        fx,fy = fr if fr != -1 else (fx,fy)
        
        
        # pawn checker
        sign = -1 if colour == 'w' else 1
        for x,y in ((fx+1*sign,fy-1),(fx+1*sign,fy+1)):
            if 0<=x<=7 and 0<=y<=7:
                if f'{cnot}p' in self.board[x][y] or f'{cnot}P' in self.board[x][y]:
                    return True
        
        #rook/queen checker (row/coloumn)
        for x,y in ((1,0),(-1,0),(0,1),(0,-1)):
            ffx,ffy = fx+x,fy+y
            while 0<=ffx<=7 and 0<=ffy<=7:
                if self.board[ffx][ffy] != ' * ':
                    if self.board[ffx][ffy] in (f'{cnot}r1',f'{cnot}r2',f'{cnot}q0'):
                        return True
                    break
                ffx += x
                ffy += y
        
        #horse checker
        k = filter(lambda x: 0<=x[0]<=7 and 0<=x[1]<=7,[[fx+2,fy-1],[fx+2,fy+1],[fx-2,fy-1],[fx-2,fy+1],
                                                    [fx-1,fy+2],[fx+1,fy+2],[fx-1,fy-2],[fx+1,fy-2]])
        for x,y in k:
            if self.board[x][y] in (f'{cnot}h1',f'{cnot}h2'):
                return True
        
        # bishop/queen checker (diagonals)
        for x,y in ((-1,-1),(-1,1),(1,-1),(1,1)):
            ffx,ffy = fx+x,fy+y
            while 0<=ffx<=7 and 0<=ffy<=7:
                if self.board[ffx][ffy] != ' * ':
                    if self.board[ffx][ffy] in (f'{cnot}b1',f'{cnot}b2',f'{cnot}q0'):
                        return True
                    break
                ffx += x
                ffy += y
        return False
        
        
    def castling(self,color):
        of_pos,check = (self.bpos,self.bcheck) if color[0] == 'b' else (self.wpos,self.wcheck) 
        if color[0] == 'w':
            if color[1] == '1':
                rpos = [7,0]
            elif color[1] == '2':
                rpos = [7,7]
            kpos = [7,4]
        elif color[0] == 'b':
            if color[1] == '1':
                rpos = [0,0]
            elif color[1] == '2':
                rpos = [0,7]
            kpos = [0,4]
        cond1 = of_pos[f'{color[0]}r{color[1]}']==rpos and of_pos[f'{color[0]}k0'] == kpos #not moved
        
        if color[1] in ('1','2'):
            sign = 0 if color[1] == '1' else 1
            cond2 = (self.board[kpos[0]][1] if color[1]=='1' else ' * ') == self.board[kpos[0]][3+2*sign] == self.board[kpos[0]][2+4*sign] == ' * ' #empty gap b/w them
            cond3 = not( (self.checker(color[0],fr =[kpos[0],1]) if color[1]=='1' else False) or self.checker(color[0],fr=[kpos[0],3+2*sign]) or self.checker(color[0],fr=[kpos[0],2+4*sign])) #king not in check
            if (not check) and cond1 and cond2 and cond3:
                of_pos[f'{color[0]}k0'] = [kpos[0],2+4*sign]
                of_pos[f'{color[0]}r{color[1]}'] = [kpos[0],3+2*sign]
                
                if color[0]=='b':
                    self.bval = self.bpos.values()
                else:
                    self.wval = self.wpos.values()
                
                self.board[kpos[0]][2+4*sign] = f'{color[0]}k0'
                self.board[kpos[0]][3+2*sign] = f'{color[0]}r{color[1]}'
                self.board[kpos[0]][4] = self.board[kpos[0]][7*sign] = ' * '
                return True
        
        return False


    def pawn_swapper(self,pawn,to):
        if self.pawn(pawn,to):
            pos,check,word = (self.bpos,'w','WHITE') if pawn[0] == 'b' else (self.wpos,'b','BLACK')
            fx,fy = pos[pawn]
            
            ##checks for validity of pawn input!!
            while (select:=input("(r,q,b,h): ")) not in ('r','q','b','h'):
                print()
                
            ## helps to find the suitable number required
            for x in range(10):
                if (new_pawn:=pawn[0] + select + str(x)) not in pos:
                    pos[new_pawn] = pos.pop(pawn)
                    self.board[fx][fy] = new_pawn
                    
                    ## checks for check made by the new pawn
                    if self.checker(check):
                        print(f"\t\tDUDE {word} is on check")
                    
                    ## updates bval/wval db..
                    if pawn[0] == 'b':
                        self.bval = self.bpos.values()
                    else:
                        self.wval = self.wpos.values()
                    return True
        return False

if __name__ == '__main__':
    game = Chess()
    game.print_board()
    mov = 0
    turns = ['w','b']
    while (inp:=(input('name: '))) != 'xxx':
        if len(inp) == 3 and inp[0]==turns[mov%2]:
            if inp[2] != 'c':
                pos = input('pos: ').split()
                if not ''.join(pos).isnumeric() and len(pos)!=2:
                    print('give correct positon bro: ')
                    continue
                
                pos = list(map(int,pos))
            else:
                pos = [0,0]
            system('cls')
            if game.sorter(inp,pos):
                game.print_board()
                mov += 1
            else:
                print('\t\tillegal move brothor')
                if game.wcheck:
                    print('\t\tDUDE w STILL IS ON CHECK')
                elif game.bcheck:
                    print('\t\tDUDE b STILL IS ON CHECK')
                game.print_board()
        else:
            print(f"its {turns[mov%2]} turn now")
    print(f"\t\t{turns[mov%2]} forfited\n\t\thence {turns[(mov+1)%2]} wins")
