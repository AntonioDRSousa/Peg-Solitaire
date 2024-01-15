import tkinter as tk
from tkinter import messagebox

class Peg:
    def __init__(self,win1,win2,sboard):
        self.win1 = win1
        self.win2 = win2

        self.changeFrame(self.win1,self.win2)
        
        self.sboard = sboard
        self.dim = (600,600)
        self.canvas = tk.Canvas(self.win2,width=self.dim[0],height=self.dim[1],bg="black",highlightthickness=0)
        self.canvas.pack()
        
        self.npieces = 0
        self.isSelect = False
        self.select = (-1,-1)
        self.pointer = (0,0)
        
        self.loadBoard()
        self.drawBoard()
        self.drawPointer()
        
        self.win2.master.bind("<Up>",self.keyUp)
        self.win2.master.bind("<Down>",self.keyDown)
        self.win2.master.bind("<Right>",self.keyRight)
        self.win2.master.bind("<Left>",self.keyLeft)
        self.win2.master.bind("<KeyPress>",self.key)
        
    def changeFrame(self,w1,w2):
        w1.forget()
        w2.pack(fill='both',expand=1)
        
    def keyUp(self,event):
        if self.pointer[1]>0:
            self.pointer = (self.pointer[0],self.pointer[1]-1)
            self.canvas.move(self.r1,0,-self.ssq)
            
    def keyDown(self,event):
        if self.pointer[1]<(self.height-1):
            self.pointer = (self.pointer[0],self.pointer[1]+1)
            self.canvas.move(self.r1,0,self.ssq)
            
    def keyLeft(self,event):
        if self.pointer[0]>0:
            self.pointer = (self.pointer[0]-1,self.pointer[1])
            self.canvas.move(self.r1,-self.ssq,0)
            
    def keyRight(self,event):
        if self.pointer[0]<(self.width-1):
            self.pointer = (self.pointer[0]+1,self.pointer[1])
            self.canvas.move(self.r1,self.ssq,0)
            
    def keySpace(self):
        if self.isSelect:
            c = self.board[self.pointer[1]][self.pointer[0]]
            
            if c=='.':
                self.select = self.pointer
                self.canvas.delete(self.r2)
                t2 = self.tupleRect(self.select[0],self.select[1])
                self.r2 = self.canvas.create_rectangle(t2[0],t2[1],t2[2],t2[3],outline='yellow',width=10)
            
            elif c=='o':
                self.move()
                self.isSelect = False
                self.drawBoard()
                self.drawPointer()

                self.checkVictory()
                self.checkDefeat()
            
            else:
                self.isSelect = False
        else:
            self.select = self.pointer
            self.isSelect = True
            t2 = self.tupleRect(self.select[0],self.select[1])
            self.r2 = self.canvas.create_rectangle(t2[0],t2[1],t2[2],t2[3],outline='yellow',width=10)
      
    def show(self,s1,s2):
        messagebox.showinfo(s1,s2)
        self.canvas.delete("all")
        self.changeFrame(self.win2,self.win1)
        
    def checkVictory(self):
        if self.npieces==1:
            self.show("Victory","You Win.")
    
    def checkDefeat(self):
        def getDir(x,size):
            a = {x-2,x+2}
            dc = {x-2:(x-2,x-1), x+2:(x+1,x+2)}
            b = set(range(size))
            c = list(a.intersection(b))
            c.sort()
            d = []
            for i in c:
                d.append(dc[i])
            return d
            
        def tstring(x1,y1,x2,y2,z1,z2):
            st = self.board[x1][y1]+self.board[x2][y2]
            if z1<z2:
                st = st[::-1]
            s.append(st)
            
        for i in range(self.width):
            for j in range(self.height):
                if self.board[j][i]=='.':
                    a = getDir(j,self.height)
                    b = getDir(i,self.width)
                    s = []
                    for k in a:
                        tstring(k[0],i,k[1],i,k[0],j)
                    for k in b:
                        tstring(j,k[0],j,k[1],k[0],i)
                    if ".o" in s:
                        return
        self.show("Defeat","You Lose.")
        
    def key(self,event):
        if event.char == ' ':
            self.keySpace()
     

    def move(self):
        def diff(t1,t2):
            return (t1[0]-t2[0],t1[1]-t2[1])
            
        def neig(p,v):
            return p[0]+v[0] , p[1]+v[1]
            
        d = diff(self.select,self.pointer)
        
        if d==(2,0):
            vet = (1,0)
        elif d==(-2,0):
            vet = (-1,0)
        elif d==(0,2):
            vet = (0,1)
        elif d==(0,-2):
            vet = (0,-1)
        else:
            return
            
        x , y = neig(self.pointer,vet)
        if self.board[y][x]=='.':
            x1 , y1 = self.select
            x2 , y2 = self.pointer
            self.board[y][x]='o'
            self.board[y1][x1]='o'
            self.board[y2][x2]='.'
            self.npieces -= 1
        else:
            return
    
        
    def loadBoard(self):
        self.board = open('boards/'+self.sboard+'.brd','r+').readlines()
        
        # remove blank characters
        for i in range(len(self.board)):
            self.npieces += self.board[i].count('.')
            for j in ['\n','\t',' ']:
                self.board[i] = (self.board[i].split(j))[0]
            self.board[i] = list(self.board[i])
        
          
        self.width = len(self.board)
        self.height = len(self.board[0])
        sh = self.dim[1]/self.height
        sw = self.dim[0]/self.width
        self.ssq = min(sh,sw)
        self.sp = self.ssq//4
            
    def tupleRect(self,x,y):
        return (x*self.ssq,y*self.ssq,(x+1)*self.ssq,(y+1)*self.ssq)
            
    def drawBoard(self):
        color = {'#':'white','.':'gray','o':'gray'}
        color_piece = 'blue'
        for i in range(self.width):
            for j in range(self.height):
                t = self.tupleRect(i,j)
                self.canvas.create_rectangle(t[0],t[1],t[2],t[3],fill=color[self.board[j][i]],width=1)
                if self.board[j][i]=='.':
                    self.canvas.create_oval(self.sp+i*self.ssq,self.sp+j*self.ssq,(i+1)*self.ssq-self.sp,(j+1)*self.ssq-self.sp,fill=color_piece)
                    
    def drawPointer(self):
        t1 = self.tupleRect(self.pointer[0],self.pointer[1])
        self.r1 = self.canvas.create_rectangle(t1[0],t1[1],t1[2],t1[3],outline='red',width=10)
        
    def drawSelection(self):
        t2 = self.tupleRect(self.select[0],self.select[1])
        self.r2 = self.canvas.create_rectangle(t2[0],t2[1],t2[2],t2[3],outline='yellow',width=10)
