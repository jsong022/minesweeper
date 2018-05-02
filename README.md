## Minesweeper

### Introduction
My own versions of the classic Minesweeper game. 2 versions both written with Python 3.6.3. 

### File Descriptions
- minesweeper.py - runs a command line interface version
- minesweeperGUI.py - runs a Minesweeper game with a GUI built with tkinter

### Instructions for GUI version
- left click on boxes to reveal that tile
- right click on boxes to toggle flag
	- flagged tile cannot be revealed
- middle click on revealed tiles to reveal all adjacent tiles
	- only works if the number being shown is equal to number of adjacent flags
- left click on smiley to quick restart with same board dimensions & number of mines
- on Win:
	- all unflagged mines are flagged
- on Loss:
	- all Mines that have not been flagged are revealed
	- Exploded Mine (the cause of loss) is marked with a red background
	- all incorrect Flags are crossed out

### Instructions for Command Line version
- Game will first prompt for the minefield dimensions and the total number of mines
	- input format should be "R C M" where R, C, and M are integers separated by a space
		- R = # of rows i.e. board height
		- C = # of columns i.e. board width
		- M = # of mines on the field
	- There is no input checking for this set up, so the user is expected to provide a good input
- The first move is always a "show" action i.e. left click in Microsoft Minesweeper
	- input format should be a single integer, "I"
		- I = position on the board to check
		- Position index starts from 0 as top-left corner.
		- Index increments from left to right and top to bottom
- All subsequent can be either a "show" or a "flag" action
	- a Show action input format may be "show i" or "s i"
		- i = position on the board to check as an integer
	- a Flag action input format may be "flag i" or "f i"
		- i = position on the board to toggle flag
	- Show action on an already revealed square or a flagged square has no effect
	- Flag action on a flagged square will revert it back to an unknown square
	- Flag action on an already revealed square has no effect
- Show action taken on an empty square, or a square with no bombs adjacent to it will cascade to adjacent squares
	- Cascading show action will continue cascading until a non-empty adjacent square is hit in all directions
- Loss condition: a Show action is taken on a mine square
- Win condition: Number of flagged or unknown squares equal to number of mines on the field
	- i.e. all non-mine squares have been revealed
- Game will ask if user wants to replay upon game ending
	- input should be "y" for yes or "n" for no

### Game Board Notation Legend of Command Line version
- ?? = Unknown Square
- !! = Flagged Square
- __ = Empty Square
- 1-8 = Number of Mines Adjacent to that Square
- MN = Revealed Mine Square

### Board Indexing Example of Command Line version
0	1	2

3	4	5

6	7	8

### To-Do
- [x] Implement a simple version of the game with hard coded settings
- [x] Implement a command line interface for the set up
- [x] Finalize the base gameplay logic (win condition, replays, timer, etc)
- [x] Create a GUI
- [ ] Implement all base gameplay functionality in GUI version
	- [ ] Custom game settings (currently hardcoded 10x10 board wtih 20 mines)
	- [x] Difficulty levels (Beginner, Intermediate, and Expert) chosen from menu bar
	- [x] Proper end of game (currently program just quits upon win/loss)
	- [x] Replay functionality added (as a menu item under Game). Replay with same boardsize & number of mines.
	- [x] Middle Mouse Button functionality added
	- [x] Add comments/docstrings
- [ ] Make GUI look pretty (IN PROGRESS)
	- [x] Added a flag counter
	- [x] Added total number of mines on field
	- [x] Fixed window size
	- [x] Smiley Button that is animated and works as a quick reset 