# =================================================================================================
# Colorize orange
# Davide Rossetto [davide(dot)ross93(at)gmail(dot)com]
# =================================================================================================

import maya.cmds as cmds

VERSION = '1.0.0'

COLOR = (1, 0.5, 0)

selection = cmds.ls(sl=True)

if len(selection) == 0:
    cmds.inViewMessage(amg='No object selected', pos='topLeft', fade=True)
    quit('No object selected')

for obj in selection:
    shape_name = '{}Shape'.format(obj)

    if not cmds.objExists(shape_name):
        continue
    
    cmds.setAttr('{}.overrideEnabled'.format(shape_name), True)
    cmds.setAttr('{}.overrideRGBColors'.format(shape_name), True)

    for channel, color_val in zip(('R', 'G', 'B'), COLOR):
        cmds.setAttr('{}Shape.overrideColor{}'.format(obj, channel), color_val)
    