import random
import time
import tkinter as tk
from tkinter import messagebox

class myLabel(tk.Label):
    def __init__(self, parent, image, row, col, tile):
        """ Custom Attributes:
            self.row: Integer denoting the row location of this Label (e.g. 0 is first row)
            self.col: Integer denoting the column location of this Label (e.g. 0 is left most column)
            self.tile: points to the Tile() instance this myLabel belongs to
        """
        tk.Label.__init__(self,parent, image=image)
        self.row = row
        self.col = col
        self.tile = tile
        
class Tile(object):
    def __init__(self, parent, row, col):
        """ sets up self.images[] attribute which loads all the images needed by a Tile
                [0] is empty background
                [1] to [8] are the numbers
                [9] is a mine, [10] is empty button, [11] is flag
                [12] is incorrect flag, [13] is exploded mine
            Attributes:
                self.shown: boolean that is True when Tile has been revealed
                self.mine: boolean that is True if the Tile is a mine
                self.flag: boolean that is True if the Tile has been flagged
                self.inPlay: boolean that is True if the game is in play
                self.count: Integer for number of adjacent mine Tiles (-1 if mine)
                self.numFlags: Integer for number of adjacent Flagged Tiles
                self.parent: the parent element (should be main window)
                self.adj: a list() to hold adjacent Tile instances
                self.label: a myLabel() that shows the mine/number of adjacent mines
                self.button: a myLabel() that is hiding the Tile's value
        """
        #set up instance variables
        self.images = []
        for i in range(14):
            self.images.append(tk.PhotoImage(file = "images/tile-"+str(i)+".gif"))
        self.shown = False
        self.mine = False
        self.flag = False
        self.inPlay = True
        self.count = 0
        self.numFlags = 0
        self.parent = parent
        self.adj = []

        #set up the 2 myLabel() objects and place them on the grid
        self.label = myLabel(parent, image=self.images[0], row=row, col=col, tile=self)
        self.label.config(padx = 0, pady = 0, borderwidth = 0)
        self.label.grid(row = row, column = col)
        self.button = myLabel(parent, image=self.images[10], row=row, col=col, tile=self)
        self.button.config(padx = 0, pady = 0, borderwidth = 0)
        self.button.grid(row = row, column = col)
        
        #right click press listener on button
        self.button.bind('<ButtonPress-3>', self.buttonPress)
        #right click release listener on button
        self.button.bind('<ButtonRelease-3>', self.setFlag)
    
    def setMine(self):
        """Sets the Tile as a mine
            self.count attribute is changed to -1 (old code kept around just in case)
            self.label's image is change to be the Mine (still hidden by self.button)
            marks self.mine boolean attribute to be true
        """
        self.count = -1
        self.label.configure(image = self.images[9])
        self.mine = True

    def buttonPress(self, event=None):
        """Changes the image of self.button, a myLabel() object
            to indicate it is currently being clicked on
            Only works for Tiles that are in play (self.inPlay == True)
        """
        if self.inPlay: self.button.configure(image = self.images[0])
        
    def setFlag(self, event):
        """Toggles the flag on the tile if it is still unknown and in play
            self.flag boolean attribute is toggled
            and changes the image of self.button, a myLabel() hiding the hidden mine/number
        """
        if self.shown or not self.inPlay: return
        self.flag = not(self.flag)
        image_index = 11 if self.flag else 10
        self.button.configure(image = self.images[image_index])

        
    def countFlags(self):
        """Counts the number of flags around the current Tile()
            saves the number in self.numFlags attribute
            and returns the final self.numFlags
        """
        num = 0
        for tile in self.adj:
            num += 1 if tile.isFlagged() else 0
        self.numFlags = num
        return self.numFlags

    def countMines(self):
        """Counts the number of mines around the current Tile()
            saves the count in self.count attribute.
            Additionally, it changes the self.label

            Does not count if this Tile() is a mine.
        """
        if self.mine:
            return
        num = 0
        for tile in self.adj:
            num += 1 if tile.isMine() else 0
        self.count = num
        self.label.configure(image = self.images[num])
    
    def show(self, event=None):
        """ Removes the self.button myLabel() that has been hiding the value/mine
            Has no effect on Tiles that are already being shown
            Calls self.showAround() to cascade if self.count == 0
            Returns -1 if one or more of the revealed Tiles is a Mine.
            Returns the number of Tiles revealed by it as an Integer.
        """
        if not self.shown and not self.flag:
            check = 1
            self.shown = True
            self.button.grid_remove()
            if self.count == 0:
                num = self.showAround()
                if (check < 0) or (num < 0): check = -1
                else: check += num
            elif self.mine:
                if self.inPlay: self.label.configure(image = self.images[13])
                return -1
            return check
        return 0

    def showAround(self):
        """ Calls show() on all Tiles around self
            Returns -1 if one or more of mines have been revealed
            Otherwise returns the total number of tiles revealed
        """
        check = 0
        for sqr in self.adj:
            if sqr is not None:
                num = sqr.show()
                if (check < 0) or (num < 0): check = -1
                else: check += num
        return check

    def isMine(self):
        """ returns self.mine which is True if the Tile is a mine"""
        return self.mine

    def isZero(self):
        """ returns self.count == 0 i.e. True only if there are no Mines around this Tile"""
        return self.count == 0

    def isShown(self):
        """ returns self.shown which is True if the Tile has been revealed"""
        return self.shown
    
    def isFlagged(self):
        """ returns true iff shown is 10 i.e. the square is flagged as a mine"""
        return self.flag

    def isInPlay(self):
        """ returns self.inPlay which is True when the game is being played"""
        return self.inPlay

class Board(object):
    def __init__(self, rows, cols, minecount, parent):
        self.rows = rows
        self.cols = cols
        self.numChecked = 0
        self.minecount = minecount
        self.parent = parent
        self.tiles = []
        self.mines = []
        self.minesArmed = False
        self.startTime = None
        
        #add all tiles to the board
        for row in range(rows):
            self.tiles.append([])
            for col in range(cols):
                self.tiles[row].append(Tile(parent=parent, row=row, col=col))
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
        clickedTile = event.widget.tile
        # do nothing if clicked on Flag tile
        if clickedTile.isFlagged(): return 0
        clickedTile.buttonPress()
        # end function if this isn't the first tile revealed in the game
        if self.minesArmed:return 0
        pos = (event.widget.row * self.cols) + event.widget.col
        size = self.rows * self.cols
        #get a list random indexes in range to be mines
        self.mines = random.sample(range(size), self.minecount)
        if pos in self.mines:
            self.mines.remove(pos)
            temp = random.sample(range(size), 1)[0]
            while (temp == pos): temp = random.sample(range(size), 1)[0]
            self.mines.append(temp)
        #mark all mine squares as mines
        for mine in self.mines:
            targetRow = int(mine/self.cols)
            targetCol = mine % self.cols
            self.tiles[targetRow][targetCol].setMine()
        #calculate the number in each Square of the current game
        for row in self.tiles:
            for tile in row:
                tile.countMines()
        self.minesArmed = True
        self.startTime = time.time()
        return 1

    def showTile(self, event):
        if event.widget.tile.isInPlay():
            returned = event.widget.tile.show()
            if returned < 0:
                self.endGame("You Lost!\n")
            else:
                self.numChecked += returned
                if (self.rows * self.cols) - self.numChecked == self.minecount:
                    self.endGame("You Won!\n")

    def revealBombs(self):
        for row in self.tiles:
            for tile in row:
                tile.inPlay = False
                if tile.isMine():
                    tile.show()
                elif tile.isFlagged():
                    tile.button.configure(image=tile.images[12])
        
    def endGame(self, msg):
        elapsedTime = time.time() - self.startTime
        readableTime = str(int((elapsedTime / 60) / 60))
        readableTime += ":" + str(int(elapsedTime / 60))
        readableTime += ":" + str(elapsedTime % 60)[0:6]
        msg +="Time: " + readableTime
        self.revealBombs()
        messagebox.showinfo('Game Over', msg)

def game(rows,cols,mines,root):
    root.destroy()
    main(rows,cols,mines)

def main(rows, cols, mines):
    root = tk.Tk()
    menu = tk.Menu(root)
    root.config(menu=menu)
    root.title("Minesweeper")
    gamemenu = tk.Menu(menu)
    menu.add_cascade(label="Game", menu=gamemenu)
    gamemenu.add_command(label="Beginner", command=lambda: game(8,8,10,root))
    gamemenu.add_command(label="Intermediate", command=lambda: game(16,16,40,root))
    gamemenu.add_command(label="Expert", command=lambda: game(16,30,99,root))
    gamemenu.add_separator()
    gamemenu.add_command(label="Custom", command=None)
    gamemenu.add_separator()
    gamemenu.add_command(label="Exit", command=root.destroy)
    myBoard = Board(rows, cols, mines, root)
    root.geometry(str(20*cols)+"x"+str(20*rows))
    root.mainloop()

if __name__ == "__main__":
    main(10,10,20)
