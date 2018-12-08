# =================================================================================================
# Connect rotation
# Davide Rossetto [davide(dot)ross93(at)gmail(dot)com]
# =================================================================================================

import maya.cmds as cmds

VERSION = '1.0.0'

sel = cmds.ls(sl=True)

if len(sel) != 2:
    quit('Selection error')

cmds.connectAttr('{}.rotate'.format(sel[0]), '{}.rotate'.format(sel[1]))
