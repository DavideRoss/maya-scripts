# =================================================================================================
# Create IK/FK switch
# Davide Rossetto [davide(dot)ross93(at)gmail(dot)com]
# =================================================================================================

import maya.cmds as cmds

VERSION = '1.0.0'

selection = cmds.ls(sl=True)

if len(selection) != 3:
    quit('Wrong selection length')

ik_jnt = selection[0]
fk_jnt = selection[1]
skin_jnt = selection[2]

base_name = ik_jnt.replace('_IK', '').replace('_JNT', '')
bc_node = '{}_BlendColors'.format(base_name)

cmds.createNode('blendColors', n=bc_node)

cmds.connectAttr('{}.rotate'.format(ik_jnt), '{}.color1'.format(bc_node))
cmds.connectAttr('{}.rotate'.format(fk_jnt), '{}.color2'.format(bc_node))
cmds.connectAttr('{}.output'.format(bc_node), '{}.rotate'.format(skin_jnt))
