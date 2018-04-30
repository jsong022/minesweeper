import random

class Square(object):
    def __init__(self, shown = 9, mine = False, count = 0):
        self.shown = shown
        self.mine = mine
        self.count = 0
        self.adj = []
        for i in range(8): self.adj.append(None)
    
    def setMine(self):
        self.count = -1
        self.mine = True
    
    def setFlag(self):
        if self.shown is 9: self.shown = 10
        elif self.shown is 10: self.shown = 9
    def countMines(self):
        if self.mine: return
        self.count = 0
        for sqr in self.adj:
            if sqr is not None:
                self.count += 1 if sqr.isMine() else 0
    
    def show(self):
        if self.isUnknown():
            self.shown = self.count
            if self.count is 0: self.showAround()
            elif self.mine: return False
        return True

    def showAround(self):
        for sqr in self.adj:
            if sqr is not None: sqr.show()
        
    #returns true iff the square's value is negative i.e. it is a Mine
    def isMine(self):
        return self.mine

    #returns true iff the square's value is 0
    def isZero(self):
        return self.count is 0

    #returns true iff shown is 9 i.e. the square is not currently being shown
    def isUnknown(self):
        return self.shown is 9
    
    #returns true iff shown is 10 i.e. the square is flagged as a mine
    def isFlagged(self):
        return self.shown is 10
    
class Game(object):
    def __init__(self, row, col, minecount):
        self.row = row
        self.col = col
        self.minecount = minecount
        self.state = []
        for i in range(row*col):
            sqr = Square()
            self.state.append(sqr)
        for i in range(row*col):
            sqr = self.state[i]
            #set up upper row adjacencies for each Square not in top row
            if int(i/col) is not 0:
                if i % col is not 0: sqr.adj[0] = self.state[i-col-1]
                if i % col is not col - 1: sqr.adj[2] = self.state[i-col+1]
                sqr.adj[1] = self.state[i-col]
            #set up lower row adjacencies for each Square not in bottom row
            if int(i/col) is not row - 1:
                if i % col is not 0: sqr.adj[5] = self.state[i+col-1]
                if i % col is not col - 1: sqr.adj[7] = self.state[i+col+1]
                sqr.adj[6] = self.state[i+col]
            #left side adjacency
            if i % col is not 0: sqr.adj[3] = self.state[i-1]
            #right side adjacency
            if i % col is not col - 1: sqr.adj[4] = self.state[i+1]

    # first move of the game places all the Mines
    # and sets up the mineCount for every Square
    # and ensures state[pos] is not a Mine, preventing first click loss
    def start(self, pos):
        size = self.row * self.col
        #get a list random indexes in range to be mines
        mines = random.sample(range(size), self.minecount)
        #make sure the first checked square is not a mine
        if pos in mines:
            mines.remove(pos)
            temp = random.sample(range(size), 1)[0]
            while (temp == pos): temp = random.sample(range(size), 1)[0]
            mines.append(temp)
        #mark all mine squares as mines
        for mine in mines:
            self.state[mine].setMine()
        #calculate the number in each Square of the current game
        for sqr in self.state:
            sqr.countMines()

    #prints out the current state
    def print(self):
        line = "-"
        for i in range(self.col):
            line += "---"
        print(line)
        msg = "" 
        for i in range(self.row * self.col):
            if i % self.col is 0: msg += "|"
            if self.state[i].isUnknown(): msg += "??"
            elif self.state[i].isFlagged(): msg += "!!"
            elif self.state[i].isMine(): msg += "MN"
            elif self.state[i].isZero(): msg += "__"
            else: msg += str(self.state[i].shown) + " "
            msg += "|"
            if i % self.col is self.col - 1:
                print(msg)
                msg = ""
                print(line)
        print()

    #prints out all the values of the current state
    def printSolution(self):
        line = "-"
        for i in range(self.col):
            line += "---"
        print(line)
        msg = "" 
        for i in range(self.row * self.col):
            if i % self.col is 0: msg += "|"
            if self.state[i].isMine(): msg += "MN"
            elif self.state[i].isZero(): msg += "__"
            else:
                msg += str(self.state[i].count)
                msg += " "
            msg += "|"
            if i % self.col is self.col - 1:
                print(msg)
                msg = ""
                print(line)
cmd = input("How many rows, columns, and mines?\n(Please give input as 3 integers separated by commas)\n-> ").split(',')
myGame = Game(int(cmd[0]),int(cmd[1]),int(cmd[2]))
move = int(input("What is your first move?\n-> "))
myGame.start(move)
myGame.state[move].show()
myGame.print()
play = True
while (play):
    cmd = input("Next move?\n-> ")
    if cmd == "quit":
        print("Quitting Game!")
        exit()
    cmd = cmd.split(" ")
    if (len(cmd) is not 2) or (int(cmd[1]) >= len(myGame.state)) or (int(cmd[1]) < 0):
        print("Invalid Input! Try Again.")
    elif cmd[0] == "show" or cmd[0] == "s":
        play = myGame.state[int(cmd[1])].show()
        myGame.print()
    elif cmd[0] == "flag" or cmd[0] == "f":
        myGame.state[int(cmd[1])].setFlag()
        myGame.print()
    else:
        print("Invalid Input! Try Again.")
    if not play: print("YOU LOSE!")
