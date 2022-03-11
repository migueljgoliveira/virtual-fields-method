# -*- coding: mbcs -*-
#
# Abaqus/Viewer Release 2019 replay file
# Internal Version: 2018_09_24-20.41.51 157541
# Run by Miguel on Fri Mar 11 11:15:04 2022
#

# from driverUtils import executeOnCaeGraphicsStartup
# executeOnCaeGraphicsStartup()
#: Executing "onCaeGraphicsStartup()" in the site directory ...
from abaqus import *
from abaqusConstants import *
session.Viewport(name='Viewport: 1', origin=(0.0, 0.0), width=134.494781494141, 
    height=168.555557250977)
session.viewports['Viewport: 1'].makeCurrent()
session.viewports['Viewport: 1'].maximize()
from viewerModules import *
from driverUtils import executeOnCaeStartup
executeOnCaeStartup()
o2 = session.openOdb(name='Double-Notched-2D.odb')
#: Model: C:/Users/Miguel/Documents/GitHub/virtual-fields-method/input/Double-Notched-2D/Double-Notched-2D.odb
#: Number of Assemblies:         1
#: Number of Assembly instances: 0
#: Number of Part instances:     1
#: Number of Meshes:             1
#: Number of Element Sets:       6
#: Number of Node Sets:          6
#: Number of Steps:              1
session.viewports['Viewport: 1'].setValues(displayedObject=o2)
session.viewports['Viewport: 1'].makeCurrent()
leaf = dgo.LeafFromElementSets(elementSets=('ROI', ))
session.viewports['Viewport: 1'].odbDisplay.displayGroup.replace(leaf=leaf)
session.viewports['Viewport: 1'].view.setValues(nearPlane=374.795, 
    farPlane=430.19, width=77.0924, height=38.6351, viewOffsetX=0.926238, 
    viewOffsetY=0.477636)
session.viewports['Viewport: 1'].odbDisplay.display.setValues(plotState=(
    CONTOURS_ON_DEF, ))
session.viewports['Viewport: 1'].odbDisplay.display.setValues(plotState=(
    CONTOURS_ON_UNDEF, ))
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=107 )
session.viewports['Viewport: 1'].odbDisplay.setPrimaryVariable(
    variableLabel='S', outputPosition=INTEGRATION_POINT, refinement=(COMPONENT, 
    'S11'), )
dtm = session.odbs['C:/Users/Miguel/Documents/GitHub/virtual-fields-method/input/Double-Notched-2D/Double-Notched-2D.odb'].rootAssembly.datumCsyses['ASSEMBLY_PART-1-1_ORI-1']
session.viewports['Viewport: 1'].odbDisplay.basicOptions.setValues(
    transformationType=USER_SPECIFIED, datumCsys=dtm)
session.viewports['Viewport: 1'].odbDisplay.display.setValues(plotState=(
    ORIENT_ON_DEF, ))
session.viewports['Viewport: 1'].odbDisplay.display.setValues(plotState=(
    CONTOURS_ON_UNDEF, ))
session.viewports['Viewport: 1'].odbDisplay.setPrimaryVariable(
    variableLabel='S', outputPosition=INTEGRATION_POINT, refinement=(COMPONENT, 
    'S22'), )
session.viewports['Viewport: 1'].odbDisplay.setPrimaryVariable(
    variableLabel='S', outputPosition=INTEGRATION_POINT, refinement=(COMPONENT, 
    'S11'), )
