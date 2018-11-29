import maya.cmds as cmds

WINDOW_ID = 'SubstancePainterImporterWin'

def select_input_dir(*args):
    dir = cmds.fileDialog2(fm=2)
    cmds.textField('dirTextCtrl', e=True, text=dir[0])

def get_textures_info(*args):
    dir = cmds.textField('dirTextCtrl', q=True, text=True)
    print cmds.getFileList(folder=dir)

if cmds.window(WINDOW_ID, exists=True):
    cmds.deleteUI(win)

win = cmds.window(title='Substance Painter importer', width=370, mxb=False, mnb=False, s=False)
form = cmds.formLayout(numberOfDivisions=100)

colLayout = cmds.columnLayout(adjustableColumn=True)

dirSelectorLayout = cmds.rowLayout(
    numberOfColumns=3,
    columnWidth3=(100, 210, 40),
    adjustableColumn=2,
    columnAlign=(1, 'right'),
    columnAttach=[
        (1, 'both', 0),
        (2, 'both', 0),
        (3, 'both', 0)
    ]
)

dirLabelCtrl = cmds.text(label='Directory')
dirTextCtrl = cmds.textField('dirTextCtrl', text='D:/Projects/Maya/Pinup/sourceimages/textures/back_armor') # WARNING: DEBUG!
dirBtnCtrl = cmds.iconTextButton(style='iconOnly', image='sphere.png', command=select_input_dir)

cmds.setParent('..')

cmds.button(label='Load', command=get_textures_info)

cmds.formLayout(form, edit=True, attachForm=[
    (colLayout, 'top', 5),
    (colLayout, 'left', 5)
])

cmds.showWindow(win)
