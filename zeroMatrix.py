#zeroMatrix.py
import maya.cmds as cmds

'''
For Maya 2020 or +
Reset object's transform attributes
by transfering them to Offset Parent Matrix
'''

for ctrl in cmds.ls(selection=True):
    
    matrixSelect = cmds.getAttr(f'{ctrl}.matrix')

    matrixZero = [1.0, 0.0, 0.0, 0.0, 
                  0.0, 1.0, 0.0, 0.0, 
                  0.0, 0.0, 1.0, 0.0, 
                  0.0, 0.0, 0.0, 1.0]
    #print(list(matrixZero))
                  
    if matrixSelect != matrixZero :
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
