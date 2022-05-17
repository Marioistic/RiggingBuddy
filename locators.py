import maya.cmds as cmds

# Creates the fields where user can set the amount of spine and finger joints
def createFields():
    
    global spineCount
    global fingerCount
    
    cmds.text("Spine Count", label="Spine Count")
    spineCount = cmds.intField(minValue=1, maxValue=11, value=4)

    cmds.text("Finger Count", label="Finger Count")
    fingerCount = cmds.intField(minValue=1, maxValue=11, value=5)


# Function to create all the OPM locators for the rig
def createLocators():
    
    global opmStorageGroup
    
    if cmds.objExists("opmStorage_GRP"):
        print("The locator group already exists!")
        return 0
    else:
        # Creates OPM storage group
        opmStorageGroup = cmds.group(empty=True, name="opmStorage_GRP")

    # Creates the root locator and parents it to opmStorage_GRP
    rootLocator = cmds.spaceLocator(name="LOC_root")
    cmds.scale(0.15, 0.15, 0.15, rootLocator)
    cmds.move(0, 2.5, 0, rootLocator)
    cmds.parent(rootLocator, opmStorageGroup)

    # Calls to each helper function below. The 1 value indicates left (1) or right (-1)
    createSpine()
    createHead()
    createLeg(1)
    createLeg(-1)
    createArm(1)
    createArm(-1)


# Creates the spine locators based upon the provided value by the user
def createSpine():
    for i in range(0, cmds.intField(spineCount, query=True, value=True)):
        # Creates LOC_spine_# and parents it to opmStorage_GRP
        spine = cmds.spaceLocator(name="LOC_spine_" + str(i))  # Example: LOC_spine_1
        cmds.scale(0.1, 0.1, 0.1, spine)
        cmds.parent(spine, opmStorageGroup)  
        cmds.move(0, 2.75 + (0.25 * i), 0, spine)

        
# Creates locators for the head
# Eyes and jaw are handled seperately
def createHead():
    # Creates neck locator and parents it to opmStorage_GRP
    neck = cmds.spaceLocator(name="LOC_C_head_0")
    cmds.scale(0.1, 0.1, 0.1, neck)
    cmds.move(0, 2.75 + (0.25 * cmds.intField(spineCount, query=True, value=True)), 0, neck)
    cmds.parent(neck, opmStorageGroup)
        
    # Creates face locator and parents it to opmStorage_GRP
    face = cmds.spaceLocator(name="LOC_C_head_1")
    cmds.scale(0.1, 0.1, 0.1, face)
    cmds.move(0, 3.2 + (0.25 * cmds.intField(spineCount, query=True, value=True)), 0, face)
    cmds.parent(face, opmStorageGroup)
        
    # Creates the top of the head locator and parents it to opmStorage_GRP
    headEnd = cmds.spaceLocator(name="LOC_C_head_2")
    cmds.scale(0.1, 0.1, 0.1, headEnd)
    cmds.move(0, 3.5 + (0.25 * cmds.intField(spineCount, query=True, value=True)), 0, headEnd)
    cmds.parent(headEnd, opmStorageGroup)    
        
    # Calls the jaw fuction to create jaw locators
    # Calls the eye function to create both eyes using 1 for left and -1 for right
    createJaw()
    createEye(1)
    createEye(-1)


# Creates the jaw locators
def createJaw():
    # Creates jaw base locator and parents it to opmStorage_GRP
    jawBase = cmds.spaceLocator(name="LOC_C_jaw_0")
    cmds.scale(0.1, 0.1, 0.1, jawBase)
    cmds.move(0, 3.0 + (0.25 * cmds.intField(spineCount, query=True, value=True)), 0.05, jawBase)
    cmds.parent(jawBase, opmStorageGroup)
        
    # Creates the end of the jaw locator and parents it to opmStorage_GRP
    jawEnd = cmds.spaceLocator(name="LOC_C_jaw_1")
    cmds.scale(0.1, 0.1, 0.1, jawEnd)
    cmds.move(0, 2.9 + (0.25 * cmds.intField(spineCount, query=True, value=True)), 0.2, jawEnd)
    cmds.parent(jawEnd, opmStorageGroup)
        

# Creates the eye locators 
def createEye(side):
    ###########
    # Left Eye
    ###########    
    if side == 1:
        # Creates the left eye locator and parents it to opmStorage_GRP
        leftEye = cmds.spaceLocator(name="LOC_L_eye_0")
        cmds.scale(0.1,0.1,0.1, leftEye)
        cmds.parent(leftEye, opmStorageGroup)
        cmds.move(0.1, 3.2 + (0.25 * cmds.intField(spineCount, query=True, value=True)), 0.15, leftEye)
            
        # Creates the left eye end locator and parents it to opmStorage_GRP
        leftEyeEnd = cmds.spaceLocator(name="LOC_L_eye_1")
        cmds.scale(0.1,0.1,0.1, leftEyeEnd)
        cmds.parent(leftEyeEnd, opmStorageGroup)
        cmds.move(0.1 * side, 3.2 + (0.25 * cmds.intField(spineCount, query=True, value=True)), 0.3, leftEyeEnd)  
    ############
    # Right Eye
    ############
    else:
        # Creates the right eye locator and parents it to opmStorage_GRP
        rightEye = cmds.spaceLocator(name="LOC_R_eye_0")
        cmds.scale(0.1,0.1,0.1, rightEye)
        cmds.parent(rightEye, opmStorageGroup)
        cmds.move(0.1 * side, 3.2 + (0.25 * cmds.intField(spineCount, query=True, value=True)), 0.15, rightEye)
            
        # Creates the right eye end locator and parents it to opmStorage_GRP
        rightEyeEnd = cmds.spaceLocator(name="LOC_R_eye_1")
        cmds.scale(0.1,0.1,0.1, rightEyeEnd)
        cmds.parent(rightEyeEnd, opmStorageGroup)
        cmds.move(0.1 * side, 3.2 + (0.25 * cmds.intField(spineCount, query=True, value=True)), 0.3, rightEyeEnd)
    

# Creates locators for both legs based upon the provided parameter (1 or -1)
def createLeg(side):
    ###########
    # Left Leg
    ###########
    if side == 1:
        # Creates left hip locator and parents it to opmStorage_GRP
        leftHip = cmds.spaceLocator(name="LOC_L_leg_0")
        cmds.scale(0.1, 0.1, 0.1, leftHip)
        cmds.move(0.2 * side, 2.4, 0, leftHip)
        cmds.parent(leftHip, opmStorageGroup)
            
        # Creates left knee locator and parents it to opmStorage_GRP
        leftKnee = cmds.spaceLocator(name="LOC_L_leg_1")
        cmds.scale(0.1, 0.1, 0.1, leftKnee)
        cmds.move(0.33 * side, 1.3, 0, leftKnee)
        cmds.parent(leftKnee, opmStorageGroup)

        # Creates left ankle locator and parents it to opmStorage_GRP
        leftAnkle = cmds.spaceLocator(name="LOC_L_leg_2")
        cmds.scale(0.1, 0.1, 0.1, leftAnkle)
        cmds.move(0.4 * side, 0.2, 0, leftAnkle)
        cmds.parent(leftAnkle, opmStorageGroup)

        # Creates left ball locator and parents it to opmStorage_GRP
        leftBall = cmds.spaceLocator(name="LOC_L_leg_3")
        cmds.scale(0.1, 0.1, 0.1, leftBall)
        cmds.move(0.4 * side, 0, 0.2, leftBall)
        cmds.parent(leftBall, opmStorageGroup)

        # Creates left toe locator and parents it to opmStorage_GRP
        leftToe = cmds.spaceLocator(name="LOC_L_leg_4")
        cmds.scale(0.1, 0.1, 0.1, leftToe)
        cmds.move(0.4 * side, 0, 0.5, leftToe)
        cmds.parent(leftToe, opmStorageGroup)    
    ############
    # Right Leg
    ############
    else:
        # Creates right hip locator and parents it to opmStorage_GRP
        rightHip = cmds.spaceLocator(name="LOC_R_leg_0")
        cmds.scale(0.1, 0.1, 0.1, rightHip)
        cmds.move(0.2 * side, 2.4, 0, rightHip)
        cmds.parent(rightHip, opmStorageGroup)

        # Creates right knee locator and parents it to opmStorage_GRP
        rightKnee = cmds.spaceLocator(name="LOC_R_leg_1")
        cmds.scale(0.1, 0.1, 0.1, rightKnee)
        cmds.move(0.33 * side, 1.3, 0, rightKnee)
        cmds.parent(rightKnee, opmStorageGroup)

        # Creates right ankle locator and parents it to opmStorage_GRP
        rightAnkle = cmds.spaceLocator(name="LOC_R_leg_2")
        cmds.scale(0.1, 0.1, 0.1, rightAnkle)
        cmds.move(0.4 * side, 0.2, 0, rightAnkle)
        cmds.parent(rightAnkle, opmStorageGroup)

        # Creates right ball locator and parents it to opmStorage_GRP
        rightBall = cmds.spaceLocator(name="LOC_R_leg_3")
        cmds.scale(0.1, 0.1, 0.1, rightBall)
        cmds.move(0.4 * side, 0, 0.2, rightBall)
        cmds.parent(rightBall, opmStorageGroup)

        # Creates right toe locator and parents it to opmStorage_GRP
        rightToe = cmds.spaceLocator(name="LOC_R_leg_4")
        cmds.scale(0.1, 0.1, 0.1, rightToe)
        cmds.move(0.4 * side, 0, 0.5, rightToe)
        cmds.parent(rightToe, opmStorageGroup)


# Creates locators for both arms based upon the provided parameter (1 or -1)
def createArm(side):
    ###########
    # Left Arm
    ###########
    if side == 1:
        # Creates left clavicle locator and parents it to opmStorage_GRP
        leftClavicle = cmds.spaceLocator(name="LOC_L_arm_0")
        cmds.scale(0.1, 0.1, 0.1, leftClavicle)
        cmds.parent(leftClavicle, opmStorageGroup)
        cmds.move(0.25 * side, 2.75 + (0.25 * cmds.intField(spineCount, query=True, value=True)), 0, leftClavicle)

        # Creates left shoulder locator and parents it to opmStorage_GRP
        leftShoulder = cmds.spaceLocator(name="LOC_L_arm_1")
        cmds.scale(0.1, 0.1, 0.1, leftShoulder)
        cmds.parent(leftShoulder, opmStorageGroup)
        cmds.move(0.5 * side, 2.55 + (0.25 * cmds.intField(spineCount, query=True, value=True)), 0, leftShoulder)
            
        # Creates left elbow locator and parents it to opmStorage_GRP
        leftElbow = cmds.spaceLocator(name="LOC_L_arm_2")
        cmds.scale(0.1, 0.1, 0.1, leftElbow)
        cmds.parent(leftElbow, opmStorageGroup)
        cmds.move(0.9 * side, 2.2 + (0.25 * cmds.intField(spineCount, query=True, value=True)), 0, leftElbow)
            
        # Creates left wrist locator and parents it to opmStorage_GRP
        leftWrist = cmds.spaceLocator(name="LOC_L_arm_3")
        cmds.scale(0.1, 0.1, 0.1, leftWrist)
        cmds.parent(leftWrist, opmStorageGroup)
        cmds.move(1.4 * side, 1.85 + (0.25 * cmds.intField(spineCount, query=True, value=True)), 0, leftWrist)
            
        # Calls the hand function with the provided side (1 = left) and left wrist locator)
        createHand(1, leftWrist)
    ############
    # Right Arm
    ############
    else:    
        # Creates right clavicle locator and parents it to opmStorage_GRP
        rightClavicle = cmds.spaceLocator(name="LOC_R_arm_0")
        cmds.scale(0.1, 0.1, 0.1, rightClavicle)
        cmds.parent(rightClavicle, opmStorageGroup)
        cmds.move(0.25 * side, 2.75 + (0.25 * cmds.intField(spineCount, query=True, value=True)), 0, rightClavicle)
            
        # Creates right shoulder locator and parents it to opmStorage_GRP
        rightShoulder = cmds.spaceLocator(name="LOC_R_arm_1")
        cmds.scale(0.1, 0.1, 0.1, rightShoulder)
        cmds.parent(rightShoulder, opmStorageGroup)
        cmds.move(0.5 * side, 2.55 + (0.25 * cmds.intField(spineCount, query=True, value=True)), 0, rightShoulder)
            
        # Creates right elbow locator and parents it to opmStorage_GRP
        rightElbow = cmds.spaceLocator(name="LOC_R_arm_2")
        cmds.scale(0.1, 0.1, 0.1, rightElbow)
        cmds.parent(rightElbow, opmStorageGroup)
        cmds.move(0.9 * side, 2.2 + (0.25 * cmds.intField(spineCount, query=True, value=True)), 0, rightElbow)
            
        # Creates right wrist locator and parents it to opmStorage_GRP
        rightWrist = cmds.spaceLocator(name="LOC_R_arm_3")
        cmds.scale(0.1, 0.1, 0.1, rightWrist)
        cmds.parent(rightWrist, opmStorageGroup)
        cmds.move(1.4 * side, 1.85 + (0.25 * cmds.intField(spineCount, query=True, value=True)), 0, rightWrist)
            
        # Calls the hand function with the provided side (-1 = right) and  right wrist locator)
        createHand(-1, rightWrist)


# Fuction for creating the hands using the provided side (1 or -1) and wrist locator
def createHand(side, wrist):
    ############
    # Left Hand
    ############
    if side == 1:
        # Stores the position of the left wrist locator
        leftHandPosition = cmds.xform(wrist, query=True, translation=True, worldSpace=True)
            
        # Calls the finger function using the side of the model, position of the hand, and provided number of desired fingers
        for i in range(0, cmds.intField(fingerCount, query=True, value=True)):
            createFingers(1, leftHandPosition, i)
    #############
    # Right Hand
    #############
    else:
        # Stores the position of the right wrist locator
        rightHandPosition = cmds.xform(wrist, query=True, translation=True, worldSpace=True)
        
        # Calls the finger function using the side of the model, position of the hand, and provided number of desired fingers
        for i in range(0, cmds.intField(fingerCount, query=True, value=True)):
            createFingers(-1, rightHandPosition, i)


# Function used to create the individual fingers using the side, position of the hand group, and user provided finger count
def createFingers(side, handPosition, count):
    for x in range(0, 4):
        ###############
        # Left Fingers
        ###############
        if side == 1:
            # Creates fingers in the form of LOC_L_finger_<finger#>_<knuckle#>
            leftFinger = cmds.spaceLocator(name="LOC_L_finger_" + str(count) + "_" + str(x))
            cmds.scale(0.03, 0.03, 0.03, leftFinger)
            # Parents the knuckle LOC of each finger to opmStorage_GRP
            cmds.parent(leftFinger, opmStorageGroup)
            cmds.move(handPosition[0] + (0.1 + (0.1 * x)) * side, handPosition[1] - (0.1 + (0.1 * x)),
                      handPosition[2] + -(0.05 * count), leftFinger)
        ################
        # Right Fingers
        ################
        else:
            # Creates fingers in the form of LOC_R_finger_<finger#>_<knuckle#>
            rightFinger = cmds.spaceLocator(name="LOC_R_finger_" + str(count) + "_" + str(x))
            cmds.scale(0.03, 0.03, 0.03, rightFinger)
            # Parents the knuckle LOC of each finger to opmStorage_GRP
            cmds.parent(rightFinger, opmStorageGroup)
            cmds.move(handPosition[0] + (0.1 + (0.1 * x)) * side, handPosition[1] - (0.1 + (0.1 * x)),
                      handPosition[2] + -(0.05 * count), rightFinger)
                      
   
# Function for mirroring user edits to locators from left to right (model's perspective)                
def mirrorLocators():
    allLeftLocators = cmds.ls("LOC_L_*")
    leftLocators = cmds.listRelatives(*allLeftLocators, parent=True, fullPath=True)
    
    allRightLocators = cmds.ls("LOC_R_*")
    rightLocators = cmds.listRelatives(*allRightLocators, parent=True, fullPath=True)
    

    for i, left in enumerate(leftLocators):
        leftPosition = cmds.xform(left, query=True, translation=True, worldSpace=True)
        cmds.move(-leftPosition[0], leftPosition[1], leftPosition[2], rightLocators[i])
        

# Removes all locators from the scene
def deleteLocators():
    cmds.delete("opmStorage_GRP")
