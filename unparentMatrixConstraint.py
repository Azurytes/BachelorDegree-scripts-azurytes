#unparentMatrixConstraint.py
import maya.cmds as cmds

'''
Use Maya nodal system
Unparent constraint between joints and contollers using matrices
Only work if the setup is the same done by parentMatrixConstraint.py
'''

def unparentMatrixConstraint(ctrl):
    try:
        ctrlParent, jntChild, *_ = ctrl
    except ValueError:
        print('OOPS ! Need at least 2 objects selected')
        raise
        
    if not cmds.objExists(f'{jntChild}_multMatrix'):
        return print('No matrixConstraint to undo')
  
    print(f'Ctrl : {ctrlParent}')
    print(f'Jnt : {jntChild}')
    
    if cmds.objectType(f'{jntChild}', isType='joint'):
        
        resultTransfer = cmds.createNode('decomposeMatrix', name=f'{jntChild}_decomposeMatrix')
        cmds.connectAttr(f'{jntChild}_multMatrix.matrixSum', f'{resultTransfer}.inputMatrix')
        for coordinate in ('Translate', 'Rotate', 'Scale', 'Shear'):
            lowerCoord = coordinate.lower()
            cmds.connectAttr(f'{resultTransfer}.output{coordinate}', f'{jntChild}.{lowerCoord}')
            cmds.disconnectAttr(f'{resultTransfer}.output{coordinate}', f'{jntChild}.{lowerCoord}')
        
        cmds.disconnectAttr(f'{jntChild}_multMatrix.matrixSum', f'{jntChild}.offsetParentMatrix')
        matrixZero = iter([1.0, 0.0, 0.0, 0.0, 
                       0.0, 1.0, 0.0, 0.0, 
                       0.0, 0.0, 1.0, 0.0, 
                       0.0, 0.0, 0.0, 1.0])
        cmds.setAttr(f'{jntChild}.offsetParentMatrix', matrixZero, type='matrix')
        cmds.makeIdentity(f'{jntChild}', apply=True, t=1, r=1, s=1, n=0, pn=1)
        cmds.delete(resultTransfer)
    else:
        cmds.delete(f'{jntChild}_multMatrix')
    
unparentMatrixConstraint(cmds.ls(os=True))
