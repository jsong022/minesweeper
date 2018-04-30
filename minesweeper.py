import random
import time

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
            check = 1
            self.shown = self.count
            if self.count is 0: check += self.showAround()
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
        self.numChecked = 0
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
        return time.time()

    # returns true iff number of unchecked mines is the same and minecount
    # i.e. the game has been won
    def checkEnd(self):
        return (self.row * self.col) - self.numChecked == self.minecount 

    def flag(self, pos):
        self.state[pos].setFlag()
        self.print()

    def show(self, pos):
        temp = self.state[pos].show()
        self.print()
        if temp is -1: return False
        self.numChecked += temp
        return True;

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

class App(object):
    def __init__(self):
        myGame = None
        startTime = None
        endTime = None
        playing = False

    def endGame(self, msg):
        print(msg)
        self.endTime = time.time()
        elapsedTime = self.endTime - self.startTime
        readableTime = str(int((elapsedTime / 60) / 60))
        readableTime += ":" + str(int(elapsedTime / 60))
        readableTime += ":" + str(elapsedTime % 60)[0:6]
        print("Time: " + readableTime)
        if msg == "You Lose!": self.myGame.printSolution()
        self.playing = False

    def setUp(self):
        prompt = "How many rows, columns, and mines?"
        prompt += "\n(Please give input as 3 integers separated by spaces)\n-> "
        cmd = input(prompt).split(' ')
        self.myGame = Game(int(cmd[0]),int(cmd[1]),int(cmd[2]))
        self.myGame.print()

    def firstMove(self):
        move = int(input("What is your first move?\n-> "))
        self.startTime = self.myGame.start(move)
        self.playing = self.myGame.show(move)
        if (self.playing):
            if self.myGame.checkEnd(): self.endGame("You Win!")
        else:
            self.endGame("You Lose!")

    def makeMoves(self):
        while self.playing:
            cmd = input("Next move?\n-> ")
            if cmd == "give up":
                self.endGame("Giving up...")
            elif cmd == "quit":
                print("Quitting Game!")
                exit()
            cmd = cmd.split(" ")
            if (len(cmd) is not 2) or (int(cmd[1]) >= len(self.myGame.state)) or (int(cmd[1]) < 0):
                print("Invalid Input! Try Again.")
            elif cmd[0] == "show" or cmd[0] == "s":
                self.playing = self.myGame.show(int(cmd[1]))
                if (self.playing):
                    if self.myGame.checkEnd(): self.endGame("You Win!")
                else: self.endGame("You Lose!")
            elif cmd[0] == "flag" or cmd[0] == "f":
                self.myGame.flag(int(cmd[1]))
            else:
                print("Invalid Input! Try Again.")

    def playGame(self):
        self.setUp()
        self.firstMove()
        self.makeMoves()
        replay = True
        while replay:
            cmd = input("\nPlay Again? (y/n)\n-> ")
            if cmd == "y":
                replay = False
                self.playGame()
            elif cmd == "n":
                replay = False
                print("Quitting Game!")
                exit()
            else:
                print("Please input 'y' for yes or 'n' for no") 
    
App().playGame()
