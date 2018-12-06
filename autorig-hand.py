# =================================================================================================
# AutoRig - hand
# Davide Rossetto [davide(dot)ross93(at)gmail(dot)com]
# =================================================================================================

import maya.cmds as cmds
import re

VERSION = '1.0.0'

COLOR_ORANGE = (1, .5, 0)
COLOR_YELLOW = (1, 1, 0)

FINGER_MAIN_AXIS = 'Z'
FINGER_DEF = ['Base', 'Mid', 'Tip']
PLUS_SEQ = ['x', 'y', 'z']

# =================================================================================================

def create_control(joint, color=COLOR_ORANGE, scale=1):
    ctrl_name = joint.replace('_JNT', '')
    ctrl = cmds.circle(nr=(1, 0, 0), c=(0, 0, 0), n='{}_CTRL'.format(ctrl_name))
    ctrl_grp = cmds.group(ctrl, n='{}_CTRL_GRP'.format(ctrl_name))
    cmds.matchTransform(ctrl_grp, joint)
    cmds.scale(scale, scale, scale, '{}_CTRL_GRP'.format(ctrl_name))
    colorize_object('{}_CTRL'.format(ctrl_name), color=color)

def colorize_object(obj, color=COLOR_ORANGE):
    cmds.setAttr('{}Shape.overrideEnabled'.format(obj), True)
    cmds.setAttr('{}Shape.overrideRGBColors'.format(obj), True)

    for channel, color in zip(('R', 'G', 'B'), color):
        cmds.setAttr('{}Shape.overrideColor{}'.format(obj, channel), color)

def get_base_name(obj):
    return obj.replace('_JNT', '').replace('_CTRL', '').replace('_GRP', '')

def connect_rotation(ctrl, jnt):
    cmds.connectAttr('{}.rotate'.format(ctrl), '{}.rotate'.format(jnt))

def unpack_finger(name):
    (side, name, index) = re.search(r'([LR]_)?(\w+)_(\d)', name).groups()
    return (name, FINGER_DEF[int(index)], side)

def add_separator_attr(obj, name):
    new_attr = cmds.addAttr(obj, ln=name, k=True)
    cmds.setAttr('{}.{}'.format(obj, name), lock=True)

# =================================================================================================

selection = cmds.ls(sl=True)

if len(selection) == 0:
    cmds.inViewMessage(amg='No object selected', pos='topLeft', fade=True)
    quit('No object selected')

wrist_jnt = selection[0]
wrist_ctrl = wrist_jnt.replace('_JNT', '_CTRL')
wrist_ctrl_grp = wrist_ctrl + '_GRP'

if not cmds.objExists(wrist_ctrl):
    create_control(wrist_jnt, color=COLOR_YELLOW)
    connect_rotation(wrist_ctrl, wrist_jnt)

add_separator_attr(wrist_ctrl, 'MASTER')
cmds.addAttr(wrist_ctrl, at='float', ln='Master_Fist', k=True)
mfist_attr = '{}.Master_Fist'.format(wrist_ctrl)

for finger_jnt in list(filter(lambda x: '_JNT' in x, cmds.listRelatives(wrist_jnt))):
    finger_joints = [finger_jnt, finger_jnt.replace('0', '1'), finger_jnt.replace('0', '2')]
    finger_info = unpack_finger(finger_jnt)
    add_separator_attr(wrist_ctrl, finger_info[0].upper())

    f_plus = '{}_{}_MasterFist_PlusMinusAvg'.format(finger_info[2], finger_info[0])
    cmds.createNode('plusMinusAverage', n=f_plus)

    cmds.connectAttr('{}.Master_Fist'.format(wrist_ctrl), '{}.input3D[0].input3Dx'.format(f_plus))
    cmds.connectAttr('{}.Master_Fist'.format(wrist_ctrl), '{}.input3D[0].input3Dy'.format(f_plus))
    cmds.connectAttr('{}.Master_Fist'.format(wrist_ctrl), '{}.input3D[0].input3Dz'.format(f_plus))
    
    for i in range(0, len(finger_joints)):
        # ==== POPULATE NAMES =====================================================================
        f_jnt = finger_joints[i]
        f_ctrl = get_base_name(f_jnt) + '_CTRL'
        f_grp = f_ctrl + '_GRP'

        # ==== CREATE CONTROL =====================================================================
        create_control(f_jnt, scale=.2)

        # ==== SET PARENTING ======================================================================
        if i != 0:
            cmds.parent(f_grp, '{}_CTRL'.format(get_base_name(finger_joints[i - 1])))
        else:
            cmds.parent(f_grp, wrist_ctrl)

        # ==== CONNECT ROTATION TO JOINT ==========================================================
        connect_rotation(f_ctrl, f_jnt)
        fing_def = unpack_finger(f_jnt)
        cmds.addAttr(wrist_ctrl, at='float', ln='{}_{}'.format(fing_def[0], fing_def[1]), k=True)
        cmds.connectAttr('{}.{}_{}'.format(wrist_ctrl, fing_def[0], fing_def[1]), '{}.input3D[1].input3D{}'.format(f_plus, PLUS_SEQ[i]))
        cmds.connectAttr('{}.output3D.output3D{}'.format(f_plus, PLUS_SEQ[i]), '{}.rotate{}'.format(f_ctrl, FINGER_MAIN_AXIS))
