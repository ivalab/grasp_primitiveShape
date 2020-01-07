The various source code items can be found on https://github.com/CoppeliaRobotics
Clone each required repository with:

git clone --recursive https://github.com/CoppeliaRobotics/repositoryName

Use following directory structure:

v_rep
    |__ v_rep
    |__ dynamicsPlugin
    |__ meshCalculationPlugin
    |__ programming
                  |__ include
                  |__ common
                  |__ v_repMath
                  |__ remoteApi
                  |__ externalIk
                  |__ remoteApiBindings
                  |__ b0RemoteApiBindings
                  |__ v_repExtCodeEditor
                  |__ v_repExtRemoteApi
                  |__ v_repExtJoystick
                  |__ v_repExtCam
                  |__ v_repExtURDF
                  |__ v_repExtSDF
                  |__ v_repExtCollada
                  |__ v_repExtRmlType2
                  |__ v_repExtRRS1
                  |__ v_repExtMtb
                  |__ v_repExtCustomUI
                  |__ v_repExtOMPL
                  |__ v_repExtICP
                  |__ v_repExtSurfaceReconstruction
                  |__ v_repExtLuaCommander
                  |__ v_repExtPluginSkeleton
                  |__ v_repExtPluginSkeletonNG
                  |__ v_repExtCHAI3D
                  |__ v_repExtConvexDecompose
                  |__ v_repExtPovRay
                  |__ v_repExtQhull
                  |__ v_repExtVision
                  |__ v_repExtExternalRenderer
                  |__ v_repExtLuaRemoteApiClient
                  |__ v_repExtBlueZero
                  |__ v_repExtImage
                  |__ v_repExtOctomap
                  |__ v_repExtDataFlow
                  |__ v_repExtBubbleRob
                  |__ v_repExtK3
                  |__ v_repExtAssimp
                  |__ v_repExtOpenMesh
                  |__ v_repExtOpenGL3Renderer
                  |__ externalIkDemo1
                  |__ externalIkDemo2
                  |__ externalIkDemo3
                  |__ bubbleRobClient
                  |__ bubbleRobServer
                  |__ b0_bubbleRob
                  |__ rcsServer
                  |__ mtbServer
                  |__ v_repLuaLibrary

ros_packages
           |__ v_repExtRosInterface
           |__ ros_bubble_rob2
           |__ vrep_plugin_skeleton
           |__ vrep_skeleton_msg_and_srv


Following are the main Items:
-----------------------------

-   'v_rep' (requires 'include', 'common' and 'v_repMath'):         
    https://github.com/CoppeliaRobotics/v_rep

-   'v_repClientApplication' (requires 'include' and 'common'):
    https://github.com/CoppeliaRobotics/v_repClientApplication


Various common items:
---------------------

-   'v_repMath':
    https://github.com/CoppeliaRobotics/v_repMath

-   'common' (requires 'include'):
    https://github.com/CoppeliaRobotics/common

-   'include' (requires 'common'):
    https://github.com/CoppeliaRobotics/include

-   'remoteApi' (requires 'include' and 'common'):
    https://github.com/CoppeliaRobotics/remoteApi

-   'externalIk' (requires 'include', 'common' and 'v_repMath'):
    https://github.com/CoppeliaRobotics/externalIk

-   'v_repStubsGen' (submodule):
    https://github.com/CoppeliaRobotics/v_repStubsGen

-   'v_repPlusPlus' (submodule):
    https://github.com/CoppeliaRobotics/v_repPlusPlus

-   'remoteApiBindings' (requires 'remoteApi' if libs need to be rebuilt)
    https://github.com/CoppeliaRobotics/remoteApiBindings

-   'b0RemoteApiBindings' (requires 'bluezero' if libs need to be rebuilt)
    https://github.com/CoppeliaRobotics/b0RemoteApiBindings

Major plugins:
--------------

-   'dynamicsPlugin' (requires 'include', 'common' and 'v_repMath'):
    https://github.com/CoppeliaRobotics/dynamicsPlugin

-   'meshCalculationPlugin' (requires 'include', 'common' and 'v_repMath'):
    https://github.com/CoppeliaRobotics/meshCalculationPlugin

-   'v_repExtCodeEditor' (requires 'include', 'common' and 'QScintilla'):
    https://github.com/CoppeliaRobotics/meshCalculationPlugin


Various plugins:		
----------------

-   'v_repExtJoystick' (requires 'include' and 'common'):
    https://github.com/CoppeliaRobotics/v_repExtJoystick (Windows only)

-   'v_repExtCam' (requires 'include' and 'common'):
    https://github.com/CoppeliaRobotics/v_repExtCam (Windows only)

-   'v_repExtUrdf' (requires 'include', 'common' and 'v_repMath'):
    https://github.com/CoppeliaRobotics/v_repExtUrdf

-   'v_repExtCollada' (requires 'include', 'common' and 'v_repMath'):
    https://github.com/CoppeliaRobotics/v_repExtCollada

-   'v_repExtSDF' (requires 'include' and 'common' and 'v_repMath'):
    https://github.com/CoppeliaRobotics/v_repExtSDF

-   'v_repExtRmlType2' (requires 'include' and 'common'):
    https://github.com/CoppeliaRobotics/v_repExtRmlType2

-   'v_repExtRRS1' (requires 'include' and 'common'):
    https://github.com/CoppeliaRobotics/v_repExtRRS1

-   'v_repExtMtb' (requires 'include' and 'common'):
    https://github.com/CoppeliaRobotics/v_repExtMtb

-   'v_repExtCustomUI' (requires 'include' and 'common'):
    https://github.com/CoppeliaRobotics/v_repExtCustomUI

-   'v_repExtOMPL' (requires 'include' and 'common'):
    https://github.com/CoppeliaRobotics/v_repExtOMPL

-   'v_repExtICP' (requires 'include' and 'common'):
    https://github.com/CoppeliaRobotics/v_repExtICP

-   'v_repExtSurfaceReconstruction' (requires 'include' and 'common'):
    https://github.com/CoppeliaRobotics/v_repExtSurfaceReconstruction

-   'v_repExtRosInterface' (requires 'include' and 'common'):
    https://github.com/CoppeliaRobotics/v_repExtRosInterface

-   'v_repExtLuaCommander' (requires 'include' and 'common'):
    https://github.com/CoppeliaRobotics/v_repExtLuaCommander

-   'v_repExtPluginSkeleton' (requires 'include' and 'common'):
    https://github.com/CoppeliaRobotics/v_repExtPluginSkeleton

-   'v_repExtPluginSkeletonNG' (requires 'include' and 'common'):
    https://github.com/CoppeliaRobotics/v_repExtPluginSkeletonNG

-   'vrep_plugin_skeleton' (requires 'include' and 'common'):
    https://github.com/CoppeliaRobotics/vrep_plugin_skeleton

-   'v_repExtCHAI3D' (requires 'include' and 'common'):
    https://github.com/CoppeliaRobotics/v_repExtCHAI3D

-   'v_repExtConvexDecompose' (requires 'include' and 'common'):
    https://github.com/CoppeliaRobotics/v_repExtConvexDecompose

-   'v_repExtPovRay' (requires 'include' and 'common'):
    https://github.com/CoppeliaRobotics/v_repExtPovRay

-   'v_repExtQhull' (requires 'include' and 'common'):
    https://github.com/CoppeliaRobotics/v_repExtQhull

-   'v_repExtOpenMesh' (requires 'include' and 'common'):
    https://github.com/CoppeliaRobotics/v_repExtOpenMesh

-   'v_repExtRemoteApi' (requires 'include' and 'common'):
    https://github.com/CoppeliaRobotics/v_repExtRemoteApi

-   'v_repExtVision' (requires 'include' and 'common'):
    https://github.com/CoppeliaRobotics/v_repExtVision

-   'v_repExtExternalRenderer' (requires 'include' and 'common'):
    https://github.com/CoppeliaRobotics/v_repExtExternalRenderer

-   'v_repExtLuaRemoteApiClient' (requires 'include' and 'common'):
    https://github.com/CoppeliaRobotics/v_repExtLuaRemoteApiClient

-   'v_repExtBlueZero' (requires 'include' and 'common'):
    https://github.com/CoppeliaRobotics/v_repExtBlueZero

-   'v_repExtImage' (requires 'include' and 'common'):
    https://github.com/CoppeliaRobotics/v_repExtImage

-   'v_repExtOctomap' (requires 'include' and 'common'):
    https://github.com/CoppeliaRobotics/v_repExtOctomap

-   'v_repExtDataFlow' (requires 'include' and 'common'):
    https://github.com/CoppeliaRobotics/v_repExtDataFlow

-   'v_repExtBubbleRob' (requires 'include' and 'common'):
    https://github.com/CoppeliaRobotics/v_repExtBubbleRob

-   'v_repExtK3' (requires 'include' and 'common'):
    https://github.com/CoppeliaRobotics/v_repExtK3

-   'v_repExtOpenGL3Renderer' (requires 'include' and 'common'):
    https://github.com/stepjam/v_repExtOpenGL3Renderer


Various other repositories:		
---------------------------

-   'externalIkDemo1' (requires 'include', 'common', 'externalIk' and 'remoteApi'):
    https://github.com/CoppeliaRobotics/externalIkDemo1

-   'externalIkDemo2' (requires 'include', 'common', 'externalIk' and 'remoteApi'):
    https://github.com/CoppeliaRobotics/externalIkDemo2

-   'externalIkDemo3' (requires 'include', 'common', 'externalIk' and 'remoteApi'):
    https://github.com/CoppeliaRobotics/externalIkDemo3

-   'bubbleRobClient' (requires 'include', 'common' and 'remoteApi'):
    https://github.com/CoppeliaRobotics/bubbleRobClient

-   'bubbleRobServer' (requires 'include' and 'common'):
    https://github.com/CoppeliaRobotics/bubbleRobServer
    
-   'b0_bubbleRob' (requires 'include' and 'common'):
    https://github.com/CoppeliaRobotics/b0_bubbleRob

-   'rcsServer' (requires 'include' and 'common'):
    https://github.com/CoppeliaRobotics/rcsServer

-   'mtbServer' (requires 'include' and 'common'):
    https://github.com/CoppeliaRobotics/mtbServer

-   'ros_bubble_rob2'
    https://github.com/CoppeliaRobotics/ros_bubble_rob2

-   'vrep_skeleton_msg_and_srv'
    https://github.com/CoppeliaRobotics/vrep_skeleton_msg_and_srv

-   'v_repLuaLibrary':
    https://github.com/CoppeliaRobotics/v_repLuaLibrary

-   'PyRep':
    https://github.com/stepjam/PyRep
