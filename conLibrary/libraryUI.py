import controllerLibrary                        # import controllerLibrary.py
reload(controllerLibrary)                       # reload controllerLibrary.py
from PySide2 import QtWidgets, QtCore, QtGui    # import QtWidgets, QtCore, QtGui from PySide2
import maya.cmds as cmds                        # import maya commands library
import pprint                                   # import pprint[note: pprint= pretty print]

class ControllerLibraryUI(QtWidgets.QDialog):
    """
     The ControllerlibraryUI is a dialog used to create, save and import models
    """

    def __init__(self):
        super(ControllerLibraryUI, self).__init__()             # to change QtWidgets.QDialog constructor
        self.setWindowTitle('Object Library')                    # set window Title
        self.library =controllerLibrary.ControllerLibrary()     # make object of ControllerLibrary class form controllerLibrary.py
        self.buildUI()                                          # call buildUI to create layout
        self.populate()                                         # show items in control library

    def buildUI(self):
        """
        buildUI is used to create layout of for controllerLibrary


        """
        layout = QtWidgets.QVBoxLayout(self)     # QtWidgets.QVBoxLayout: to create the verticle layout for savae widget

        saveWidget = QtWidgets.QWidget()    # new widget for the save text feild and the save button
        saveLayout = QtWidgets.QHBoxLayout(saveWidget)    # arrange savewidget as horizontal layout
        layout.addWidget(saveWidget)   # add savewidget to layout

        self.saveNameField = QtWidgets.QLineEdit()   # create save name text feild
        saveLayout.addWidget(self.saveNameField)   # add text feild to save layout

        saveBtn = QtWidgets.QPushButton('Save')   # create save button
        saveBtn.clicked.connect(self.save)   # execute save function(def save) on click
        saveLayout.addWidget(saveBtn)   # add  save button to save layout

        iconSize = 80    # to display the icon size of controller
        buffer = 15    # to add margin of icon
        self.listWidget= QtWidgets.QListWidget()    # to create the new widget(listWidget) to display the available controller
        self.listWidget.setViewMode(QtWidgets.QListWidget.IconMode)   # to see the controller or model in the icon mode instad of default list mode
        self.listWidget.setIconSize(QtCore.QSize(iconSize,iconSize))   # to set the icon thumbnail size
        self.listWidget.setResizeMode(QtWidgets.QListWidget.Adjust)   # to change arrangment of icon upon window resize
        self.listWidget.setGridSize(QtCore.QSize(iconSize+buffer,iconSize+buffer))   # to set margin to icon
        layout.addWidget(self.listWidget)    # to add listwidget to layout


        # create import,refresh and close ,deleteitem
        btnWidget = QtWidgets.QWidget()    # create new button widget
        btnLayout = QtWidgets.QHBoxLayout(btnWidget)   # create button layout for button widget in horizontal way
        layout.addWidget(btnWidget)   # add button widget to main layout

        importBtn = QtWidgets.QPushButton('Import')   # to create import button
        importBtn.clicked.connect(self.load)    # to execute load function when clicked      importBtn.clicked.connect(self.load)
        btnLayout.addWidget(importBtn)    # add import button to button layout

        refreshBtn = QtWidgets.QPushButton('Refresh')    # create refresh button
        refreshBtn.clicked.connect(self.populate)    # to execute populate function when clicked
        btnLayout.addWidget(refreshBtn)    # add refresh button to button layout

        closeBtn = QtWidgets.QPushButton('close')    # create close button
        # close function is inherited from QtWideget.QDialog library
        closeBtn.clicked.connect(self.close)    # to execute the close function on click
        btnLayout.addWidget(closeBtn)    # add close button to button layout

        delBtn = QtWidgets.QPushButton('Delete')
        delBtn.clicked.connect(self.dele)
        btnLayout.addWidget(delBtn)

    def populate(self):
        """

        to display the maya files or controller available in controllibrary directory

        """
        self.listWidget.clear()    # to clear the list every time we click refresh button
        # to find the available controller in controllibrary directory the fuction is defined in the controllerLibrary.py
        self.library.find()

        # to get the controller in lirary [note: items is a python inbuilt mapping function]
        for name, info in self.library.items():
            item = QtWidgets.QListWidgetItem(name)   # get the name of item
            self.listWidget.addItem(item)   # add item to listWdiget to display in listLayout

            # to get the path of screenshot
            screenshot = info.get('screenshot')
            if screenshot:    # check weather screenshot exists
                icon = QtGui.QIcon(screenshot)    # make screenshot as icon
                item.setIcon(icon)    # set icon to item

            item.setToolTip(pprint.pformat(info))   # to display tooltip on hover of all info availbale in json(info file) for that item

    def load(self):
        """

        to load or import selected controller from library into the scene

        """
        currentItem = self.listWidget.currentItem()    # to select an item from listwidget or control libray

        if not currentItem:    # if no item is selected in control library then return without doing anything
            return

        name= currentItem.text()   # to get curent selected item in text format
        self.library.load(name)   # to import current item into the scene [note: this load function is from controllerLibrary]


    def save(self):
        """

        this function is used to save selected object in control libraray with given name

        """
        name = self.saveNameField.text()  # to get the name given in the text feild
        if not name.strip():  # to check weather name is not empty
            cmds.warning("You must give name of object")  # to display warning on if name is empty and return without doing anything
            return

        self.library.save(name)  # save the selected object with given name in control library [note: save function is defined in the controllerLibrary.py]
        self.populate()   # to display saved item in listwidget or in list layout
        self.saveNameField.setText('')   # after save and display set the saveNameText feild to empty string

    def dele(self):
        currentItem = self.listWidget.currentItem()
        if not currentItem:    # if no item is selected in control library then return without doing anything
            print "select a object"
            return
        else:
            name = currentItem.text()
            self.library.delItem(name)
            self.populate()


def showUI():
    """

    this function used by maya to call the script or plugin

    """
    ui=ControllerLibraryUI()    # call ControllerLibraryUI class from the this file itself to creat layout
    ui.show()                   # to show ui (layout) of ControllerLibrary
    return ui                   # to return ui when called by maya
