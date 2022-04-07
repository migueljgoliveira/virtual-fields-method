# -*- coding: mbcs -*-
#
# Abaqus/Viewer Release 2019 replay file
# Internal Version: 2018_09_24-20.41.51 157541
# Run by Miguel on Thu Apr  7 11:57:39 2022
#

# from driverUtils import executeOnCaeGraphicsStartup
# executeOnCaeGraphicsStartup()
#: Executing "onCaeGraphicsStartup()" in the site directory ...
from abaqus import *
from abaqusConstants import *
session.Viewport(name='Viewport: 1', origin=(0.0, 0.0), width=126.260406494141, 
    height=168.555557250977)
session.viewports['Viewport: 1'].makeCurrent()
session.viewports['Viewport: 1'].maximize()
from viewerModules import *
from driverUtils import executeOnCaeStartup
executeOnCaeStartup()
o2 = session.openOdb(name='Dogbone.odb')
#: Model: C:/Users/Miguel/Documents/GitHub/virtual-fields-method/input/Dogbone/Dogbone/Dogbone.odb
#: Number of Assemblies:         1
#: Number of Assembly instances: 0
#: Number of Part instances:     1
#: Number of Meshes:             1
#: Number of Element Sets:       5
#: Number of Node Sets:          6
#: Number of Steps:              1
session.viewports['Viewport: 1'].setValues(displayedObject=o2)
session.viewports['Viewport: 1'].makeCurrent()
session.viewports['Viewport: 1'].odbDisplay.display.setValues(plotState=(
    CONTOURS_ON_DEF, ))
session.viewports['Viewport: 1'].view.setValues(nearPlane=117.922, 
    farPlane=198.306, width=100.741, height=51.4614, viewOffsetX=1.30208, 
    viewOffsetY=-0.597089)
session.viewports['Viewport: 1'].odbDisplay.display.setValues(plotState=(
    CONTOURS_ON_UNDEF, ))
session.viewports['Viewport: 1'].view.setValues(nearPlane=118.891, 
    farPlane=197.337, width=45.4384, height=58.0937, viewOffsetX=-0.375305, 
    viewOffsetY=-0.752061)
session.viewports['Viewport: 1'].odbDisplay.setPrimaryVariable(
    variableLabel='COORD', outputPosition=NODAL, refinement=(INVARIANT, 
    'Magnitude'), )
session.viewports['Viewport: 1'].odbDisplay.setPrimaryVariable(
    variableLabel='COORD', outputPosition=NODAL, refinement=(COMPONENT, 
    'COOR1'), )
session.viewports['Viewport: 1'].odbDisplay.setPrimaryVariable(
    variableLabel='COORD', outputPosition=NODAL, refinement=(COMPONENT, 
    'COOR2'), )
session.viewports['Viewport: 1'].odbDisplay.setPrimaryVariable(
    variableLabel='PEEQ', outputPosition=INTEGRATION_POINT, )
#: 
#: Node: PART-1-1.26
#:                                         1             2             3        Magnitude
#: Base coordinates:                  8.33333e+00,  5.00000e+01,  0.00000e+00,      -      
#: No deformed coordinates for current plot.
#: 
#: Node: PART-1-1.27
#:                                         1             2             3        Magnitude
#: Base coordinates:                  1.66667e+01,  5.00000e+01,  0.00000e+00,      -      
#: No deformed coordinates for current plot.
#: 
#: Node: PART-1-1.26
#:                                         1             2             3        Magnitude
#: Base coordinates:                  8.33333e+00,  5.00000e+01,  0.00000e+00,      -      
#: No deformed coordinates for current plot.
#: 
#: Node: PART-1-1.25
#:                                         1             2             3        Magnitude
#: Base coordinates:                  0.00000e+00,  5.00000e+01,  0.00000e+00,      -      
#: No deformed coordinates for current plot.
#: 
#: Node: PART-1-1.26
#:                                         1             2             3        Magnitude
#: Base coordinates:                  8.33333e+00,  5.00000e+01,  0.00000e+00,      -      
#: No deformed coordinates for current plot.
#: 
#: Node: PART-1-1.27
#:                                         1             2             3        Magnitude
#: Base coordinates:                  1.66667e+01,  5.00000e+01,  0.00000e+00,      -      
#: No deformed coordinates for current plot.
#: 
#: Node: PART-1-1.28
#:                                         1             2             3        Magnitude
#: Base coordinates:                  2.50000e+01,  5.00000e+01,  0.00000e+00,      -      
#: No deformed coordinates for current plot.
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=0 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=1 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=2 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=1 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=2 )
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=19 )
