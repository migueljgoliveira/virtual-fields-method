# -*- coding: mbcs -*-
#
# Abaqus/Viewer Release 2019 replay file
# Internal Version: 2018_09_24-20.41.51 157541
# Run by Miguel on Wed Mar 30 16:30:45 2022
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
o2 = session.openOdb(name='H-Dogbone.odb')
#: Model: C:/Users/Miguel/Documents/GitHub/virtual-fields-method/input/H-Dogbone/H-Dogbone/H-Dogbone.odb
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
session.viewports['Viewport: 1'].odbDisplay.display.setValues(plotState=(
    CONTOURS_ON_UNDEF, ))
session.viewports['Viewport: 1'].odbDisplay.setPrimaryVariable(
    variableLabel='S', outputPosition=INTEGRATION_POINT, refinement=(COMPONENT, 
    'S11'), )
session.viewports['Viewport: 1'].odbDisplay.setPrimaryVariable(
    variableLabel='SDV1', outputPosition=INTEGRATION_POINT, )
dtm = session.odbs['C:/Users/Miguel/Documents/GitHub/virtual-fields-method/input/H-Dogbone/H-Dogbone/H-Dogbone.odb'].rootAssembly.datumCsyses['ASSEMBLY_PART-1-1_ORI-1']
session.viewports['Viewport: 1'].odbDisplay.basicOptions.setValues(
    transformationType=USER_SPECIFIED, datumCsys=dtm)
session.viewports['Viewport: 1'].odbDisplay.setPrimaryVariable(
    variableLabel='S', outputPosition=INTEGRATION_POINT, refinement=(INVARIANT, 
    'Mises'), )
session.viewports['Viewport: 1'].odbDisplay.setPrimaryVariable(
    variableLabel='S', outputPosition=INTEGRATION_POINT, refinement=(COMPONENT, 
    'S11'), )
session.viewports['Viewport: 1'].odbDisplay.setPrimaryVariable(
    variableLabel='LE', outputPosition=INTEGRATION_POINT, refinement=(
    INVARIANT, 'Max. In-Plane Principal'), )
session.viewports['Viewport: 1'].odbDisplay.setPrimaryVariable(
    variableLabel='LE', outputPosition=INTEGRATION_POINT, refinement=(
    COMPONENT, 'LE11'), )
session.viewports['Viewport: 1'].odbDisplay.setPrimaryVariable(
    variableLabel='LE', outputPosition=INTEGRATION_POINT, refinement=(
    COMPONENT, 'LE22'), )
session.viewports['Viewport: 1'].odbDisplay.setPrimaryVariable(
    variableLabel='LE', outputPosition=INTEGRATION_POINT, refinement=(
    COMPONENT, 'LE11'), )
session.viewports['Viewport: 1'].odbDisplay.basicOptions.setValues(
    transformationType=DEFAULT, datumCsys=None)
session.viewports['Viewport: 1'].odbDisplay.setPrimaryVariable(
    variableLabel='LE', outputPosition=INTEGRATION_POINT, refinement=(
    COMPONENT, 'LE22'), )
session.viewports['Viewport: 1'].odbDisplay.setPrimaryVariable(
    variableLabel='LE', outputPosition=INTEGRATION_POINT, refinement=(
    COMPONENT, 'LE11'), )
session.viewports['Viewport: 1'].odbDisplay.commonOptions.setValues(
    visibleEdges=NONE)
session.viewports['Viewport: 1'].odbDisplay.basicOptions.setValues(
    averagingThreshold=0)
session.viewports['Viewport: 1'].odbDisplay.contourOptions.setValues(
    contourStyle=CONTINUOUS, maxValue=0.256623, minValue=-0.000827371)
session.viewports['Viewport: 1'].odbDisplay.setPrimaryVariable(
    variableLabel='LE', outputPosition=INTEGRATION_POINT, refinement=(
    COMPONENT, 'LE22'), )
session.viewports['Viewport: 1'].odbDisplay.setPrimaryVariable(
    variableLabel='LE', outputPosition=INTEGRATION_POINT, refinement=(
    COMPONENT, 'LE12'), )
dtm = session.odbs['C:/Users/Miguel/Documents/GitHub/virtual-fields-method/input/H-Dogbone/H-Dogbone/H-Dogbone.odb'].rootAssembly.datumCsyses['ASSEMBLY_PART-1-1_ORI-1']
session.viewports['Viewport: 1'].odbDisplay.basicOptions.setValues(
    transformationType=USER_SPECIFIED, datumCsys=dtm)
session.viewports['Viewport: 1'].odbDisplay.basicOptions.setValues(
    transformationType=DEFAULT, datumCsys=None)
session.viewports['Viewport: 1'].odbDisplay.contourOptions.setValues(
    reversedContourLegendRange=ON, maxValue=0.0032101, minValue=-0.156412)
session.viewports['Viewport: 1'].odbDisplay.contourOptions.setValues(
    spectrum='Reversed rainbow', reversedContourLegendRange=OFF)
dtm = session.odbs['C:/Users/Miguel/Documents/GitHub/virtual-fields-method/input/H-Dogbone/H-Dogbone/H-Dogbone.odb'].rootAssembly.datumCsyses['ASSEMBLY_PART-1-1_ORI-1']
session.viewports['Viewport: 1'].odbDisplay.basicOptions.setValues(
    transformationType=USER_SPECIFIED, datumCsys=dtm)
session.viewports['Viewport: 1'].odbDisplay.setPrimaryVariable(
    variableLabel='S', outputPosition=INTEGRATION_POINT, refinement=(INVARIANT, 
    'Mises'), )
session.viewports['Viewport: 1'].odbDisplay.setPrimaryVariable(
    variableLabel='S', outputPosition=INTEGRATION_POINT, refinement=(COMPONENT, 
    'S11'), )
session.viewports['Viewport: 1'].odbDisplay.setPrimaryVariable(
    variableLabel='S', outputPosition=INTEGRATION_POINT, refinement=(COMPONENT, 
    'S22'), )
session.viewports['Viewport: 1'].odbDisplay.setPrimaryVariable(
    variableLabel='S', outputPosition=INTEGRATION_POINT, refinement=(COMPONENT, 
    'S33'), )
session.viewports['Viewport: 1'].odbDisplay.setPrimaryVariable(
    variableLabel='S', outputPosition=INTEGRATION_POINT, refinement=(COMPONENT, 
    'S22'), )
session.viewports['Viewport: 1'].odbDisplay.setPrimaryVariable(
    variableLabel='S', outputPosition=INTEGRATION_POINT, refinement=(COMPONENT, 
    'S11'), )
session.viewports['Viewport: 1'].odbDisplay.setPrimaryVariable(
    variableLabel='S', outputPosition=INTEGRATION_POINT, refinement=(INVARIANT, 
    'Third Invariant'), )
session.viewports['Viewport: 1'].odbDisplay.setPrimaryVariable(
    variableLabel='S', outputPosition=INTEGRATION_POINT, refinement=(COMPONENT, 
    'S11'), )
session.viewports['Viewport: 1'].odbDisplay.setPrimaryVariable(
    variableLabel='S', outputPosition=INTEGRATION_POINT, refinement=(COMPONENT, 
    'S22'), )
session.viewports['Viewport: 1'].odbDisplay.basicOptions.setValues(
    transformationType=DEFAULT, datumCsys=None)
session.viewports['Viewport: 1'].odbDisplay.setPrimaryVariable(
    variableLabel='S', outputPosition=INTEGRATION_POINT, refinement=(COMPONENT, 
    'S11'), )
session.viewports['Viewport: 1'].odbDisplay.setPrimaryVariable(
    variableLabel='S', outputPosition=INTEGRATION_POINT, refinement=(COMPONENT, 
    'S22'), )
session.viewports['Viewport: 1'].odbDisplay.contourOptions.setValues(
    spectrum='Rainbow', maxValue=249.269, minValue=-139.615)
session.viewports['Viewport: 1'].odbDisplay.setPrimaryVariable(
    variableLabel='S', outputPosition=INTEGRATION_POINT, refinement=(COMPONENT, 
    'S11'), )
session.viewports['Viewport: 1'].odbDisplay.setPrimaryVariable(
    variableLabel='S', outputPosition=INTEGRATION_POINT, refinement=(COMPONENT, 
    'S22'), )
session.viewports['Viewport: 1'].odbDisplay.contourOptions.setValues(
    maxAutoCompute=OFF, maxValue=150, minAutoCompute=OFF, minValue=-35)
session.viewports['Viewport: 1'].odbDisplay.setPrimaryVariable(
    variableLabel='S', outputPosition=INTEGRATION_POINT, refinement=(COMPONENT, 
    'S12'), )
session.viewports['Viewport: 1'].odbDisplay.contourOptions.setValues(
    maxAutoCompute=ON, minAutoCompute=ON)
session.viewports['Viewport: 1'].odbDisplay.contourOptions.setValues(
    spectrum='Reversed rainbow')
dtm = session.odbs['C:/Users/Miguel/Documents/GitHub/virtual-fields-method/input/H-Dogbone/H-Dogbone/H-Dogbone.odb'].rootAssembly.datumCsyses['ASSEMBLY_PART-1-1_ORI-1']
session.viewports['Viewport: 1'].odbDisplay.basicOptions.setValues(
    transformationType=USER_SPECIFIED, datumCsys=dtm)
dtm = session.odbs['C:/Users/Miguel/Documents/GitHub/virtual-fields-method/input/H-Dogbone/H-Dogbone/H-Dogbone.odb'].rootAssembly.datumCsyses['ASSEMBLY_PART-1-1_ORI-1']
