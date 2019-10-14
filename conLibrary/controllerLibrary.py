from maya import cmds   # import maya commands
import os               # import os [note : for file path handling]
import json             # import json [note:to save maya file info(name, path) in json format]

USERAPPDIR = cmds.internalVar(userAppDir=True)                      # to get user application(project) directory
DIRECTORY = os.path.join(USERAPPDIR, 'controllerLibrary')           # create path controllerLibrary folder in application(project) directory



def createDirectory(directory=DIRECTORY):
    """
    This function is used to create control library directorary if it doesn't exists
    Args:
        directory(str):the directorary path to create


    """

    if not os.path.exists(directory):    # check control library directory if it doesn't exists
        os.mkdir(directory)              # create controlLibrary directory




class ControllerLibrary(dict):
    """
    this is main class for controllerLibrary for
    def save : to save model along with screenshot with info[name, path] of json format (info file) in the controlLibrary directory
    def find : to get all maya file and info file in the controlLibrary directory
    def load : to import the model from controlLibrary with given name
    def saveScreenshot: to save the screenshot of selected model and save with name of that item
    """
    def save(self, name, directory=DIRECTORY, screenshot = True, **info):
        """
        to save the screenshot and model to the control library directory
        Args:
            name:(str) name of the item to be svaed
            directory: (str) path of the coontrolLibrary directory
            screenshot: (bool) to save screenshot
            **info:(to send extra arguments to json file of name amd path)

        """
        #  call createDirectory check control library directory is created
        createDirectory(directory)

        path=os.path.join(directory, '%s.ma' %name)              # append save model name as maya file in the directory
        infoFile=os.path.join(directory, '%s.json' % name)       # save info file in json format [name, path, screenshotpath]
        info['name']=name                                        # save model name in json(info) file with key 'name'
        info['path']=path                                        # save path of file in json(info) file with key 'path'

        cmds.file(rename=path)                                   # save model as new file with given path

        '''
        if  any selection is true then save only selected model 
        else  save whole scene
        '''
        if cmds.ls(sl=True):
            cmds.file(type='mayaAscii', exportSelected=True)
        else:
            cmds.file(save=True, type='mayaAscii', force=True)


        if screenshot:
            info['screenshot'] = self.saveScreenshot(name,directory)    # save screenshot path in the json(info) file


        with open(infoFile, 'w' ) as f:         # create json(info) file as write permission
            json.dump(info,f, indent=4)         # write info in the file with indentation of 4

        self[name] = info                       # save info to name as dictionary for accessing throughout the class



    def find(self, directory=DIRECTORY):
        """
         to find the maya items in the given directory
        Args:
            directory: (str)(path) of control library directory

        Returns: contains maya files  can be used as themapping items of python inbuilt command

        """


        self.clear()    # clear all found item before execution useful during Refresh
        if not os.path.exists(directory):    # check controlLibrary path exists if not then return doing nothing
            return

        files = os.listdir(directory)    # list all files in the directory
        mayaFiles = [f for f in files if f.endswith('.ma')]     # filter maya files from all files [note : this is list comphersion]


        """
        mayaFiles = [f for f in files if f.endswith('.ma')]

        above single line code is list comperhension

        mayafiles=[]
        for f in files:
            if f.endswith('.ma'):
                mayaFiles.append(f)                
        """


        for ma in mayaFiles:    # for maya file in all maya file
            name, ext = os.path.splitext(ma)   # extract only name without .ma
            path = os.path.join(directory,ma)    # get path of maya file with ext

            infoFile = '%s.json' % name         # to get the json(info) file of that maya file
            if infoFile in files:               # if info file found in the control library directory
                infoFile = os.path.join(directory, infoFile)        # make path of info file

                with open(infoFile, 'r') as f:              # open info file as read
                    info = json.load(f)                     # get details from json into info dictnoary
            else:
                info={}                                     # else info will be empty dictonary

            screenshot='%s.jpg'% name           # assign name of screenshot to be saved
            if screenshot in files:             # if screenshot found in control library directory
                info['screenshot']= os.path.join(directory, screenshot)         # save screeshot path to info

            info['name']=name           # save name of the model to info
            info['path']=path           # save path of file to info

            self[name] = info           # save info in dictionary of item for mapping


    def load(self, name):
        """
         to import model into the scene
        Args:
            name: name of the model

        Returns:

        """
        path = self[name]['path']       # get the value(path) with key: 'path' from dictionary name
        cmds.file(path, i=True, usingNamespaces=False)          # import file from path without namespaces



    def saveScreenshot(self, name, directory=DIRECTORY):
        """
         to save screenshot of the model
        Args:
            name: (str) name of the model
            directory: (str) (path) path of the control library

        Returns:
            path: path of image of the screenshot

        """


        path = os.path.join(directory, '%s.jpg' % name)     # to get the path of the screenshot

        cmds.viewFit()      # view fit from maya commands of selected object i.e click 'f' key
        cmds.setAttr('defaultRenderGlobals.imageFormat', 8)     # set maya render to image format of jpg

        cmds.playblast(completeFilename=path, forceOverwrite=True, format='image', width=200, height=200,
                       showOrnaments=False, startTime=1, endTime=1, viewer=False)       # get playblast of 1 frame and save in given path

            # return the path of the image
        return path



    def delItem (self, name,directory=DIRECTORY):
        """
         to delete the item from library
        Args:
            name: name of the model

        Returns:

        """

        path = self[name]['path']   # get the value(path) with key: 'path' from dictionary name
        winPath=path.replace("/","\\")
        screenshotPath =self [name]['screenshot']
        winScreenshotPath=screenshotPath.replace("/","\\")
        jsonPath=directory+'\\%s.json'% name
        winJsonPath=jsonPath.replace("/","\\")

        os.remove(winPath)
        os.remove(winJsonPath)
        os.remove(winScreenshotPath)

        #self.find()

        '''
        print name
        print winPath
        print winScreenshotPath
        print winJsonPath
        print directory
        '''
