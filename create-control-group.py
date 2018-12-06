# =================================================================================================
# Create control group
# Davide Rossetto [davide(dot)ross93(at)gmail(dot)com]
# =================================================================================================

import maya.cmds as cmds

VERSION = '1.0.0'

selection = cmds.ls(sl=True)

if len(selection) > 0:
    sel_obj = selection[0]
    obj_type = cmds.objectType(sel_obj)
    
    if obj_type == 'joint':
        ctrl_name = sel_obj.replace('_JNT', '')
        ctrl = cmds.circle(nr=(1, 0, 0), c=(0, 0, 0), n='{}_CTRL'.format(ctrl_name))
        ctrl_grp = cmds.group(ctrl, n='{}_CTRL_GRP'.format(ctrl_name))
        cmds.matchTransform(ctrl_grp, sel_obj)
    else:
        cmds.inViewMessage(amg='Selected object is not a joint', pos='topLeft', fade=True)
else:
    cmds.inViewMessage(amg='No object selected', pos='topLeft', fade=True)
