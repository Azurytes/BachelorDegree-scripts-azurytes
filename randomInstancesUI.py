#randomInstancesUI.py
'''
For Maya
Create instance of 1st selection
2nd selection can establish a ground where instances are placed
Based on SDK learning channel intro videos: https://www.youtube.com/watch?v=kUkk7rcwtI8
'''

import maya.cmds as cmds
import random
import sys
import functools

#random.seed( 1234 )

result = cmds.ls( orderedSelection=True )

print (f'result: {result}')

if len(result) == 0:
    
    print('Veuillez sélectionner un ou plusieurs objets')
        
    sys.exit()
    
transformName = result[0]

if len(result) >= 2:
    sol = result[1]

'''create group that will have instances'''
instanceGroupName = cmds.group( empty=True, name=transformName + '_instance_grp##' )
        
    
def createUI( pWindowTitle, pApplyCallback ):
    '''create window settings'''

    windowID = 'randomInstancesID'

    if cmds.window( windowID, exists=True ):
        cmds.deleteUI( windowID )
    
    cmds.window( windowID, title=pWindowTitle, sizeable=False, resizeToFitChildren=True )

    cmds.rowColumnLayout( numberOfColumns=3,columnWidth=[ (1,125), (2,60), (3,60) ],
                          columnOffset=[ (1,'right',3) ] )
    
    cmds.text( label='Random seed: ' )
    
    randomSeedField = cmds.intField( value=1234 )
    cmds.separator( h=10, style='none' )

    cmds.text( label='Number of instances: ' )

    numberInstancesField = cmds.intField( value=50, min=1 )
    cmds.separator( h=10, style='none' )

    cmds.text( label='X axis area: ' )

    xMinField = cmds.intField( value = -10 )
    xMaxField = cmds.intField( value = 10 )

    cmds.text( label='Y axis area: ' )

    yMinField = cmds.intField( value = 0 )
    yMaxField = cmds.intField( value = 0 )

    cmds.text( label='Z axis area: ' )

    zMinField = cmds.intField( value = -10 )
    zMaxField = cmds.intField( value = 10 )

    cmds.text( label='Scale: ' )

    scaleMinField = cmds.floatField( value = 0.8, pre=3 )
    scaleMaxField = cmds.floatField( value = 1.2, pre=3 )

    if len(result) >= 2:
        cmds.text( label='Match Ground Rot: ' )
        
        matchRotField = cmds.intSlider(value = 0, max=1, min=0)
        cmds.text(label='No--Yes')

        cmds.separator(h=10, style='none' )
    
    cmds.separator( h=10, style='none' )
    cmds.separator( h=10, style='none' )
    cmds.separator( h=10, style='none' )

    if len(result) == 1:
        cmds.button( label='Apply', command=functools.partial( pApplyCallback, randomSeedField,
                                                               numberInstancesField, xMinField, xMaxField, yMinField,
                                                               yMaxField, zMinField, zMaxField, scaleMinField,
                                                               scaleMaxField ) )
    else:
        cmds.button( label='Apply', command=functools.partial( pApplyCallback, randomSeedField,
                                                               numberInstancesField, xMinField, xMaxField, yMinField,
                                                               yMaxField, zMinField, zMaxField, scaleMinField,
                                                               scaleMaxField, matchRotField ) )


    def cancelCallback( *pArgs ):
        if cmds.window( windowID, exists=True ):
            cmds.deleteUI( windowID )
        
    cmds.button( label='Cancel', command=cancelCallback )

    cmds.showWindow()
    

def applyCallback( pRandomSeedField, pNumberInstancesField, pXMinField, pXMaxField,
                   pYMinField, pYMaxField, pZMinField, pZMaxField, pScaleMinField,
                   pScaleMaxField, *pArgs ):

    print ('Apply button pressed')
    
    userRandomSeed = cmds.intField( pRandomSeedField, query=True, value=True )
    numberInstances = cmds.intField( pNumberInstancesField, query=True, value=True )
    xMin = cmds.intField( pXMinField, query=True, value=True )
    xMax = cmds.intField( pXMaxField, query=True, value=True )
    yMin = cmds.intField( pYMinField, query=True, value=True )
    yMax = cmds.intField( pYMaxField, query=True, value=True )
    zMin = cmds.intField( pZMinField, query=True, value=True )
    zMax = cmds.intField( pZMaxField, query=True, value=True )
    scaleMin = cmds.floatField( pScaleMinField, query=True, value=True )
    scaleMax = cmds.floatField( pScaleMaxField, query=True, value=True )

    if pArgs[0]:
        #print(f'pArgs: {pArgs}')
        pMatchRotField, *_ = pArgs
        #print(f'MatchRotField: {pMatchRotField}')
        matchRot = cmds.intSlider( pMatchRotField, query=True, value=True )
    
    random.seed( userRandomSeed )

    for i in range( 0, numberInstances ):
        '''create instances'''

        instanceResult = cmds.instance( transformName, name=transformName + '_instance##' )

        cmds.parent( instanceResult, instanceGroupName )

        #print ('instanceResult: ' + str( instanceResult ))

        x = random.uniform( xMin, xMax )
        y = random.uniform( yMin, yMax )
        z = random.uniform( zMin, zMax )

        cmds.move( x, y, z, instanceResult )

        yRot = random.uniform( 0, 360 )

        cmds.rotate(0, yRot, 0, instanceResult )

        '''avoir mis le pivot à la base du premier objet pour que ça marche correctement'''

        scalingFactor = random.uniform( scaleMin, scaleMax )

        cmds.scale( scalingFactor, scalingFactor, scalingFactor, instanceResult )

    if 'matchRot' in locals():
        if matchRot == 0:
            '''don't rotate instances'''
    
            cmds.matchTransform ( instanceGroupName, sol, rot = False, pos = True )
    
        else:
            '''rotate instances'''
    
            cmds.matchTransform ( instanceGroupName, sol, rot = True, pos = True )

    if cmds.window( 'randomInstancesID', exists=True ):
        ''' delete window'''
        cmds.deleteUI( 'randomInstancesID' )
        
createUI( 'Random Instances', applyCallback )
