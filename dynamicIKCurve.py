import maya.cmds as cmds
import maya.mel as mel

'''
For rig in Maya
Make a joint chain follow a simulated curve
'''

def getNiceName(pathObject):
    return pathObject.split('|')[len(pathObject.split('|'))-1]

selection = cmds.ls(long=True, orderedSelection=True)
firstJoint, *chainCTRL = selection

nameBase = f'{getNiceName(firstJoint)}'.replace('_00_JNT', '')

listChainIK = cmds.listRelatives(f'{firstJoint}', allDescendents=True, fullPath=True, type='joint')
listChainIK.append(f'{firstJoint}')
listChainIK.sort()

if not cmds.objExists('setupCloth_GRP'):
    cmds.group(empty=True, name='setupCloth_GRP')

'''create dynamic curve'''
nameHandle = f'{nameBase}_IK_HDL'
dynamicIk = cmds.ikHandle(name=nameHandle, numSpans=3, solver='ikSplineSolver', 
                startJoint=listChainIK[0], endEffector=listChainIK[len(listChainIK)-1])
#print(f'dynamicIk: {dynamicIk}')
dynamicHdl, dynamicEff, dynamicCurveIK = dynamicIk
#print(f'dynamicHdl: {dynamicHdl}')
#print(f'dynamicEff: {dynamicEff}')
#print(f'dynamicCurveIK: {dynamicCurveIK}')

cmds.rename(f'{dynamicEff}', f'{nameBase}_IK_EFF')
dynamicCurveIK = cmds.rename(f'{dynamicCurveIK}', f'{nameBase}_IK_curve')
dynamicCurveOg = "".join(cmds.duplicate(f'{dynamicCurveIK}', name=f'{nameBase}_baseDynamic_curve'))
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

transfoFollicle = cmds.rename(f'{transfoFollicle}', f'{nameBase}_follicle')
dynamicCurveMoov = cmds.rename(f'{dynamicCurveMoov}', f'{nameBase}_dynamic_curve')
dynamicHairSystem = cmds.rename(f'{dynamicHairSystem}', f'{nameBase}_hairSystem')
groupName = f'{nameBase}_setupDynamic_GRP'
groupSetupDynamic = cmds.group(f'{dynamicHairSystem}', f'{transfoFollicle}', f'{dynamicHdl}', name=groupName, parent='setupCloth_GRP')
groupCurveDynamic = cmds.group(f'{dynamicCurveMoov}', f'{dynamicCurveOg}', f'{dynamicCurveIK}', name=f'{nameBase}_curveDynamic_GRP',
                               parent=groupSetupDynamic)
#cmds.parent(f'{dynamicHdl}', f'{groupSetup}')
cmds.delete('hairSystem*OutputCurves')

cmds.blendShape(f'{dynamicCurveMoov}', f'{dynamicCurveIK}', weight=[0, 1])
