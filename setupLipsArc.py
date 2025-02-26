#setupLipsArc.py
import maya.cmds as cmds

'''
For lips rigging on Maya
Make nodal connections between the controller and joint
to generate an arc when controller move
'''

def setupLips(lipSelection):
    
    '''get controller and joints name'''
    lipCTRL, lipJNT, *_ = lipSelection
    if not cmds.objectType(lipJNT, isType='joint'):
        print('OOPS! Second selection is the joint to constrain')
        return
    lipRoot = ''.join(cmds.listRelatives(f'{lipJNT}', parent=True))
    lipCTRL_parent = ''.join(cmds.listRelatives(f'{lipCTRL}', parent=True))
    print(f'lipRoot: {lipRoot}')
    print(f'parent of controller: {lipCTRL_parent}')
    offsetValue = cmds.getAttr(f'{lipJNT}.translateX')
    nameClean = lipCTRL.replace('_CTRL','')
    
    '''create attributs in controller'''
    if 'gradient' not in cmds.listAttr(f'{lipCTRL}'):
        cmds.addAttr(f'{lipCTRL}', longName='ARC_SETTINGS', attributeType='enum', enumName='----------:o')
        cmds.setAttr(f'{lipCTRL}.ARC_SETTINGS', channelBox=True, lock=True)
        cmds.addAttr(f'{lipCTRL}', longName='gradient', attributeType='long', defaultValue=1)
        cmds.addAttr(f'{lipCTRL}', longName='offset', attributeType='float', defaultValue=offsetValue)
        cmds.addAttr(f'{lipCTRL}', longName='movement', attributeType='long', defaultValue=30, minValue=0)
        cmds.addAttr(f'{lipCTRL}', longName='axe_horizontal', attributeType='enum', enumName='X:Y:Z',
                    defaultValue=2)
        cmds.addAttr(f'{lipCTRL}', longName='axe_vertical', attributeType='enum', enumName='X:Y:Z',
                    defaultValue=1)
        
        for attributeTitle in ('gradient', 'offset', 'movement', 'axe_horizontal', 'axe_vertical'):
            cmds.setAttr(f'{lipCTRL}.{attributeTitle}', keyable=True)
        
    '''get axes'''
    transHorizValue = cmds.getAttr(f'{lipCTRL}.axe_horizontal', asString=True)
    print(f'Trans Horizontal: {transHorizValue}')
    transVertiValue = cmds.getAttr(f'{lipCTRL}.axe_vertical', asString=True)
    print(f'Trans Vertical: {transVertiValue}')
    
    for axeRef in ('X', 'Y', 'Z'):
        if transVertiValue == axeRef:
            rotHorizValue = axeRef
            print(f'Rot Horizontal: {rotHorizValue}')
        elif transHorizValue == axeRef:
            rotVertiValue = axeRef
            print(f'Rot Vertical: {rotVertiValue}')
        else:
            depthValue = axeRef
            print(f'Depth axis: {depthValue}')
    
    '''delete existing locator if script already been used'''
    if cmds.objExists(f'{nameClean}_LOC_offset'):
        cmds.delete(f'{nameClean}_LOC_offset')
        
    '''position locator on end joint'''
    print(f'nameClean: {nameClean}')
    lipLOC = ''.join(cmds.spaceLocator(name=f'{nameClean}_LOC'))
    lipLOC_group = cmds.group(f'{lipLOC}', name=f'{lipLOC}_offset')
    cmds.matchTransform(f'{lipLOC_group}',f'{lipCTRL}', position=True, rotation=True)
    cmds.parent(f'{lipLOC_group}', f'{lipCTRL_parent}')
    cmds.pointConstraint(f'{lipCTRL}', f'{lipLOC}')
    cmds.setAttr(f'{lipLOC}.visibility', 0)
    
    '''delete utility nodes if script have already been used'''
    for utilityName in ('orient_multi', 'orient_reverse', 'trans_multi', 'offset_PMA',
                      'invert_reverse', 'gradient_multi'):
        if cmds.objExists(f'{nameClean}_{utilityName}'):
            cmds.delete(f'{nameClean}_{utilityName}')
            
    '''setup all utility nodes'''
    orientMulti = cmds.createNode('multiplyDivide', name=f'{nameClean}_orient_multi')
    print(f'orientMulti: {orientMulti}')
    reverseOrientValue = cmds.createNode('multiplyDivide', name=f'{nameClean}_orient_reverse')
    cmds.setAttr(f'{reverseOrientValue}.input2X', -1)
    #cmds.setAttr(f'{orientMulti}.input2X', -30)
    #cmds.setAttr(f'{orientMulti}.input2Y', 30)
    
    transMulti = cmds.createNode('multiplyDivide', name=f'{nameClean}_trans_multi')
    
    offsetPMA = cmds.createNode('plusMinusAverage', name=f'{nameClean}_offset_PMA')
    #cmds.setAttr(f'{offsetPMA}.input1D[1]', offsetValue)
    cmds.setAttr(f'{offsetPMA}.operation', 2)
    
    invertReverse = cmds.createNode('multiplyDivide', name=f'{nameClean}_invert_reverse')
    cmds.setAttr(f'{invertReverse}.input2X', -1)
    
    gradientMulti = cmds.createNode('multiplyDivide', name=f'{nameClean}_gradient_multi')
    #cmds.setAttr(f'{gradientMulti}.input2X', 1)
    
    '''make connections'''
    cmds.connectAttr(f'{lipCTRL}.movement', f'{reverseOrientValue}.input1X')
    cmds.connectAttr(f'{reverseOrientValue}.outputX', f'{orientMulti}.input2X')
    cmds.connectAttr(f'{lipCTRL}.movement', f'{orientMulti}.input2Y')
    cmds.connectAttr(f'{lipLOC}.translate{transHorizValue}', f'{orientMulti}.input1X')
    cmds.connectAttr(f'{lipLOC}.translate{transVertiValue}', f'{orientMulti}.input1Y')
    cmds.connectAttr(f'{orientMulti}.outputX', f'{lipRoot}.rotate{rotHorizValue}')
    cmds.connectAttr(f'{orientMulti}.outputY', f'{lipRoot}.rotate{rotVertiValue}')
    
    cmds.connectAttr(f'{lipCTRL}.gradient', f'{gradientMulti}.input2X')
    cmds.connectAttr(f'{lipLOC}.translate{transHorizValue}', f'{gradientMulti}.input1X')
    cmds.connectAttr(f'{gradientMulti}.outputX', f'{transMulti}.input2X')
    cmds.connectAttr(f'{lipLOC}.translate{transHorizValue}', f'{transMulti}.input1X')
    
    cmds.connectAttr(f'{transMulti}.outputX', f'{offsetPMA}.input1D[0]')
    cmds.connectAttr(f'{lipCTRL}.offset', f'{offsetPMA}.input1D[1]')
    
    cmds.connectAttr(f'{offsetPMA}.output1D', f'{invertReverse}.input1X')
    cmds.connectAttr(f'{invertReverse}.outputX', f'{lipJNT}.translate{depthValue}')
    
setupLips(cmds.ls(orderedSelection=True))
