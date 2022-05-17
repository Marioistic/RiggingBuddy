import maya.cmds as cmds
from importlib import reload
import locators
import joints

# Reloads all supporting files each time script is run
# Necessary or you would need to restart Maya after any updates
locators = reload(locators)
joints = reload(joints)


class RiggingBuddy():
    def __init__(self):
        self.buildUI()
        
        
    def buildUI(self):
        cmds.window("Rigging Buddy 1.0")
        cmds.rowColumnLayout(numberOfColumns=2)
        cmds.separator(style="none")
        
        cmds.separator(h = 10, st = "none")
        locators.createFields()
        cmds.separator(h = 10, st = "none")
        
        cmds.separator(h = 10, st = "none")
        cmds.button(label="Create Locators", width=200, command="locators.createLocators()")
        cmds.button(label="Mirror L->R", width=200, command="locators.mirrorLocators()") 
        cmds.separator(h = 10, st = "none")
        
        cmds.separator(style="none")
        cmds.button(label="Create Joints", width=200, command="joints.createJoints()")
        
        cmds.separator(height=10, style="none")
        cmds.button(label="Delete Locators", width=200, command="locators.deleteLocators()")
        cmds.button(label="Delete Joints", width=200, command="joints.deleteJoints()")
        cmds.separator(height=10, style="none")
        
        cmds.button(label="Delete All", width=200, command=self.deleteAll)
        
        cmds.showWindow()
        
        
    def deleteAll(self, void):
        cmds.delete("opm*")
        cmds.delete("JNT_*")
        

RiggingBuddy()











                      

