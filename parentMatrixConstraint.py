#parentMatrixConstraint.py
import maya.cmds as cmds

'''
Use Maya nodal system
Need Maya 2020 or + for Offset Parent Matrix
Parent constraint joints to contollers using matrices
Note: You can't bake animation on joints that use this constraint
'''

def parentMatrixConstraint(ctrl):
    try:
        ctrlParent, jntChild, *_ = ctrl
    except ValueError:
        print('OOPS ! Need at least 2 objects selected')
        raise
        
    for mathNode in ('multMatrix', 'decomposeMatrix', 'plusMinusAverage'):
        if cmds.objExists(f'{jntChild}_{mathNode}'):
            print('That constraint have been done before')
            cmds.delete(f'{jntChild}_{mathNode}')
    mult = cmds.createNode("multMatrix", name=f'{jntChild}_multMatrix')
    decompose = cmds.createNode("decomposeMatrix", name=f'{jntChild}_decomposeMatrix')
    subtractRotation = cmds.createNode("plusMinusAverage", name=f'{jntChild}_plusMinusAverage')
    cmds.setAttr(f"{subtractRotation}.operation", 2)
    
    print(f'Ctrl : {ctrlParent}')
    print(f'Jnt : {jntChild}')
    jntParent = "".join(cmds.listRelatives(jntChild, parent=True))
    print(f'Parent Jnt : {jntParent}')
    
    '''connections for multMatrix'''
    
    cmds.connectAttr(f"{ctrlParent}.worldMatrix[0]", f"{mult}.matrixIn[0]")
    cmds.connectAttr(f"{jntParent}.worldInverseMatrix[0]", f"{mult}.matrixIn[1]")
    
    #cmds.connectAttr(f'{mult}.matrixSum', f'{jntChild}.offsetParentMatrix', force=True)
    '''connections for decomposeMatrix'''
    cmds.connectAttr(f'{mult}.matrixSum', f'{decompose}.inputMatrix')
    cmds.connectAttr(f'{ctrlParent}.rotateOrder', f'{decompose}.inputRotateOrder')
    for coordinates in ('Translate', 'Scale', 'Shear'):
        coordLower = coordinates.lower()
        print(f'coordinates: {coordLower}')
        cmds.connectAttr(f'{decompose}.output{coordinates}', f'{jntChild}.{coordLower}', force=True)
        
    '''subtract current joint orient to the constraint rotation, so there is no offset'''
    if cmds.objectType(f'{jntChild}', isType='joint'):
        cmds.connectAttr(f'{decompose}.outputRotate', f'{subtractRotation}.input3D[0]')
        cmds.connectAttr(f'{jntChild}.jointOrient', f'{subtractRotation}.input3D[1]')
        cmds.connectAttr(f'{subtractRotation}.output3D', f'{jntChild}.rotate')
    
parentMatrixConstraint(cmds.ls(os=True))
