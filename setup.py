import cx_Freeze
import sys
import os.path
PYTHON_INSTALL_DIR = os.path.dirname(os.path.dirname(os.__file__))
os.environ['TCL_LIBRARY'] = os.path.join(PYTHON_INSTALL_DIR, 'tcl', 'tcl8.6')
os.environ['TK_LIBRARY'] = os.path.join(PYTHON_INSTALL_DIR, 'tcl', 'tk8.6')

if sys.platform == "win32":
	base = "Win32GUI"

executables = [cx_Freeze.Executable("minesweeperGUI.py", base=base)]
cx_Freeze.setup(
	name = "Minesweeper",
	options = {"build_exe": 
		{
                        "includes": ["random", "time", "tkinter.messagebox"],
			#"packages": ["tkinter"],
		 	"include_files": [
		 		"images/tile-0.gif", "images/tile-1.gif", "images/tile-2.gif", "images/tile-3.gif", 
		 		"images/tile-4.gif", "images/tile-5.gif", "images/tile-6.gif", "images/tile-7.gif",
		 		"images/tile-8.gif", "images/tile-9.gif", "images/tile-10.gif", "images/tile-11.gif",
		 		"images/tile-12.gif", "images/tile-13.gif", "images/smile-0.gif", "images/smile-1.gif",
		 		"images/smile-2.gif", "images/smile-3.gif",  "images/smile-4.gif", 
            	os.path.join(PYTHON_INSTALL_DIR, 'DLLs', 'tk86t.dll'),
            	os.path.join(PYTHON_INSTALL_DIR, 'DLLs', 'tcl86t.dll'),
		 	]}},
	version = "0.0.1",
	description = "My own version of Minesweeper game written in Python3 using tkinter",
	executables = executables
)
