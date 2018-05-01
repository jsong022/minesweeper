import random
import time
import tkinter as tk
from tkinter import messagebox

class myButton(tk.Button):
    def __init__(self, window, text, row, col, rows, cols):
        tk.Button.__init__(self,window, text=text)
        self.row = row
        self.col = col
        self.rows = rows
        self.cols = cols
        
class Tile(object):
    def __init__(self, window, row, col, rows, cols, shown = False, mine = False, count = 0):
        self.shown = shown
        self.mine = mine
        self.count = count
        self.window = window
        self.flag = False
        self.adj = []
        self.label = tk.Label(window, text=str(count))
        self.label.grid(row = row, column = col)
        self.button = myButton(window, text="  ", row=row, col=col, rows=rows, cols=cols)
        self.button.grid(row = row, column = col)
        #right click press
        self.button.bind('<ButtonPress-3>', self.rightClickPress)
        #right click release
        self.button.bind('<ButtonRelease-3>', self.setFlag)

    def setMine(self):
        self.count = -1
        self.label.configure(text = "X")
        self.mine = True

    def rightClickPress(self, event):
        self.button.configure(relief = "sunken")
        
    def setFlag(self, event):
        if self.shown: return
        self.button.configure(relief = "raised")
        self.flag = not(self.flag)
        self.button.configure(text = "!!" if self.flag else "  ")
    
    def countMines(self):
        if self.mine:
            return
        num = 0
        for tile in self.adj:
            num += 1 if tile.isMine() else 0
        self.count = num
        self.label.configure(text = str(num) + " ")
    
    def show(self, event=None):
        if not self.shown:
            check = 1
            self.shown = True
            self.button.grid_remove()
            if self.count == 0: check += self.showAround()
            elif self.mine: return -1
            return check
        return 0

    def showAround(self):
        check = 0
        for sqr in self.adj:
            if sqr is not None: check += sqr.show()
        return check
        
    #returns true iff the square's value is negative i.e. it is a Mine
    def isMine(self):
        return self.mine

    #returns true iff the square's value is 0
    def isZero(self):
        return self.count == 0

    #returns true iff shown is 9 i.e. the square is not currently being shown
    def isShown(self):
        return self.shown
    
    #returns true iff shown is 10 i.e. the square is flagged as a mine
    def isFlagged(self):
        return self.flag

class Board(object):
    def __init__(self, rows, cols, minecount, window):
        self.rows = rows
        self.cols = cols
        self.numChecked = 0
        self.minecount = minecount
        self.window = window
        self.tiles = []
        self.mines = []
        self.minesArmed = False
        self.startTime = None
        
        #add all tiles to the board
        for row in range(rows):
            self.tiles.append([])
            for col in range(cols):
                self.tiles[row].append(Tile(window=window, row=row, col=col, rows=rows, cols=cols))
                self.tiles[row][col].button.bind('<ButtonPress-1>',  self.setUpBombs)
                self.tiles[row][col].button.bind('<ButtonRelease-1>',  self.showTile)
                
        #set up adjacency lists for each tile
        for row in range(rows):
            for col in range(cols):
                #row above current tile
                if row-1 >= 0:
                   if col-1 >= 0: self.tiles[row][col].adj.append(self.tiles[row-1][col-1])
                   self.tiles[row][col].adj.append(self.tiles[row-1][col])
                   if col+1 < cols: self.tiles[row][col].adj.append(self.tiles[row-1][col+1])
                #current row
                if col-1 >= 0: self.tiles[row][col].adj.append(self.tiles[row][col-1])
                if col+1 < cols: self.tiles[row][col].adj.append(self.tiles[row][col+1])
                #row below current tile
                if row+1 < rows:
                   if col-1 >= 0: self.tiles[row][col].adj.append(self.tiles[row+1][col-1])
                   self.tiles[row][col].adj.append(self.tiles[row+1][col])
                   if col+1 < cols: self.tiles[row][col].adj.append(self.tiles[row+1][col+1])
    
    def setUpBombs(self, event):
        if self.minesArmed:return 0
        pos = (event.widget.row * event.widget.cols) + event.widget.col
        size = event.widget.rows * event.widget.cols
        #get a list random indexes in range to be mines
        self.mines = random.sample(range(size), self.minecount)
        if pos in self.mines:
            self.mines.remove(pos)
            temp = random.sample(range(size), 1)[0]
            while (temp == pos): temp = random.sample(range(size), 1)[0]
            self.mines.append(temp)
        #mark all mine squares as mines
        for mine in self.mines:
            targetRow = int(mine/cols)
            targetCol = mine % cols
            self.tiles[targetRow][targetCol].setMine()
        #calculate the number in each Square of the current game
        for row in self.tiles:
            for tile in row:
                tile.countMines()
        self.minesArmed = True
        self.startTime = time.time()
        return 1

    def showTile(self, event):
        row, col = event.widget.row, event.widget.col
        returned = self.tiles[row][col].show()
        if returned < 0:
            self.endGame("You Lost!\n")
        else:
            self.numChecked += returned
            if (self.rows * self.cols) - self.numChecked == self.minecount:
                self.endGame("You Won!\n")
                
    def endGame(self, msg):
            elapsedTime = time.time() - self.startTime
            readableTime = str(int((elapsedTime / 60) / 60))
            readableTime += ":" + str(int(elapsedTime / 60))
            readableTime += ":" + str(elapsedTime % 60)[0:6]
            msg +="Time: " + readableTime
            messagebox.showinfo('Game Over', msg)
            quit()

rows, cols = 10, 10
window = tk.Tk()
window.title("Minesweeper")
myBoard = Board(rows, cols, 20, window)
window.geometry("500x500")
window.mainloop()
