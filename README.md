# Bachelor's Degree scripts

Compilation of scripts I wrote along my 3D courses and my internship between 2020 and 2024.<br>
Most of them are for automating rigging task. Every Python script uses Maya API.

It includes: 
- *BubbleNiveauVector.cs* : move 3 bubbles in a spirit level for Unity using vector projection.
- *dynamicIKCurve.py* : create a IK chain of joints following a curve that can be simulated.
- *parentMatrixConstraint.py* : constrain a joint to a controller by using it's transformation matrix (need Maya 2020 or +).
- *randomInstancesUI.py* : create instances of a selected object and scatter them on a defined distance.
- *setupLipsArc.py* : setup nodal connections for a set of selected controller and joint so that the joint follow an arc around a root.
- *switchFkIkDynamic.py* : Setting up FK/IK of a selected joint chain and IK can follow a simulated curve or not.
- *unparentMatrixConstraint.py* : remove nodal connections of parentMatrixConstraint.py and reset selection transformation matrix (need Maya 2020 or +).
- *zeroMatrix.py* : reset transformation matrix to zero by transfering values to Parent Offset Matrix (need Maya 2020 or +).
