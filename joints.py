import maya.cmds as cmds
from importlib import reload
import locators

locators = reload(locators)


# Function to create all joints for the rig
def createJoints():
    if cmds.objExists("JNT_GRP"):
        print("The joint group already exists!")
        return 0
    else:
        # Creates empty joint group
        jointGroup = cmds.group(empty=True, name="JNT_GRP")
        
    # Finds the location of all the finger locators
    allFingers = cmds.ls("LOC_L_finger_*_0")
    
    # Creates spine by finding LOC_root and using that to find all other spine locators
    root = cmds.ls("LOC_root")
    allSpines = cmds.ls("LOC_spine_*", type="locator")
    spine = cmds.listRelatives(*allSpines, parent=True, fullPath=True)
    
    # Creates all spine joints including root
    for i, s in enumerate(spine):
        # This is a special case since the root joint has no parent and must be handled seperately
        if i == 0:
            # Creates a joint name variable to make the creation process easier to iterate
            # The joint names are determined based upon the allSpines and spine variables above
            jointAName = "JNT_root"
            jointBName = "JNT_spine_" + str(i)
            
            # Creates the joints using a similar setup to the names for ease of iteration
            jointA = cmds.createNode("joint", name=jointAName)
            jointB = cmds.createNode("joint", name=jointBName, parent=jointA)
            
            # Finds the appropiate locator and stores it as a variable
            locatorA = "LOC_root"
            locatorB = "LOC_spine_" + str(i)
            
            # Creates the transform node that will be used to store the rest position and rotation
            rotationA = cmds.createNode("transform", name=jointAName + "_REST", parent="opmStorage_GRP")
            rotationB = cmds.createNode("transform", name=jointBName + "_REST", parent="opmStorage_GRP")
            
            # These nodes do all the necessary math for the OPM setup to work properly
            aim = cmds.createNode("aimMatrix")
            mult = cmds.createNode("multMatrix")
            
            # This is where the magic happens! Through these connections in the node editor,
            # the joint is able to stay zeroed out and oriented properly while passing off
            # all of the transformation values to the rest group made above
            cmds.connectAttr(locatorA + ".worldMatrix", aim + ".inputMatrix", force=True)
            cmds.connectAttr(locatorB + ".worldMatrix", aim + ".primaryTargetMatrix", force=True)
            cmds.connectAttr(locatorB + ".worldMatrix", rotationB + ".offsetParentMatrix", force=True)
            cmds.connectAttr(rotationB + ".worldMatrix", mult + ".matrixIn[0]", force=True)
            cmds.connectAttr(rotationA + ".worldInverseMatrix", mult + ".matrixIn[1]", force=True)

            cmds.connectAttr(aim + ".outputMatrix", rotationA + ".offsetParentMatrix", force=True)
            # This line is ONLY needed for the root joint of the skeleton
            cmds.connectAttr(rotationA + ".worldMatrix", jointA + ".offsetParentMatrix", force=True)

            cmds.connectAttr(mult + ".matrixSum", jointB + ".offsetParentMatrix", force=True)
        # All other spine joints can be created without any special situation to account for
        else:
            # I use B and C instead of A and B to avoid confusion with the above if statement
            # Joint B is the same joint used above, but now it is the parent instead of the child.
            # For all iterations Joint B will always be the parent of Joint C
            jointBName = "JNT_spine_" + str(i - 1)
            jointCName = "JNT_spine_" + str(i)
            
            # Joint B alredy exists so the variable is updated by always storing the joint that is at i - 1
            jointB = "JNT_spine_" + str(i - 1)
            jointC = cmds.createNode("joint", name=jointCName, parent=jointB)
            
            # The locators are always at position i and i - 1
            locatorB = "LOC_spine_" + str(i - 1)
            locatorC = "LOC_spine_" + str(i)
            
            # Rest B already exists so the variable is updated by always storing the joint that is at i - 1
            rotationB = "JNT_spine_" + str(i - 1) + "_REST"
            rotationC = cmds.createNode("transform", name=jointCName + "_REST", parent="opmStorage_GRP")
            
            # You always need a new version of each of these nodes each iteration
            aim = cmds.createNode("aimMatrix")
            mult = cmds.createNode("multMatrix")
            
            # This is where the magic happens! Through these connections in the node editor,
            # the joint is able to stay zeroed out and oriented properly while passing off
            # all of the transformation values to the rest group made above
            cmds.connectAttr(locatorB + ".worldMatrix", aim + ".inputMatrix", force=True)
            cmds.connectAttr(locatorC + ".worldMatrix", aim + ".primaryTargetMatrix", force=True)
            cmds.connectAttr(locatorC + ".worldMatrix", rotationC + ".offsetParentMatrix", force=True)
            cmds.connectAttr(rotationC + ".worldMatrix", mult + ".matrixIn[0]", force=True)
            cmds.connectAttr(rotationB + ".parentInverseMatrix", mult + ".matrixIn[1]", force=True)

            cmds.connectAttr(aim + ".outputMatrix", rotationB + ".offsetParentMatrix", force=True)

            cmds.connectAttr(mult + ".matrixSum", jointC + ".offsetParentMatrix", force=True)
            
        '''   
            # This is a special case since the root joint has no parent and must be handled seperately
        if i == 0:
            # Creates a joint name variable to make the creation process easier to iterate
            # The joint names are determined based upon the allSpines and spine variables above
            controlAName = "CTL_root"
            controlBName = "CTL_spine_" + str(i)
            
            # Creates the joints using a similar setup to the names for ease of iteration
            controlA = cmds.circle(name=controlAName)
            controlB = cmds.circle(name=controlBName)
            cmds.parent(controlB, controlA)
            
            
            cmds.connectAttr(rotationA + ".worldMatrix", controlA + ".offsetParentMatrix", force=True)
            cmds.connectAttr(mult + ".matrixSum", controlB + ".offsetParentMatrix")
        '''   
            
            
        
    # Calls all the helper function to actually create the joints
    createHeadJoints(len(allSpines))
    createLegJoints()
    createArmJoints(len(allSpines))
    createFingerJoints(len(allFingers))
    

# Creates all the head joints including the eyes and jaw
def createHeadJoints(spineAmount):
    # Find all the head locators
    allHead = cmds.ls("LOC_C_head_*", type="locator")
    head = cmds.listRelatives(*allHead, parent=True, fullPath=True)
    
    # Loop through all head locators and create joints
    for i, h in enumerate(head):
        # This is a special case since the neck joint is parented to the last spine joint
        if i == 0:
            # Creates a joint name variable to make the creation process easier to iterate
            # The joint names are determined based upon the allHead and head variables above
            jointAName = "JNT_spine_" + str(spineAmount - 1)
            jointBName = "JNT_C_head_" + str(i)
            
            # Creates the joints using a similar setup to the names for ease of iteration
            # Note that joint A already exists
            jointA = "JNT_spine_" + str(spineAmount - 1)
            jointB = cmds.createNode("joint", name=jointBName, parent=jointA)
            
            # Finds the appropiate locator and stores it as a variable
            locatorA = "LOC_spine_" + str(spineAmount - 1)
            locatorB = "LOC_C_head_" + str(i)
            
            # Creates the transform node that will be used to store the rest position and rotation
            # Note that rotation A already exists. It only needs to be created with the first joint
            # It will already exist for all other joints
            rotationA = "JNT_spine_" + str(spineAmount - 1) + "_REST"
            rotationB = cmds.createNode("transform", name=jointBName + "_REST", parent="opmStorage_GRP")
            
            # These nodes do all the necessary math for the OPM setup to work properly
            aim = cmds.createNode("aimMatrix")
            mult = cmds.createNode("multMatrix")
            
            # This is where the magic happens! Through these connections in the node editor,
            # the joint is able to stay zeroed out and oriented properly while passing off
            # all of the transformation values to the rest group made above
            cmds.connectAttr(locatorA + ".worldMatrix", aim + ".inputMatrix", force=True)
            cmds.connectAttr(locatorB + ".worldMatrix", aim + ".primaryTargetMatrix", force=True)
            cmds.connectAttr(locatorB + ".worldMatrix", rotationB + ".offsetParentMatrix", force=True)
            cmds.connectAttr(rotationB + ".worldMatrix", mult + ".matrixIn[0]", force=True)
            # Note that rotation A now uses its parentInverseMatrix instead of the worldInverseMatrix
            # This is because it has a parent that is NOT the world
            cmds.connectAttr(rotationA + ".parentInverseMatrix", mult + ".matrixIn[1]", force=True)

            cmds.connectAttr(aim + ".outputMatrix", rotationA + ".offsetParentMatrix", force=True)

            cmds.connectAttr(mult + ".matrixSum", jointB + ".offsetParentMatrix", force=True)
        # All other head joints can be created without any special situation to account for
        else:
            # I use B and C instead of A and B to avoid confusion with the above if statement
            # Joint B is the same joint used above, but now it is the parent instead of the child.
            # For all iterations Joint B will always be the parent of Joint C
            jointBName = "JNT_C_head_" + str(i - 1)
            jointCName = "JNT_C_head_" + str(i)
            
            # Joint B alredy exists so the variable is updated by always storing the joint that is at i - 1
            jointB = "JNT_C_head_" + str(i - 1)
            jointC = cmds.createNode("joint", name=jointCName, parent=jointB)
            
            # The locators are always at position i and i - 1
            locatorB = "LOC_C_head_" + str(i - 1)
            locatorC = "LOC_C_head_" + str(i)
            
            # Rest B already exists so the variable is updated by always storing the joint that is at i - 1
            rotationB = "JNT_C_head_" + str(i - 1) + "_REST"
            rotationC = cmds.createNode("transform", name=jointCName + "_REST", parent="opmStorage_GRP")
            
            # You always need a new version of each of these nodes each iteration
            aim = cmds.createNode("aimMatrix")
            mult = cmds.createNode("multMatrix")
            
            # This is where the magic happens! Through these connections in the node editor,
            # the joint is able to stay zeroed out and oriented properly while passing off
            # all of the transformation values to the rest group made above
            cmds.connectAttr(locatorB + ".worldMatrix", aim + ".inputMatrix", force=True)
            cmds.connectAttr(locatorC + ".worldMatrix", aim + ".primaryTargetMatrix", force=True)
            cmds.connectAttr(locatorC + ".worldMatrix", rotationC + ".offsetParentMatrix", force=True)
            cmds.connectAttr(rotationC + ".worldMatrix", mult + ".matrixIn[0]", force=True)
            cmds.connectAttr(rotationB + ".parentInverseMatrix", mult + ".matrixIn[1]", force=True)

            cmds.connectAttr(aim + ".outputMatrix", rotationB + ".offsetParentMatrix", force=True)

            cmds.connectAttr(mult + ".matrixSum", jointC + ".offsetParentMatrix", force=True)
        
        
    # Calls helper functions to create the jaw and eyes
    createJawJoints()
    createEyeJoints()


# Creates the jaw joints
def createJawJoints():
    # Find all the jaw locators
    allJaw = cmds.ls("LOC_C_jaw_*", type="locator")
    jaw = cmds.listRelatives(*allJaw, parent=True, fullPath=True)
    
    # Loop through all jaw locators and create joints
    for i, j in enumerate(jaw):
        if i == 0:
            jointAName = "JNT_C_head_1" 
            jointBName = "JNT_C_jaw_" + str(i)
            
            jointA = "JNT_C_head_1"
            jointB = cmds.createNode("joint", name=jointBName, parent=jointA)
            
            locatorA = "LOC_C_head_1"
            locatorB = "LOC_C_jaw_" + str(i)
            
            rotationA = "JNT_C_head_1_REST"
            rotationB = cmds.createNode("transform", name=jointBName + "_REST", parent="opmStorage_GRP")
            
            aim = cmds.createNode("aimMatrix")
            mult = cmds.createNode("multMatrix")
            
            cmds.connectAttr(locatorA + ".worldMatrix", aim + ".inputMatrix", force=True)
            cmds.connectAttr(locatorB + ".worldMatrix", aim + ".primaryTargetMatrix", force=True)
            cmds.connectAttr(locatorB + ".worldMatrix", rotationB + ".offsetParentMatrix", force=True)
            cmds.connectAttr(rotationB + ".worldMatrix", mult + ".matrixIn[0]", force=True)
            cmds.connectAttr(rotationA + ".parentInverseMatrix", mult + ".matrixIn[1]", force=True)

            cmds.connectAttr(mult + ".matrixSum", jointB + ".offsetParentMatrix", force=True)
        else:
            jointBName = "JNT_C_jaw_" + str(i - 1)
            jointCName = "JNT_C_jaw_" + str(i)
            
            jointB = "JNT_C_jaw_" + str(i - 1)
            jointC = cmds.createNode("joint", name=jointCName, parent=jointB)
            
            locatorB = "LOC_C_jaw_" + str(i - 1)
            locatorC = "LOC_C_jaw_" + str(i)
            
            rotationB = "JNT_C_jaw_" + str(i - 1) + "_REST"
            rotationC = cmds.createNode("transform", name=jointCName + "_REST", parent="opmStorage_GRP")
            
            aim = cmds.createNode("aimMatrix")
            mult = cmds.createNode("multMatrix")
            
            cmds.connectAttr(locatorB + ".worldMatrix", aim + ".inputMatrix", force=True)
            cmds.connectAttr(locatorC + ".worldMatrix", aim + ".primaryTargetMatrix", force=True)
            cmds.connectAttr(locatorC + ".worldMatrix", rotationC + ".offsetParentMatrix", force=True)
            cmds.connectAttr(rotationC + ".worldMatrix", mult + ".matrixIn[0]", force=True)
            cmds.connectAttr(rotationB + ".parentInverseMatrix", mult + ".matrixIn[1]", force=True)

            cmds.connectAttr(aim + ".outputMatrix", rotationB + ".offsetParentMatrix", force=True)

            cmds.connectAttr(mult + ".matrixSum", jointC + ".offsetParentMatrix", force=True)


# Creates the eye joints
def createEyeJoints():
    ###########
    # Left Eye
    ###########
    # Find all the left eye locators
    allLeftEye = cmds.ls("LOC_L_eye_*", type="locator")
    leftEye = cmds.listRelatives(*allLeftEye, parent=True, fullPath=True)
    
    # Loop through left eye locators and create joints
    for i, L_eye in enumerate(leftEye):
        if i == 0:
            jointAName = "JNT_C_head_1" 
            jointBName = "JNT_L_eye_" + str(i)
            
            jointA = "JNT_C_head_1"
            jointB = cmds.createNode("joint", name=jointBName, parent=jointA)
            
            locatorA = "LOC_C_head_1"
            locatorB = "LOC_L_eye_" + str(i)
            
            rotationA = "JNT_C_head_1_REST"
            rotationB = cmds.createNode("transform", name=jointBName + "_REST", parent="opmStorage_GRP")
            
            aim = cmds.createNode("aimMatrix")
            mult = cmds.createNode("multMatrix")
            
            cmds.connectAttr(locatorA + ".worldMatrix", aim + ".inputMatrix", force=True)
            cmds.connectAttr(locatorB + ".worldMatrix", aim + ".primaryTargetMatrix", force=True)
            cmds.connectAttr(locatorB + ".worldMatrix", rotationB + ".offsetParentMatrix", force=True)
            cmds.connectAttr(rotationB + ".worldMatrix", mult + ".matrixIn[0]", force=True)
            cmds.connectAttr(rotationA + ".parentInverseMatrix", mult + ".matrixIn[1]", force=True)

            cmds.connectAttr(mult + ".matrixSum", jointB + ".offsetParentMatrix", force=True)
        else:
            jointBName = "JNT_L_eye_" + str(i - 1)
            jointCName = "JNT_L_eye_" + str(i)
            
            jointB = "JNT_L_eye_" + str(i - 1)
            jointC = cmds.createNode("joint", name=jointCName, parent=jointB)
            
            locatorB = "LOC_L_eye_" + str(i - 1)
            locatorC = "LOC_L_eye_" + str(i)
            
            rotationB = "JNT_L_eye_" + str(i - 1) + "_REST"
            rotationC = cmds.createNode("transform", name=jointCName + "_REST", parent="opmStorage_GRP")
            
            aim = cmds.createNode("aimMatrix")
            mult = cmds.createNode("multMatrix")
            
            cmds.connectAttr(locatorB + ".worldMatrix", aim + ".inputMatrix", force=True)
            cmds.connectAttr(locatorC + ".worldMatrix", aim + ".primaryTargetMatrix", force=True)
            cmds.connectAttr(locatorC + ".worldMatrix", rotationC + ".offsetParentMatrix", force=True)
            cmds.connectAttr(rotationC + ".worldMatrix", mult + ".matrixIn[0]", force=True)
            cmds.connectAttr(rotationB + ".parentInverseMatrix", mult + ".matrixIn[1]", force=True)

            cmds.connectAttr(aim + ".outputMatrix", rotationB + ".offsetParentMatrix", force=True)

            cmds.connectAttr(mult + ".matrixSum", jointC + ".offsetParentMatrix", force=True)
        
    ############
    # Right Eye
    ############
    # Find all the right eye locators
    allRightEye = cmds.ls("LOC_R_eye_*", type="locator")
    rightEye = cmds.listRelatives(*allRightEye, parent=True, fullPath=True)
    
    # Loop through right eye locators and create joints
    for i, R_eye in enumerate(rightEye):
        if i == 0:
            jointAName = "JNT_C_head_1" 
            jointBName = "JNT_R_eye_" + str(i)
            
            jointA = "JNT_C_head_1"
            jointB = cmds.createNode("joint", name=jointBName, parent=jointA)
            
            locatorA = "LOC_C_head_1"
            locatorB = "LOC_R_eye_" + str(i)
            
            rotationA = "JNT_C_head_1_REST"
            rotationB = cmds.createNode("transform", name=jointBName + "_REST", parent="opmStorage_GRP")
            
            aim = cmds.createNode("aimMatrix")
            mult = cmds.createNode("multMatrix")
            
            cmds.connectAttr(locatorA + ".worldMatrix", aim + ".inputMatrix", force=True)
            cmds.connectAttr(locatorB + ".worldMatrix", aim + ".primaryTargetMatrix", force=True)
            cmds.connectAttr(locatorB + ".worldMatrix", rotationB + ".offsetParentMatrix", force=True)
            cmds.connectAttr(rotationB + ".worldMatrix", mult + ".matrixIn[0]", force=True)
            cmds.connectAttr(rotationA + ".parentInverseMatrix", mult + ".matrixIn[1]", force=True)
            
            cmds.connectAttr(aim + ".outputMatrix", rotationB + ".offsetParentMatrix", force=True)

            cmds.connectAttr(mult + ".matrixSum", jointB + ".offsetParentMatrix", force=True)
        else:
            jointBName = "JNT_R_eye_" + str(i - 1)
            jointCName = "JNT_R_eye_" + str(i)
            
            jointB = "JNT_R_eye_" + str(i - 1)
            jointC = cmds.createNode("joint", name=jointCName, parent=jointB)
            
            locatorB = "LOC_R_eye_" + str(i - 1)
            locatorC = "LOC_R_eye_" + str(i)
            
            rotationB = "JNT_R_eye_" + str(i - 1) + "_REST"
            rotationC = cmds.createNode("transform", name=jointCName + "_REST", parent="opmStorage_GRP")
            
            aim = cmds.createNode("aimMatrix")
            mult = cmds.createNode("multMatrix")
            
            cmds.connectAttr(locatorB + ".worldMatrix", aim + ".inputMatrix", force=True)
            cmds.connectAttr(locatorC + ".worldMatrix", aim + ".primaryTargetMatrix", force=True)
            cmds.connectAttr(locatorC + ".worldMatrix", rotationC + ".offsetParentMatrix", force=True)
            cmds.connectAttr(rotationC + ".worldMatrix", mult + ".matrixIn[0]", force=True)
            cmds.connectAttr(rotationB + ".parentInverseMatrix", mult + ".matrixIn[1]", force=True)

            cmds.connectAttr(aim + ".outputMatrix", rotationB + ".offsetParentMatrix", force=True)

            cmds.connectAttr(mult + ".matrixSum", jointC + ".offsetParentMatrix", force=True)
        

# Creates all the leg joints
def createLegJoints():
    ###########
    # Left Leg
    ###########
    # Finds all the left leg locators
    allLeftLeg = cmds.ls("LOC_L_leg_*", type="locator")
    leftLeg = cmds.listRelatives(*allLeftLeg, parent=True, fullPath=True)
    
    # Loops through all left leg locators to create joints
    for i, L_leg in enumerate(leftLeg):
        if i == 0:
            jointAName = "JNT_root"
            jointBName = "JNT_L_leg_" + str(i)
            
            jointA = "JNT_root"
            jointB = cmds.createNode("joint", name=jointBName, parent=jointA)
            
            locatorA = "LOC_root"
            locatorB = "LOC_L_leg_" + str(i)
            
            rotationA = "JNT_root_REST"
            rotationB = cmds.createNode("transform", name=jointBName + "_REST", parent="opmStorage_GRP")
            
            aim = cmds.createNode("aimMatrix")
            mult = cmds.createNode("multMatrix")
            
            cmds.connectAttr(locatorA + ".worldMatrix", aim + ".inputMatrix", force=True)
            cmds.connectAttr(locatorB + ".worldMatrix", aim + ".primaryTargetMatrix", force=True)
            cmds.connectAttr(locatorB + ".worldMatrix", rotationB + ".offsetParentMatrix", force=True)
            cmds.connectAttr(rotationB + ".worldMatrix", mult + ".matrixIn[0]", force=True)
            cmds.connectAttr(rotationA + ".parentInverseMatrix", mult + ".matrixIn[1]", force=True)

            cmds.connectAttr(mult + ".matrixSum", jointB + ".offsetParentMatrix", force=True)
        else:
            jointBName = "JNT_L_leg_" + str(i - 1)
            jointCName = "JNT_L_leg_" + str(i)
            
            jointB = "JNT_L_leg_" + str(i - 1)
            jointC = cmds.createNode("joint", name=jointCName, parent=jointB)
            
            locatorB = "LOC_L_leg_" + str(i - 1)
            locatorC = "LOC_L_leg_" + str(i)
            
            rotationB = "JNT_L_leg_" + str(i - 1) + "_REST"
            rotationC = cmds.createNode("transform", name=jointCName + "_REST", parent="opmStorage_GRP")
            
            aim = cmds.createNode("aimMatrix")
            mult = cmds.createNode("multMatrix")
            
            cmds.connectAttr(locatorB + ".worldMatrix", aim + ".inputMatrix", force=True)
            cmds.connectAttr(locatorC + ".worldMatrix", aim + ".primaryTargetMatrix", force=True)
            cmds.connectAttr(locatorC + ".worldMatrix", rotationC + ".offsetParentMatrix", force=True)
            cmds.connectAttr(rotationC + ".worldMatrix", mult + ".matrixIn[0]", force=True)
            cmds.connectAttr(rotationB + ".parentInverseMatrix", mult + ".matrixIn[1]", force=True)

            cmds.connectAttr(aim + ".outputMatrix", rotationB + ".offsetParentMatrix", force=True)

            cmds.connectAttr(mult + ".matrixSum", jointC + ".offsetParentMatrix", force=True)
    ############
    # Right Leg
    ############
    # Finds all the right leg locators
    allRightLeg = cmds.ls("LOC_R_leg_*", type="locator")
    rightLeg = cmds.listRelatives(*allRightLeg, parent=True, fullPath=True)
    
    # Loops through all right leg locators to create joints
    for i, R_leg in enumerate(rightLeg):
        if i == 0:
            jointAName = "JNT_root"
            jointBName = "JNT_R_leg_" + str(i)
            
            jointA = "JNT_root"
            jointB = cmds.createNode("joint", name=jointBName, parent=jointA)
            
            locatorA = "LOC_root"
            locatorB = "LOC_R_leg_" + str(i)
            
            rotationA = "JNT_root_REST"
            rotationB = cmds.createNode("transform", name=jointBName + "_REST", parent="opmStorage_GRP")
            
            aim = cmds.createNode("aimMatrix")
            mult = cmds.createNode("multMatrix")
            
            cmds.connectAttr(locatorA + ".worldMatrix", aim + ".inputMatrix", force=True)
            cmds.connectAttr(locatorB + ".worldMatrix", aim + ".primaryTargetMatrix", force=True)
            cmds.connectAttr(locatorB + ".worldMatrix", rotationB + ".offsetParentMatrix", force=True)
            cmds.connectAttr(rotationB + ".worldMatrix", mult + ".matrixIn[0]", force=True)
            cmds.connectAttr(rotationA + ".parentInverseMatrix", mult + ".matrixIn[1]", force=True)

            cmds.connectAttr(mult + ".matrixSum", jointB + ".offsetParentMatrix", force=True)
        else:
            jointBName = "JNT_R_leg_" + str(i - 1)
            jointCName = "JNT_R_leg_" + str(i)
            
            jointB = "JNT_R_leg_" + str(i - 1)
            jointC = cmds.createNode("joint", name=jointCName, parent=jointB)
            
            locatorB = "LOC_R_leg_" + str(i - 1)
            locatorC = "LOC_R_leg_" + str(i)
            
            rotationB = "JNT_R_leg_" + str(i - 1) + "_REST"
            rotationC = cmds.createNode("transform", name=jointCName + "_REST", parent="opmStorage_GRP")
            
            aim = cmds.createNode("aimMatrix")
            mult = cmds.createNode("multMatrix")
            
            cmds.connectAttr(locatorB + ".worldMatrix", aim + ".inputMatrix", force=True)
            cmds.connectAttr(locatorC + ".worldMatrix", aim + ".primaryTargetMatrix", force=True)
            cmds.connectAttr(locatorC + ".worldMatrix", rotationC + ".offsetParentMatrix", force=True)
            cmds.connectAttr(rotationC + ".worldMatrix", mult + ".matrixIn[0]", force=True)
            cmds.connectAttr(rotationB + ".parentInverseMatrix", mult + ".matrixIn[1]", force=True)

            cmds.connectAttr(aim + ".outputMatrix", rotationB + ".offsetParentMatrix", force=True)

            cmds.connectAttr(mult + ".matrixSum", jointC + ".offsetParentMatrix", force=True)
    
    
# Creates all the arm joints
def createArmJoints(spineAmount):
    ###########
    # Left Arm
    ###########
    # Finds all of the left arm locators
    allLeftArm = cmds.ls("LOC_L_arm_*", type="locator")
    leftArm = cmds.listRelatives(*allLeftArm, parent=True, fullPath=True)
   
    # Loops through all left arm locators to create joints
    for i, L_arm in enumerate(leftArm):
        if i == 0:
            jointAName = "JNT_spine_" + str(spineAmount - 1)
            jointBName = "JNT_L_arm_" + str(i)
            
            jointA = "JNT_spine_" + str(spineAmount - 1)
            jointB = cmds.createNode("joint", name=jointBName, parent=jointA)
            
            locatorA = "LOC_spine_" + str(spineAmount - 1)
            locatorB = "LOC_L_leg_" + str(i)
            
            rotationA = "JNT_spine_" + str(spineAmount - 1) + "_REST"
            rotationB = cmds.createNode("transform", name=jointBName + "_REST", parent="opmStorage_GRP")
            
            aim = cmds.createNode("aimMatrix")
            mult = cmds.createNode("multMatrix")
            
            cmds.connectAttr(locatorA + ".worldMatrix", aim + ".inputMatrix", force=True)
            cmds.connectAttr(locatorB + ".worldMatrix", aim + ".primaryTargetMatrix", force=True)
            cmds.connectAttr(locatorB + ".worldMatrix", rotationB + ".offsetParentMatrix", force=True)
            cmds.connectAttr(rotationB + ".worldMatrix", mult + ".matrixIn[0]", force=True)
            cmds.connectAttr(rotationA + ".parentInverseMatrix", mult + ".matrixIn[1]", force=True)

            cmds.connectAttr(mult + ".matrixSum", jointB + ".offsetParentMatrix", force=True)
        else:
            jointBName = "JNT_L_arm_" + str(i - 1)
            jointCName = "JNT_L_arm_" + str(i)
            
            jointB = "JNT_L_arm_" + str(i - 1)
            jointC = cmds.createNode("joint", name=jointCName, parent=jointB)
            
            locatorB = "LOC_L_arm_" + str(i - 1)
            locatorC = "LOC_L_arm_" + str(i)
            
            rotationB = "JNT_L_arm_" + str(i - 1) + "_REST"
            rotationC = cmds.createNode("transform", name=jointCName + "_REST", parent="opmStorage_GRP")
            
            aim = cmds.createNode("aimMatrix")
            mult = cmds.createNode("multMatrix")
            
            cmds.connectAttr(locatorB + ".worldMatrix", aim + ".inputMatrix", force=True)
            cmds.connectAttr(locatorC + ".worldMatrix", aim + ".primaryTargetMatrix", force=True)
            cmds.connectAttr(locatorC + ".worldMatrix", rotationC + ".offsetParentMatrix", force=True)
            cmds.connectAttr(rotationC + ".worldMatrix", mult + ".matrixIn[0]", force=True)
            cmds.connectAttr(rotationB + ".parentInverseMatrix", mult + ".matrixIn[1]", force=True)

            cmds.connectAttr(aim + ".outputMatrix", rotationB + ".offsetParentMatrix", force=True)

            cmds.connectAttr(mult + ".matrixSum", jointC + ".offsetParentMatrix", force=True)
    ###########
    # Right Arm
    ###########
    # Finds all of the right arm locators
    allRightArm = cmds.ls("LOC_R_arm_*", type="locator")
    rightArm = cmds.listRelatives(*allRightArm, parent=True, fullPath=True)
    
    # Loops through all right arm locators to create joints
    for i, R_arm in enumerate(rightArm):
        if i == 0:
            jointAName = "JNT_spine_" + str(spineAmount - 1)
            jointBName = "JNT_R_arm_" + str(i)
            
            jointA = "JNT_spine_" + str(spineAmount - 1)
            jointB = cmds.createNode("joint", name=jointBName, parent=jointA)
            
            locatorA = "LOC_spine_" + str(spineAmount - 1)
            locatorB = "LOC_R_leg_" + str(i)
            
            rotationA = "JNT_spine_" + str(spineAmount - 1) + "_REST"
            rotationB = cmds.createNode("transform", name=jointBName + "_REST", parent="opmStorage_GRP")
            
            aim = cmds.createNode("aimMatrix")
            mult = cmds.createNode("multMatrix")
            
            cmds.connectAttr(locatorA + ".worldMatrix", aim + ".inputMatrix", force=True)
            cmds.connectAttr(locatorB + ".worldMatrix", aim + ".primaryTargetMatrix", force=True)
            cmds.connectAttr(locatorB + ".worldMatrix", rotationB + ".offsetParentMatrix", force=True)
            cmds.connectAttr(rotationB + ".worldMatrix", mult + ".matrixIn[0]", force=True)
            cmds.connectAttr(rotationA + ".parentInverseMatrix", mult + ".matrixIn[1]", force=True)

            cmds.connectAttr(mult + ".matrixSum", jointB + ".offsetParentMatrix", force=True)
        else:
            jointBName = "JNT_R_arm_" + str(i - 1)
            jointCName = "JNT_R_arm_" + str(i)
            
            jointB = "JNT_R_arm_" + str(i - 1)
            jointC = cmds.createNode("joint", name=jointCName, parent=jointB)
            
            locatorB = "LOC_R_arm_" + str(i - 1)
            locatorC = "LOC_R_arm_" + str(i)
            
            rotationB = "JNT_R_arm_" + str(i - 1) + "_REST"
            rotationC = cmds.createNode("transform", name=jointCName + "_REST", parent="opmStorage_GRP")
            
            aim = cmds.createNode("aimMatrix")
            mult = cmds.createNode("multMatrix")
            
            cmds.connectAttr(locatorB + ".worldMatrix", aim + ".inputMatrix", force=True)
            cmds.connectAttr(locatorC + ".worldMatrix", aim + ".primaryTargetMatrix", force=True)
            cmds.connectAttr(locatorC + ".worldMatrix", rotationC + ".offsetParentMatrix", force=True)
            cmds.connectAttr(rotationC + ".worldMatrix", mult + ".matrixIn[0]", force=True)
            cmds.connectAttr(rotationB + ".parentInverseMatrix", mult + ".matrixIn[1]", force=True)

            cmds.connectAttr(aim + ".outputMatrix", rotationB + ".offsetParentMatrix", force=True)

            cmds.connectAttr(mult + ".matrixSum", jointC + ".offsetParentMatrix", force=True)
      

# Helper function that tells the createFinger function how many fingers to make
def createFingerJoints(fingerAmount):
    for finger in range(0, fingerAmount):
        createFinger(finger)
        

# Creates the finger joints        
def createFinger(finger):
    ############
    # Left Hand
    ############
    # Finds all of the left finger locators
    allLeftFingers = cmds.ls("LOC_L_finger_" + str(finger) + "_*", type="locator")
    leftFinger = cmds.listRelatives(*allLeftFingers, parent=True, fullPath=True)
    
    # Loop through each finger to create the joints
    for i, L_finger in enumerate(leftFinger):
        if i == 0:
            jointAName = "JNT_L_arm_3"
            jointBName = "JNT_L_finger_" + str(finger) + "_" + str(i)
            
            jointA = "JNT_L_arm_3"
            jointB = cmds.createNode("joint", name=jointBName, parent=jointA)
            
            locatorA = "LOC_L_arm_3"
            locatorB = "LOC_L_finger_" + str(finger) + "_" + str(i)
            
            rotationA = "JNT_L_arm_3_REST"
            rotationB = cmds.createNode("transform", name=jointBName + "_REST", parent="opmStorage_GRP")
            
            aim = cmds.createNode("aimMatrix")
            mult = cmds.createNode("multMatrix")
            
            cmds.connectAttr(locatorA + ".worldMatrix", aim + ".inputMatrix", force=True)
            cmds.connectAttr(locatorB + ".worldMatrix", aim + ".primaryTargetMatrix", force=True)
            cmds.connectAttr(locatorB + ".worldMatrix", rotationB + ".offsetParentMatrix", force=True)
            cmds.connectAttr(rotationB + ".worldMatrix", mult + ".matrixIn[0]", force=True)
            cmds.connectAttr(rotationA + ".parentInverseMatrix", mult + ".matrixIn[1]", force=True)

            cmds.connectAttr(mult + ".matrixSum", jointB + ".offsetParentMatrix", force=True)
        else:
            jointBName = "JNT_L_finger_" + str(finger) + "_" + str(i - 1)
            jointCName = "JNT_L_finger_" + str(finger) + "_" + str(i)
            
            jointB = "JNT_L_finger_" + str(finger) + "_" + str(i - 1)
            jointC = cmds.createNode("joint", name=jointCName, parent=jointB)
            
            locatorB = "LOC_L_finger_" + str(finger) + "_" + str(i - 1)
            locatorC = "LOC_L_finger_" + str(finger) + "_" + str(i)
            
            rotationB = "JNT_L_finger_" + str(finger) + "_" + str(i - 1) + "_REST"
            rotationC = cmds.createNode("transform", name=jointCName + "_REST", parent="opmStorage_GRP")
            
            aim = cmds.createNode("aimMatrix")
            mult = cmds.createNode("multMatrix")
            
            cmds.connectAttr(locatorB + ".worldMatrix", aim + ".inputMatrix", force=True)
            cmds.connectAttr(locatorC + ".worldMatrix", aim + ".primaryTargetMatrix", force=True)
            cmds.connectAttr(locatorC + ".worldMatrix", rotationC + ".offsetParentMatrix", force=True)
            cmds.connectAttr(rotationC + ".worldMatrix", mult + ".matrixIn[0]", force=True)
            cmds.connectAttr(rotationB + ".parentInverseMatrix", mult + ".matrixIn[1]", force=True)

            cmds.connectAttr(aim + ".outputMatrix", rotationB + ".offsetParentMatrix", force=True)

            cmds.connectAttr(mult + ".matrixSum", jointC + ".offsetParentMatrix", force=True)    
    ############
    # Right Hand
    ############
    # Finds all of the right finger locators
    allRightFingers = cmds.ls("LOC_R_finger_" + str(finger) + "_*", type="locator")
    rightFinger = cmds.listRelatives(*allRightFingers, parent=True, fullPath=True)
    
    # Loop through each finger to create the joints
    for i, R_finger in enumerate(rightFinger):
        if i == 0:
            jointAName = "JNT_R_arm_3"
            jointBName = "JNT_R_finger_" + str(finger) + "_" + str(i)
            
            jointA = "JNT_R_arm_3"
            jointB = cmds.createNode("joint", name=jointBName, parent=jointA)
            
            locatorA = "LOC_R_arm_3"
            locatorB = "LOC_R_finger_" + str(finger) + "_" + str(i)
            
            rotationA = "JNT_R_arm_3_REST"
            rotationB = cmds.createNode("transform", name=jointBName + "_REST", parent="opmStorage_GRP")
            
            aim = cmds.createNode("aimMatrix")
            mult = cmds.createNode("multMatrix")
            
            cmds.connectAttr(locatorA + ".worldMatrix", aim + ".inputMatrix", force=True)
            cmds.connectAttr(locatorB + ".worldMatrix", aim + ".primaryTargetMatrix", force=True)
            cmds.connectAttr(locatorB + ".worldMatrix", rotationB + ".offsetParentMatrix", force=True)
            cmds.connectAttr(rotationB + ".worldMatrix", mult + ".matrixIn[0]", force=True)
            cmds.connectAttr(rotationA + ".parentInverseMatrix", mult + ".matrixIn[1]", force=True)

            cmds.connectAttr(mult + ".matrixSum", jointB + ".offsetParentMatrix", force=True)
        else:
            jointBName = "JNT_R_finger_" + str(finger) + "_" + str(i - 1)
            jointCName = "JNT_R_finger_" + str(finger) + "_" + str(i)
            
            jointB = "JNT_R_finger_" + str(finger) + "_" + str(i - 1)
            jointC = cmds.createNode("joint", name=jointCName, parent=jointB)
            
            locatorB = "LOC_R_finger_" + str(finger) + "_" + str(i - 1)
            locatorC = "LOC_R_finger_" + str(finger) + "_" + str(i)
            
            rotationB = "JNT_R_finger_" + str(finger) + "_" + str(i - 1) + "_REST"
            rotationC = cmds.createNode("transform", name=jointCName + "_REST", parent="opmStorage_GRP")
            
            aim = cmds.createNode("aimMatrix")
            mult = cmds.createNode("multMatrix")
            
            cmds.connectAttr(locatorB + ".worldMatrix", aim + ".inputMatrix", force=True)
            cmds.connectAttr(locatorC + ".worldMatrix", aim + ".primaryTargetMatrix", force=True)
            cmds.connectAttr(locatorC + ".worldMatrix", rotationC + ".offsetParentMatrix", force=True)
            cmds.connectAttr(rotationC + ".worldMatrix", mult + ".matrixIn[0]", force=True)
            cmds.connectAttr(rotationB + ".parentInverseMatrix", mult + ".matrixIn[1]", force=True)

            cmds.connectAttr(aim + ".outputMatrix", rotationB + ".offsetParentMatrix", force=True)

            cmds.connectAttr(mult + ".matrixSum", jointC + ".offsetParentMatrix", force=True)


# Function to delete all joints
def deleteJoints():
    allJoints = cmds.ls("JNT_*")
    cmds.delete(allJoints)
