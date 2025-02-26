#switchFkIkDynamic.py
'''
This is the script originally wrote in only one file
I'm working on separating it in appropriate modules
'''

import maya.cmds as cmds
import maya.mel as mel
import re

'''
For Maya
Make the IK, FK and dynamic (IK on simulated curve) setup of a selected joints chain
Create all controllers
Selection order : setting, jointChain
'''

'''Store CVs position for each type of controller'''
class BSControlsData():
    controlNames = ['Square', 'Box', 'Circle Pin', 'Square Pin']
    cvTuples = {}
    cvTuples['Square'] = [(0.0, 0.005367678345843243, -0.12648576440672452), 
                          (0.0, 0.005367678345843243, 0.23232169797369148), 
                          (0.0, -0.4555341553434661, 0.23232169797369115), 
                          (0.0, -0.4555341553434661, -0.12648576440672468), 
                          (0.0, 0.005367678345843243, -0.12648576440672452)]
    cvTuples['Box'] = [(-0.14132073899449515, 0.060908589616468674, 0.1739366553564884), 
                       (-0.14132073899449515, -0.1505310268352206, 0.1739366553564884), 
                       (0.14132073899449515, -0.1505310268352206, 0.1739366553564884), 
                       (0.14132073899449515, 0.060908589616468674, 0.1739366553564884), 
                       (-0.14132073899449515, 0.060908589616468674, 0.1739366553564884), 
                       (-0.14132073899449515, 0.060908589616468674, -0.08836590043546423), 
                       (-0.14132073899449515, -0.1505310268352206, -0.08836590043546423), 
                       (-0.14132073899449515, -0.1505310268352206, 0.1739366553564884), 
                       (0.14132073899449515, -0.1505310268352206, 0.1739366553564884), 
                       (0.14132073899449515, -0.1505310268352206, -0.08836590043546423), 
                       (0.14132073899449515, 0.060908589616468674, -0.08836590043546423), 
                       (0.14132073899449515, 0.060908589616468674, 0.1739366553564884), 
                       (-0.14132073899449515, 0.060908589616468674, 0.1739366553564884), 
                       (-0.14132073899449515, 0.060908589616468674, -0.08836590043546423), 
                       (0.14132073899449515, 0.060908589616468674, -0.08836590043546423), 
                       (0.14132073899449515, -0.1505310268352206, -0.08836590043546423), 
                       (-0.14132073899449515, -0.1505310268352206, -0.08836590043546423)]
    cvTuples['Circle Pin'] = [(0.0, 1.2629202010474528e-07, 0.22591276829460605), 
                              (0.0, 0.022057267053470782, 0.22764869919590214), 
                              (0.0, 0.04357128175909273, 0.23281375650905667), 
                              (0.0, 0.06401243855738005, 0.24128075937507631), 
                              (0.0, 0.08287738640145144, 0.2528412162357826), 
                              (0.0, 0.09970163319484941, 0.26721047661248154), 
                              (0.0, 0.11407089357154852, 0.28403471500167354), 
                              (0.0, 0.1256313588364623, 0.30289966284574454), 
                              (0.0, 0.13409836170248146, 0.32334081544192894), 
                              (0.0, 0.13926341901563588, 0.34485483855175747), 
                              (0.0, 0.14099934991693197, 0.3669119583026915), 
                              (0.0, 0.13926341901563588, 0.3889690780536257), 
                              (0.0, 0.13409836170248146, 0.41048310116345477), 
                              (0.0, 0.1256313588364623, 0.43092425375963817), 
                              (0.0, 0.11407089357154852, 0.4497892016037095), 
                              (0.0, 0.09970163319484941, 0.46661343999290106), 
                              (0.0, 0.08287738640145144, 0.48098270036960034), 
                              (0.0, 0.06401243855738005, 0.49254315723030695), 
                              (0.0, 0.04357128175909273, 0.5010101600963267), 
                              (0.0, 0.022057267053470782, 0.5061752174094801), 
                              (0.0, 1.2629202010474528e-07, 0.5079111483107767), 
                              (0.0, -0.022057008166275597, 0.5061752174094801), 
                              (0.0, -0.043571020770845896, 0.5010101600963267), 
                              (0.0, -0.06401216916492657, 0.49254315723030695), 
                              (0.0, -0.0828771170089979, 0.48098270036960034), 
                              (0.0, -0.09970135539818938, 0.46661343999290106), 
                              (0.0, -0.1140706157748886, 0.4497892016037095), 
                              (0.0, -0.1256310726355954, 0.43092425375963817), 
                              (0.0, -0.13409807550161487, 0.41048310116345477), 
                              (0.0, -0.13926313281476907, 0.3889690780536257), 
                              (0.0, -0.14099906371606533, 0.3669119583026915), 
                              (0.0, -0.13926313281476907, 0.34485483855175747), 
                              (0.0, -0.13409807550161487, 0.32334081544192894), 
                              (0.0, -0.1256310726355954, 0.30289966284574454), 
                              (0.0, -0.1140706157748886, 0.28403471500167354), 
                              (0.0, -0.09970135539818938, 0.26721047661248154), 
                              (0.0, -0.0828771170089979, 0.2528412162357826), 
                              (0.0, -0.06401216916492657, 0.24128075937507631), 
                              (0.0, -0.043571020770845896, 0.23281375650905667), 
                              (0.0, -0.022057008166275597, 0.22764869919590214), 
                              (0.0, 1.2629202010474528e-07, 0.22591276829460605), 
                              (0.0, 0.0, 0.0)]
    cvTuples['Square Pin'] = [(0.0, 0.0, 0.22128980957915795), 
                              (0.0, 0.15143521257966858, 0.22128980957915795), 
                              (0.0, 0.15143521257966858, 0.5241602347384953), 
                              (0.0, -0.15143521257966858, 0.5241602347384953), 
                              (0.0, -0.15143521257966858, 0.22128980957915795), 
                              (0.0, 0.0, 0.22128980957915795), (0.0, 0.0, 0.0)]

def bsColorCurve(curveTransfo, colorShape):
    curveShape = "".join(cmds.listRelatives(curveTransfo, s=True))
    cmds.setAttr(f'{curveShape}.overrideEnabled', 1)
    cmds.setAttr(f'{curveShape}.overrideColor', colorShape)
    
def bsDrawCurve(curvePoints, nameJoint):
    '''create curve for controller'''
    controlCurve = cmds.curve(d=1, p=BSControlsData.cvTuples[curvePoints])
    if 'IK' in nameJoint:
        '''rename IK to avoid double'''
        cutName = nameJoint.find('IK')
        controlCurve = cmds.rename(f'{controlCurve}', f'{nameJoint[0:(cutName+1)]}')
        #print(f'name ik control: {nameJoint}')
    else:
        controlCurve = cmds.rename(f'{controlCurve}', f'{nameJoint}'.replace("_JNT", "_CTRL"))
    cmds.matchTransform(f'{controlCurve}', f'{nameJoint}')
    return controlCurve
    
def ikSimulationColor(settingSimulation, ikControl, nameBaseJoint):
    '''make the ik control change color when simulation is on'''
    #nameBase = f'{getNiceName(firstJoint)}'.replace('_00', '')
    nameBaseJoint = f'{nameBaseJoint}_condition'
    #jointNumber = "".join(re.findall('_[0-9][0-9]', getNiceName(mainJoint)))
    #jointNamePattern = re.sub('_[0-9][0-9]', f'_{chainType}{jointNumber}', getNiceName(mainJoint))
    nameCondition = re.sub('[A-Z]_[A-Z]_', '', nameBaseJoint)
    nameCondition = f'{nameCondition}'.replace('_', '_IkControls_color_', 1)
    #print(f'name color condition: {nameCondition}')

    ikShape = "".join(cmds.listRelatives(ikControl, s=True))
    cmds.setAttr(f'{ikShape}.overrideEnabled', 1)
    if not cmds.objExists(f'{nameCondition}'):
        cmds.createNode('condition', name = f'{nameCondition}')
        cmds.connectAttr(f'{settingSimulation}.simulation', f'{nameCondition}.firstTerm')
        cmds.setAttr(f'{nameCondition}.operation', 2)
        cmds.setAttr(f'{nameCondition}.colorIfTrueR', 16)
        cmds.setAttr(f'{nameCondition}.colorIfFalseR', 28)
    cmds.connectAttr(f'{nameCondition}.outColorR', f'{ikShape}.overrideColor')
    
def zeroMatrix(ctrl):
    matrixSelect = cmds.getAttr(f'{ctrl}.matrix')

    matrixZero = iter([1.0, 0.0, 0.0, 0.0, 
                       0.0, 1.0, 0.0, 0.0, 
                       0.0, 0.0, 1.0, 0.0, 
                       0.0, 0.0, 0.0, 1.0])
    #print(list(matrixZero))
                  
    if matrixSelect != list(matrixZero) :
        '''pass if there is no change in obj matrix'''

        matrixClean = [matrixSelect[i:i+4] for i in range(0, len(matrixSelect), 4)]
        
        matrixOffsetSelect = cmds.getAttr(f'{ctrl}.offsetParentMatrix')
        matrixOffsetClean = [matrixOffsetSelect[i:i+4] for i in range(0, len(matrixOffsetSelect), 4)]
            
        '''multiply obj matrix and offset matrix
        so that new changes are updated'''
        matrixMult = [[sum(a*b for a, b in zip(matrix_row, offset_col)) 
            for offset_col in zip(*matrixOffsetClean)] for matrix_row in matrixClean]
        matrixResult = [j for i in matrixMult for j in i]
            
        '''transfer values on OffsetParentMatrix'''
        cmds.setAttr(f'{ctrl}.offsetParentMatrix', matrixResult, type='matrix')
        
        '''reset obj matrix'''
        for coordinates in ('translate', 'rotate', 'shear'):
            cmds.setAttr(f'{ctrl}.{coordinates}', 0, 0, 0, type='short3')
        cmds.setAttr(f'{ctrl}.scale', 1, 1, 1, type='short3')

        if cmds.objectType(f'{ctrl}', isType='joint'):
            cmds.setAttr(f'{ctrl}.jointOrient', 0, 0, 0, type='short3')
    
def getNiceName(pathObject):
    return pathObject.split('|')[len(pathObject.split('|'))-1]
    
def replaceShape(toReplace, replacement):
    '''modify shape of controller with another selected shape'''
    
    newReplacement = "".join(cmds.duplicate(f'{replacement}'))
    replacementShape = "".join(cmds.listRelatives(f'{replacement}', shapes=True))
    toReplaceShape = "".join(cmds.listRelatives(f'{toReplace}', shapes=True))
    #print(f'replacementShape: {replacementShape}')
    #print(f'toReplaceShape: {toReplaceShape}')
    cmds.matchTransform(f'{replacement}', f'{toReplace}')
    cmds.parent(f'{replacementShape}', f'{toReplace}', relative=True, shape=True)
    cmds.delete(f'{toReplaceShape}', shape=True)
    cmds.delete(f'{replacement}', shape=True)
    cmds.rename(f'{replacementShape}', f'{toReplaceShape}')
    return newReplacement
    
def createSwitchAttr(settingPath):
    '''create switch attribut on setting controller
    and create and connect a reverse node connected to it'''
    
    settingName = getNiceName(settingPath)
    
    if 'switch_FK_IK' not in cmds.listAttr(f'{settingPath}'):
        cmds.addAttr(f'{settingPath}', ln='switch_FK_IK', at='double', min=0, max=1, dv=0,
                     keyable=True, readable=True)
    
    '''create and connect the reverse node for switch setup'''
    increment = 0
    while cmds.objExists(f'{settingName}_reverse_{increment}'):
        '''in case there is already a reverse with this name, make it unique'''
        increment += 1
    reverseSwitchNode = cmds.createNode('reverse', name=f'{settingName}_reverse_{increment}')
    
    cmds.connectAttr(f'{settingName}.switch_FK_IK', f'{reverseSwitchNode}.input.inputX')
    return reverseSwitchNode
    
def createDynamicAttr(settingPath):
    '''create dynamic attributes on controller'''
    
    if 'DYNAMICS' not in cmds.listAttr(f'{settingPath}'):
        cmds.addAttr(f'{settingPath}', ln='DYNAMICS', attributeType='enum', enumName='----------:o')
        cmds.setAttr(f'{settingPath}.DYNAMICS', channelBox=True, lock=True)
        cmds.addAttr(f'{settingPath}', longName='enabled', attributeType='bool', defaultValue=0)
        cmds.addAttr(f'{settingPath}', longName='simulation', attributeType='float', defaultValue=0, min=0, max=1)
        cmds.addAttr(f'{settingPath}', longName='follow_pose', attributeType='float', defaultValue=0, min=0, max=1)
        cmds.addAttr(f'{settingPath}', longName='drag', attributeType='float', defaultValue=0.05)
        cmds.addAttr(f'{settingPath}', longName='turbulence', attributeType='float', defaultValue=0)
        cmds.addAttr(f'{settingPath}', longName='wind_speed', attributeType='float', defaultValue=0)
        
        for attributeTitle in ('enabled', 'simulation', 'follow_pose', 'drag', 'turbulence', 'wind_speed'):
            cmds.setAttr(f'{settingPath}.{attributeTitle}', keyable=True)
            
    '''create and connect the reverse node for switch setup'''
    increment = 0
    while cmds.objExists(f'{settingPath}_reverseDyna_{increment}'):
        '''in case there is already a reverse with this name, make it unique'''
        increment += 1
    reverseSimulationNode = cmds.createNode('reverse', name=f'{settingPath}_reverseDyna_{increment}')
    
    cmds.connectAttr(f'{settingPath}.simulation', f'{reverseSimulationNode}.input.inputX')
    
    return reverseSimulationNode
    
def createVisibilityAttr(settingPath, reverseSetting):
    '''create dynamic visibility attributes on controller'''
    
    if 'VISIBILITY' not in cmds.listAttr(f'{settingPath}'):
        cmds.addAttr(f'{settingPath}', ln='VISIBILITY', attributeType='enum', enumName='----------:o')
        cmds.setAttr(f'{settingPath}.VISIBILITY', channelBox=True, lock=True)
        cmds.addAttr(f'{settingPath}', longName='all_controls_vis', attributeType='bool', defaultValue=1)
        cmds.addAttr(f'{settingPath}', longName='dynamic_base_vis', attributeType='bool', defaultValue=0)
        
        for attributeTitle in ('all_controls_vis', 'dynamic_base_vis'):
            cmds.setAttr(f'{settingPath}.{attributeTitle}', keyable=True)
            
    '''create and connect the multiplyDivide node for switch setup'''
    increment = 0
    while cmds.objExists(f'{getNiceName(settingPath)}_visMulti_{increment}'):
        '''in case there is already a reverse with this name, make it unique'''
        increment += 1
    multiVisibilityNode = cmds.createNode('multiplyDivide', name=f'{getNiceName(settingPath)}_visMulti_{increment}')
    
    cmds.connectAttr(f'{settingPath}.all_controls_vis', f'{multiVisibilityNode}.input1X')
    cmds.connectAttr(f'{settingPath}.dynamic_base_vis', f'{multiVisibilityNode}.input2X')
    
    cmds.connectAttr(f'{settingPath}.all_controls_vis', f'{multiVisibilityNode}.input1Y')
    cmds.connectAttr(f'{settingPath}.switch_FK_IK', f'{multiVisibilityNode}.input2Y')
    
    cmds.connectAttr(f'{settingPath}.all_controls_vis', f'{multiVisibilityNode}.input1Z')
    cmds.connectAttr(f'{reverseSetting}.output.outputX', f'{multiVisibilityNode}.input2Z')
    
    return multiVisibilityNode
    
def revPoseControlsVis(settingPath, multiVisNode, chainCTRL):
    '''make IK controls invisible when Base Curve control are visible'''
    
    increment = 0
    while cmds.objExists(f'{getNiceName(settingPath)}_reverseVis_{increment}'):
        '''in case there is already a reverse with this name, make it unique'''
        increment += 1
    reverseVisSwitchNode = cmds.createNode('plusMinusAverage', name=f'{getNiceName(settingPath)}_pmaVis_{increment}')
    cmds.setAttr(f'{reverseVisSwitchNode}.operation', 2)
    cmds.connectAttr(f'{multiVisNode}.outputY', f'{reverseVisSwitchNode}.input1D[0]', f=True)
    cmds.connectAttr(f'{multiVisNode}.outputX', f'{reverseVisSwitchNode}.input1D[1]', f=True)
    
    for indivCtrl in chainCTRL:
        indivCtrlShape = "".join(cmds.listRelatives(f'{indivCtrl}', shapes=True))
        #print(f'indivCtrlShape: {indivCtrlShape}')
        cmds.connectAttr(f'{reverseVisSwitchNode}.output1D', f'{indivCtrlShape}.visibility', f=True)
    
def createJointsChain(listChainType, copyJoint, nameReplacement, groupSetupType):
    '''duplicate selected joint chain and rename it'''
    
    jointType = cmds.duplicate(f'{copyJoint}', parentOnly=True, name=nameReplacement)
    listChainType.append("".join(jointType))
    if len(listChainType) == 1:
        cmds.parent(f'{"".join(jointType)}', f'{groupSetupType}')
    if len(listChainType) > 1:
        parentUnder = "".join(listChainType[len(listChainType)-2])
        #print(f'parentUnder: {parentUnder}')
        cmds.parent(f'{"".join(jointType)}', parentUnder)
    return "".join(jointType)
    
def switchControlsIkSimulation(settingPath, reverseSetting, constraintIk):
    '''connection so that the IK controls switch between the IK curve and the dynamic curve'''
    
    #constraintDynaAttr = "".join(cmds.listAttr(f'{constraintDynamic}', userDefined=True))
    constraintIkAttr = "".join(cmds.listAttr(f'{constraintIk}', userDefined=True))
    #print(f'constraintDynaAttr: {constraintDynaAttr}')
    print(f'constraintIkAttr: {constraintIkAttr}')
    #cmds.connectAttr(f'{settingPath}.simulation', f'{constraintDynamic}.{constraintDynaAttr}', f=True)
    cmds.connectAttr(f'{reverseSetting}.output.outputX', f'{constraintIk}.{constraintIkAttr}', f=True)
    
def parentFkControls(baseGroupName, chainJoints, reverseVisCtrl):
    '''create Fk contols and parent joints to them'''
    chainFkCTRL = []
    groupFkCtrl = cmds.group(empty=True, name=f'{baseGroupName}_FK_controls_GRP')
    for currentJoint in chainJoints:
        if currentJoint == chainJoints[len(chainJoints)-1]:
            controlFk = bsDrawCurve('Box', currentJoint)
        else:
            controlFk = bsDrawCurve('Square', currentJoint)
            
        bsColorCurve(controlFk, 18)
        chainFkCTRL.append(controlFk)
        cmds.parent(f'{controlFk}', f'{groupFkCtrl}')
        cmds.parentConstraint(f'{controlFk}', f'{currentJoint}')

    chainFkCTRL.sort()
    for currentFk in enumerate(chainFkCTRL):
        indexCurrentFk, currentFkCTRL = currentFk
        if indexCurrentFk:
            cmds.parent(f'{currentFkCTRL}', f'{chainFkCTRL[indexCurrentFk-1]}')
            
        zeroMatrix(currentFkCTRL)
        
    print(f'chainFkCTRL: {chainFkCTRL}')
    print(f'chainJoints: {chainJoints}')
    cmds.connectAttr(f'{reverseVisCtrl}.outputZ', f'{groupFkCtrl}.visibility', f=True)
                
            
def parentIkControls(baseGroupName, chainCluster, chainClusterBase, chainClusterIK, *arg):
    '''parent clusters under IK contols, and create base dynamic controls'''
    
    settingsSimuCtrl, reverseSettings, multiVisSettings = arg
    
    groupIkCtrl = cmds.group(empty=True, name=f'{baseGroupName}_IK_controls_GRP')
    #print(f'groupIkCtrl: {groupIkCtrl}')
    chainIkCtrl = []
    chainBaseDynaCtrl = []
    
    groupPose = cmds.group(empty=True, name=f'{getNiceName(groupIkCtrl)}'.replace('_IK_', '_baseDyna_'))
    cmds.connectAttr(f'{multiVisSettings}.outputX', f'{groupPose}.visibility', f=True)
    cmds.parent(f'{groupPose}', f'{groupIkCtrl}')
    increment = 0
    
    for currentCluDyna, currentCluBase, currentCluIk in zip(chainCluster, chainClusterBase, chainClusterIK):
        '''create and parent every controlleur for each cluster chain'''
        controlIk = bsDrawCurve('Circle Pin', currentCluIk)
        controlBase = bsDrawCurve('Square Pin', currentCluBase)
        
        refControlOrient = f'{baseGroupName}_FK_0{increment}_CTRL'
        cmds.matchTransform(f'{controlIk}', f'{refControlOrient}', rotationY=True)
        cmds.matchTransform(f'{controlBase}', f'{refControlOrient}', rotationY=True)
        zeroMatrix(controlIk)
        zeroMatrix(controlBase)
        
        controlIk = cmds.rename(f'{controlIk}', f'{baseGroupName}_IK_0{increment}_CTRL')
        controlBase = cmds.rename(f'{controlBase}', f'{baseGroupName}_baseDyna_0{increment}_CTRL')
        increment += 1
        
        ikSimulationColor(settingsSimuCtrl, controlIk, baseGroupName)
        bsColorCurve(controlBase, 5)
        
        cmds.parent(f'{controlIk}', f'{groupIkCtrl}')
        cmds.parent(f'{controlBase}', f'{groupPose}')
        cmds.parent(f'{currentCluBase}', f'{controlBase}')
        
        chainIkCtrl.append(controlIk)
        chainBaseDynaCtrl.append(controlBase)
        
        cmds.connectAttr(f'{controlIk}.translate', f'{currentCluDyna}.translate')
        cmds.connectAttr(f'{controlIk}.rotate', f'{currentCluDyna}.rotate')
        #print(f'controlIK: {controlIk}')
        #print(f'currentCluIk: {currentCluIk}')
        constraintClusterIk = "".join(cmds.parentConstraint(f'{controlIk}', f'{currentCluIk}', mo=True))
        switchControlsIkSimulation(settingsSimuCtrl, reverseSettings, constraintClusterIk)
    
    chainIkCtrl.sort()
    chainBaseDynaCtrl.sort()
    #print(f'chainIkCTRL: {chainIkCTRL}')
    cmds.connectAttr(f'{multiVisSettings}.outputY', f'{groupIkCtrl}.visibility', f=True)
    revPoseControlsVis(settingsSimuCtrl, multiVisSettings, chainIkCtrl)
    
    
selection = cmds.ls(long=True, orderedSelection=True)
settingsCTRL, firstJoint, *others = selection

#print(f'settingsCTRL: {settingsCTRL}')
#print(f'firstJoint: {firstJoint}')

reverseSwitch = createSwitchAttr(settingsCTRL)
settingLast = getNiceName(settingsCTRL)
reverseSimulation = createDynamicAttr(settingsCTRL)
multiVisibilitySetting = createVisibilityAttr(settingsCTRL, reverseSwitch)

listChainJoints = cmds.listRelatives(f'{firstJoint}', allDescendents=True, fullPath=True, type='joint')
listChainJoints.append(f'{firstJoint}')
listChainJoints.sort()

#print(f'listChainJoints: {listChainJoints}')

listChainFK = []
listChainIK = []
nameBase = f'{getNiceName(firstJoint)}'.replace('_00_JNT', '')
#groupName = f'{firstJoint}'.replace('_00', '_setupFkIk_GRP')
groupSetup = cmds.group(empty=True, name=f'{nameBase}_setupFkIk_GRP')
cmds.setAttr(f'{groupSetup}.visibility', 0)

for chainType in ('FK', 'IK'):
    for mainJoint in listChainJoints:
        '''find name pattern in main joint chain to rename duplicated chain properly'''
        
        #print(f'mainJoint: {mainJoint}')
        jointNumber = "".join(re.findall('_[0-9][0-9]', getNiceName(mainJoint)))
        jointNamePattern = re.sub('_[0-9][0-9]', f'_{chainType}{jointNumber}', getNiceName(mainJoint))
        #print(f'jointNamePattern: {jointNamePattern}')
        
        if chainType == 'FK':
            fkJoint = createJointsChain(listChainFK, mainJoint,jointNamePattern, groupSetup)
            #print(f'jointFK: {jointFK}')
            #bsDrawCurve('Square', jointFK)
                
        if chainType == 'IK':
            ikJoint = createJointsChain(listChainIK, mainJoint,jointNamePattern, groupSetup)
            
        
#print(f'listChainFK: {listChainFK}')
#print(f'listChainIK: {listChainIK}')
parentFkControls(nameBase, listChainFK, multiVisibilitySetting)

for mainJNT, jointFK, jointIK in zip(listChainJoints, listChainFK, listChainIK):
    '''create and connect parentConstraint of main joint chain to switch attribute'''
    
    #print(f'mainJNT: {mainJNT}')
    #print(f'jointFK: {jointFK}')
    #print(f'jointIK: {jointIK}')
    jointConstrain = "".join(cmds.parentConstraint(f'{jointFK}', f'{jointIK}', f'{mainJNT}'))
    #print(f'jointConstrain: {jointConstrain}')
    for constraintValue in cmds.listAttr(f'{jointConstrain}', userDefined=True):
        if 'IK' in constraintValue:
            #print(f'Contrainte IK: {constraintValue}')
            cmds.connectAttr(f'{settingLast}.switch_FK_IK', f'{jointConstrain}.{constraintValue}', 
                              f=True)
            
        if 'FK' in constraintValue:
            #print(f'Contrainte FK: {constraintValue}')
            cmds.connectAttr(f'{reverseSwitch}.output.outputX', f'{jointConstrain}.{constraintValue}', 
                              f=True)
                              
'''create dynamic curve'''
nameHandle = f'{nameBase}_IK_HDL'
dynamicIk = cmds.ikHandle(name=nameHandle, numSpans=3, solver='ikSplineSolver', 
                startJoint=listChainIK[0], endEffector=listChainIK[len(listChainIK)-1])
#print(f'dynamicIk: {dynamicIk}')
dynamicHdl, dynamicEff, dynamicCurveIK = dynamicIk
#print(f'dynamicHdl: {dynamicHdl}')
#print(f'dynamicEff: {dynamicEff}')
#print(f'dynamicCurveIK: {dynamicCurveIK}')

cmds.parent(f'{dynamicHdl}', f'{groupSetup}')
cmds.rename(f'{dynamicEff}', f'{nameBase}_IK_EFF')
dynamicCurveIK = cmds.rename(f'{dynamicCurveIK}', f'{nameBase}_IK_curve')
dynamicCurveOg = "".join(cmds.duplicate(f'{dynamicCurveIK}', name=f'{nameBase}_dynamic_base_curveOg'))
#print(f'dynamicCurveOg: {dynamicCurveOg}')
cmds.select(f'{dynamicCurveOg}')
mel.eval('makeCurvesDynamic 2 { "1", "0", "1", "1", "0"}')

'''find, rename and sort objects that as been created''' 

transfoFollicle = "".join(cmds.listConnections(f'{dynamicCurveOg}', source=False))
curveFollicle = "".join(cmds.listConnections(f'{dynamicCurveOg}', source=False, shapes=True))
#print(f'curveFollicle: {curveFollicle}')
dynamicCurveMoov = "".join([A for A in cmds.listConnections(f'{curveFollicle}', source=False) if 'curve' in A])
#print(f'dynamicCurveMoov: {dynamicCurveMoov}')
dynamicHairSystem = "".join([A for A in cmds.listConnections(f'{curveFollicle}', destination=False) if 'hairSystem' in A])
#print(f'dynamicHairSystem: {dynamicHairSystem}')

transfoFollicle = cmds.rename(f'{transfoFollicle}', f'{nameBase}_dynamic_follicle')
dynamicCurveMoov = cmds.rename(f'{dynamicCurveMoov}', f'{nameBase}_dynamic_curve')
dynamicHairSystem = cmds.rename(f'{dynamicHairSystem}', f'{nameBase}_dynamic_hairSystem')
groupName = f'{nameBase}_setupDynamic_GRP'
groupSetupDynamic = cmds.group(f'{dynamicHairSystem}', f'{transfoFollicle}', name=groupName, parent=groupSetup)
groupCurveDynamic = cmds.group(f'{dynamicCurveMoov}', f'{dynamicCurveOg}', f'{dynamicCurveIK}', name=f'{nameBase}_curveDynamic_GRP',
                               parent=groupSetupDynamic)
cmds.delete('hairSystem*OutputCurves')

'''make curve only attached to the base'''

cmds.setAttr(f'{transfoFollicle}Shape.pointLock', 1)

'''connect simulation settings so that the IK chain can follow it'''

dynamicNucleus = "".join(cmds.ls(type='nucleus'))
dynamicBlendShape = "".join(cmds.blendShape(f'{dynamicCurveMoov}', f'{dynamicCurveIK}', 
                    name=f'{dynamicCurveIK}'.replace('_curve', '_blendShape')))
cmds.connectAttr(f'{settingsCTRL}.simulation', f'{dynamicBlendShape}.{dynamicCurveMoov}')
cmds.connectAttr(f'{settingsCTRL}.follow_pose', f'{dynamicHairSystem}.startCurveAttract')
cmds.connectAttr(f'{settingsCTRL}.enabled', f'{dynamicNucleus}.enable', f=True)

'''create cluster for sculpting dynamic curve and IK curve'''

listCurveOgClusterHDL = []
listCurveClusterHDL = []
listCurveIkClusterHDL = []
groupClusterGlobal = cmds.group(empty=True, name=f'{nameBase}_all_CLU_GRP', parent=f'{groupSetupDynamic}')

for curveType in (dynamicCurveOg, dynamicCurveMoov, dynamicCurveIK):
    '''create clusters for every curves'''
    incrementation = 0
    
    if curveType == dynamicCurveOg:
        clusterBaseName = f'{getNiceName(curveType)}'.replace('_curveOg', '_CLU')
    else:
        clusterBaseName = f'{getNiceName(curveType)}'.replace('_curve', '_CLU')
        groupCluster = cmds.group(empty=True, name=f'{clusterBaseName}_GRP', parent=f'{groupClusterGlobal}')
    
    for rangeClu in ('0:1', '2', '3', '4:5'):
        curveCluster, curveCluHandle = cmds.cluster(f'{curveType}.cv[{rangeClu}]', name=f'{clusterBaseName}_{incrementation}')
        curveCluster = "".join(curveCluster)
        curveCluHandle = "".join(curveCluHandle)
        incrementation += 1
        
        if curveType != dynamicCurveOg:
            cmds.parent(f'{curveCluHandle}', f'{groupCluster}')
            cmds.setAttr(f'{curveCluster}.relative', 1)
         
        if curveType == dynamicCurveOg:
            listCurveOgClusterHDL.append(f'{curveCluHandle}')
            cmds.setAttr(f'{curveCluHandle}.visibility', 0)
            
        elif curveType == dynamicCurveMoov:
            listCurveClusterHDL.append(f'{curveCluHandle}')
        else:
            listCurveIkClusterHDL.append(f'{curveCluHandle}')
         
#print(f'listCurveOgClusterHDL: {listCurveOgClusterHDL}')
#print(f'listCurveClusterHDL: {listCurveClusterHDL}')
#print(f'listCurveIkClusterHDL: {listCurveIkClusterHDL}')
parentIkControls(nameBase, listCurveClusterHDL, listCurveOgClusterHDL, listCurveIkClusterHDL, settingsCTRL, reverseSimulation, 
                 multiVisibilitySetting)
cmds.group(f'{nameBase}_FK_controls_GRP', f'{nameBase}_IK_controls_GRP', name=f'{nameBase}_controls_GRP')
     
'''connect curve behaviour settings'''

dynaHairSystemShape = "".join(cmds.listRelatives(f'{dynamicHairSystem}', shapes=True))
cmds.connectAttr(f'{settingsCTRL}.drag', f'{dynaHairSystemShape}.drag')
cmds.connectAttr(f'{settingsCTRL}.turbulence', f'{dynaHairSystemShape}.turbulenceStrength')
if not cmds.isConnected(f'{settingsCTRL}.wind_speed', f'{dynamicNucleus}.windSpeed'):
    cmds.connectAttr(f'{settingsCTRL}.wind_speed', f'{dynamicNucleus}.windSpeed')
