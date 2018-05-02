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
    # images[] is a Tile class which will hold all the images needed by a Tile
    #   [0] is empty background
    #   [1] to [8] are the numbers
    #   [9] is a mine, [10] is empty button, [11] is flag
    #   [12] is incorrect flag, [13] is exploded mine
    images = []
        
    def __init__(self, parent, row, col):
        """ Attributes:
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
        self.shown = False
        self.mine = False
        self.flag = False
        self.inPlay = True
        self.count = 0
        self.numFlags = 0
        self.parent = parent
        self.adj = []

        #set up the 2 myLabel() objects and place them on the grid
        self.label = myLabel(parent, image=Tile.images[0], row=row, col=col, tile=self)
        self.label.configure(padx = 0, pady = 0, borderwidth = 0)
        self.label.grid(row = row+1, column = col)
        self.button = myLabel(parent, image=Tile.images[10], row=row, col=col, tile=self)
        self.button.configure(padx = 0, pady = 0, borderwidth = 0)
        self.button.grid(row = row+1, column = col)

    def replay(self):
        """ Resets the Tile to for the game to be restarted """
        if self.shown: self.button.grid(row = self.label.row+1, column=self.label.col)
        self.shown = False
        self.mine = False
        self.flag = False
        self.inPlay = True
        self.count = 0
        self.numFlags = 0
        self.label.configure(image=Tile.images[0])
        self.button.configure(image=Tile.images[10])

    def setMine(self):
        """ Sets the Tile as a mine
            self.count attribute is changed to -1 (old code kept around just in case)
            self.label's image is change to be the Mine (still hidden by self.button)
            marks self.mine boolean attribute to be true
        """
        self.count = -1
        self.label.configure(image = Tile.images[9])
        self.mine = True

    def buttonPress(self, event=None):
        """ Changes the image of self.button, a myLabel() object
            to indicate it is currently being clicked on
            Only works for Tiles that are in play (self.inPlay == True)
        """
        if self.inPlay: self.button.configure(image = Tile.images[0])
        
    def setFlag(self):
        """ Toggles the flag on the tile if it is still unknown and in play
            self.flag boolean attribute is toggled
            and changes the image of self.button, a myLabel() hiding the hidden mine/number
            also increments or decrements the numFlags of all adjacent Tiles
            Returns 1 if flag is toggled on and -1 if flag is toggled off
            Returns 0 if flag was not toggled
        """
        if self.shown or not self.inPlay: return 0
        self.flag = not(self.flag)
        image_index = 11 if self.flag else 10
        self.button.configure(image = Tile.images[image_index])
        flag_change = 1 if self.flag else -1
        for adjTile in self.adj:
            adjTile.numFlags += flag_change
        return flag_change

    def countMines(self):
        """ Counts the number of mines around the current Tile()
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
        self.label.configure(image = Tile.images[num])
    
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
                if self.inPlay: self.label.configure(image = Tile.images[13])
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
    
    def isFlagged(self):
        """ returns true iff shown is 10 i.e. the square is flagged as a mine"""
        return self.flag

    def isInPlay(self):
        """ returns self.inPlay which is True when the game is being played"""
        return self.inPlay

    def isSafe(self):
        """ returns True if # of adjacent Flags == # of adjacent mines
                and if self.shown is True
        """ 
        return self.numFlags == self.count and self.shown

class Board(object):
    def __init__(self, rows, cols, minecount, parent):
        self.rows = rows
        self.cols = cols
        self.numChecked = 0
        self.numMines = minecount
        self.numFlags = 0
        self.parent = parent
        self.tiles = []
        self.minesArmed = False
        self.startTime = None

        self.frame = tk.Frame(parent)
        self.frame.pack()
        self.mineLabel = tk.Label(self.frame, text="Mines: "+str(self.numMines))
        self.mineLabel.grid(row=0, column=0, sticky="W", columnspan=3)
        self.flagLabel = tk.Label(self.frame, text="Flags: "+str(self.numFlags))
        self.flagLabel.grid(row=0, column=self.cols-3, sticky="E", columnspan=3)
        
        #add all tiles to the board
        for row in range(rows):
            self.tiles.append([])
            for col in range(cols):
                tile = Tile(parent=self.frame, row=row, col=col)
                self.tiles[row].append(tile)
                #left click listeners
                tile.button.bind('<ButtonPress-1>',  self.pressTile)
                tile.button.bind('<ButtonRelease-1>',  self.showTile)
                #middle click listeners
                tile.label.bind('<ButtonPress-2>', self.pressAdjTiles)
                tile.label.bind('<ButtonRelease-2>', self.showAdjTiles)
                #right click listeners
                tile.button.bind('<ButtonPress-3>', self.pressTile)
                tile.button.bind('<ButtonRelease-3>', self.toggleFlag)
                
        #set up adjacency lists for each tile
        for row in range(rows):
            for col in range(cols):
                adj = self.tiles[row][col].adj
                #row above current tile
                if row-1 >= 0:
                   if col-1 >= 0: adj.append(self.tiles[row-1][col-1])
                   adj.append(self.tiles[row-1][col])
                   if col+1 < cols: adj.append(self.tiles[row-1][col+1])
                #current row
                if col-1 >= 0: adj.append(self.tiles[row][col-1])
                if col+1 < cols: adj.append(self.tiles[row][col+1])
                #row below current tile
                if row+1 < rows:
                   if col-1 >= 0: adj.append(self.tiles[row+1][col-1])
                   adj.append(self.tiles[row+1][col])
                   if col+1 < cols: adj.append(self.tiles[row+1][col+1])
    
    def replay(self, event=None):
        """ Resets the Board to be replayed with the same settings
            Note: the mine placement is randomized again
        """
        self.numChecked = 0
        self.numFlags = 0
        self.minesArmed = False
        self.startTime = None
        self.mineLabel.configure(text="Mines: "+str(self.numMines))
        self.flagLabel.configure(text="Flags: "+str(self.numFlags))
        for row in self.tiles:
            for tile in row:
                tile.replay()

    def setUpBombs(self, event):
        pos = (event.widget.row * self.cols) + event.widget.col
        size = self.rows * self.cols
        #get a list random indexes in range to be mines
        mines = random.sample(range(size), self.numMines)
        if pos in mines:
            mines.remove(pos)
            temp = random.sample(range(size), 1)[0]
            while (temp == pos): temp = random.sample(range(size), 1)[0]
            mines.append(temp)
        #mark all mine squares as mines
        for mine in mines:
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

    def checkEnd(self, num):
        """ ends the game as a Loss if num < 0
            Otherwise adds num to self.numChecked
            ends the game as a win if win conditions are met
            i.e. total # of tiles - # of tiles checked == # of mines
        """
        if num < 0:
            self.endGame("You Lost!\n")
        else:
            self.numChecked += num
            if (self.rows * self.cols) - self.numChecked == self.numMines:
                self.endGame("You Won!\n")

    def pressTile(self, event):
        """ Changes the image on the clicked Tile accordingly
            i.e. if Tile not isFlagged()
            also calls setUpBombs() if this is the first left click of the game
        """
        clickedTile = event.widget.tile
        if not clickedTile.isFlagged():
            clickedTile.buttonPress()
            if not self.minesArmed and event.num == 1:
                self.setUpBombs(event)

    def toggleFlag(self, event):
        """ calls setFlag() on the Tile that was right clicked"""
        self.numFlags += event.widget.tile.setFlag()
        self.flagLabel.configure(text="Flags: "+str(self.numFlags))
        
                
    def pressAdjTiles(self, event):
        """ Changes the image on the adjacent Tiles to be clicked
            only if the adjacent Tile is not flagged and not shown
        """
        clickedTile = event.widget.tile
        for adjTile in clickedTile.adj:
            if not adjTile.isFlagged():
                adjTile.buttonPress()
        
    def showTile(self, event):
        if event.widget.tile.isInPlay():
            returned = event.widget.tile.show()
            self.checkEnd(returned)

    def showAdjTiles(self,event):
        clickedTile = event.widget.tile
        if clickedTile.isSafe() and clickedTile.isInPlay(): 
            returned = event.widget.tile.showAround()
            self.checkEnd(returned)
        else:
            for adjTile in clickedTile.adj:
                if not adjTile.isFlagged():
                    adjTile.button.configure(image=Tile.images[10])
            
    def revealBombs(self):
        for row in self.tiles:
            for tile in row:
                tile.inPlay = False
                if tile.isMine():
                    tile.show()
                elif tile.isFlagged():
                    tile.button.configure(image=Tile.images[12])
        
    def endGame(self, msg):
        elapsedTime = time.time() - self.startTime
        readableTime = str(int((elapsedTime / 60) / 60))
        readableTime += ":" + str(int(elapsedTime / 60))
        readableTime += ":" + str(elapsedTime % 60)[0:6]
        msg +="Time: " + readableTime
        self.revealBombs()
        messagebox.showinfo('Game Over', msg)

def reset(rows,cols,mines,root):
    """ Calls root.destroy and restarts the game with given settings
        Arguments:
            rows = # rows in the new game
            cols = # columns in the new game
            mines = # of mines in the new game
    """
    root.destroy()
    main(rows,cols,mines)

def main(rows, cols, mines):
    root = tk.Tk()
    #clear Tile.images
    del Tile.images[:]
    #load all needed images into Tile.images
    for i in range(14):
        Tile.images.append(tk.PhotoImage(file = "images/tile-"+str(i)+".gif"))
    menu = tk.Menu(root)
    root.configure(menu=menu)
    root.title("Minesweeper")
    myBoard = Board(rows, cols, mines, root)
    gamemenu = tk.Menu(menu, tearoff = False)
    menu.add_cascade(label="Game", menu=gamemenu)
    gamemenu.add_command(label="Replay", command=lambda: myBoard.replay())
    gamemenu.add_separator()
    gamemenu.add_command(label="Beginner", command=lambda: reset(8,8,10,root))
    gamemenu.add_command(label="Intermediate", command=lambda: reset(16,16,40,root))
    gamemenu.add_command(label="Expert", command=lambda: reset(16,30,99,root))
    gamemenu.add_separator()
    gamemenu.add_command(label="Custom", command=None)
    gamemenu.add_separator()
    gamemenu.add_command(label="Exit", command=root.destroy)
    windowWidth = str(20*cols+40)
    windowHeight = str(20*rows+40)
    root.geometry(windowWidth+'x'+windowHeight)
    root.minsize(windowWidth, windowHeight)
    root.maxsize(windowWidth, windowHeight)
    root.mainloop()

if __name__ == "__main__":
    main(10,10,20)
