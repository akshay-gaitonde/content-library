#commands to run in script editor or to save in shelf

import sys
sys.path.append("D:\\akshay\\script")
from conLibrary import libraryUI
reload(libraryUI)

ui=libraryUI.showUI()