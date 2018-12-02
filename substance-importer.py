# =================================================================================================
# Substance Painter Importer
# Davide Rossetto [davide(dot)ross93(at)gmail(dot)com]
# =================================================================================================

import maya.cmds as cmds
import re

VERSION = '1.0.1'
WINDOW_ID = 'SubstancePainterImporterWin'
DEBUG = False

GREEN_COLOR = [0, 1, 0]
RED_COLOR = [1, .3, .3]

textures = []

# ===== CLASSES ===================================================================================

class TextureInfo:
    def __init__(self, name, type, udim):
        self.name = name
        self.type = type
        self.udim = udim
        
    def __str__(self):
        return 'Name: {}, type: {}, UDIM: {}'.format(self.name, self.type, self.udim)
        
# ===== CALLBACKS =================================================================================

def select_input_dir(*args):
    dir = cmds.fileDialog2(fm=2)
    if dir is None:
        return

    cmds.textField('dirTextCtrl', e=True, text=dir[0])
    cmds.button('loadButtonCtrl', e=True, en=True)
    
def change_texture_map(tex):
    global textures

    baseName = cmds.optionMenu(textureOptionCtrl, q=True, value=True)
        
    hasBaseColor = sum(1 for x in textures if x.name == tex and x.type == 'BaseColor') > 0
    hasMetalness = sum(1 for x in textures if x.name == tex and x.type == 'Metalness') > 0
    hasRoughness = sum(1 for x in textures if x.name == tex and x.type == 'Roughness') > 0
    hasNormal = sum(1 for x in textures if x.name == tex and x.type == 'Normal') > 0
    hasHeight = sum(1 for x in textures if x.name == tex and x.type == 'Height') > 0

    canCreate = True
    
    if hasBaseColor:
        maps = sum(1 for x in textures if x.name == tex and x.type == 'BaseColor')
        cmds.text(baseColorTextCtrl, edit=True, bgc=GREEN_COLOR, label='{}_BaseColor.1001.png ({} UDIM)'.format(baseName, maps))
    else:
        cmds.text(baseColorTextCtrl, edit=True, bgc=RED_COLOR, label='Base color map not found!')
        canCreate = False
        
    if hasMetalness:
        maps = sum(1 for x in textures if x.name == tex and x.type == 'Metalness')
        cmds.text(metalnessTextCtrl, edit=True, bgc=GREEN_COLOR, label='{}_Metalness.1001.png ({} UDIM)'.format(baseName, maps))
    else:
        cmds.text(metalnessTextCtrl, edit=True, bgc=RED_COLOR, label='Metalness map not found!')
        canCreate = False
        
    if hasRoughness:
        maps = sum(1 for x in textures if x.name == tex and x.type == 'Roughness')
        cmds.text(roughnessTextCtrl, edit=True, bgc=GREEN_COLOR, label='{}_Roughness.1001.png ({} UDIM)'.format(baseName, maps))
    else:
        cmds.text(roughnessTextCtrl, edit=True, bgc=RED_COLOR, label='Roughness map not found!')
        canCreate = False
        
    if hasNormal:
        maps = sum(1 for x in textures if x.name == tex and x.type == 'Normal')
        cmds.text(normalTextCtrl, edit=True, bgc=GREEN_COLOR, label='{}_Normal.1001.png ({} UDIM)'.format(baseName, maps))
    else:
        cmds.text(normalTextCtrl, edit=True, bgc=RED_COLOR, label='Normal map not found!')
        canCreate = False
        
    if hasHeight:
        maps = sum(1 for x in textures if x.name == tex and x.type == 'Height')
        cmds.text(heightTextCtrl, edit=True, bgc=GREEN_COLOR, label='{}_Height.1001.png ({} UDIM)'.format(baseName, maps))
    else:
        cmds.text(heightTextCtrl, edit=True, bgc=RED_COLOR, label='Height map not found!')
        canCreate = False

    cmds.button('createMatButtonCtrl', e=True, en=canCreate)
    cmds.button('createAnywayButtonCtrl', e=True, en=not canCreate)
    

def get_textures_info(*args):
    global textures
    
    dir = cmds.textField('dirTextCtrl', q=True, text=True)
    files = cmds.getFileList(folder=dir)
    textures = []

    items = cmds.optionMenu('textureOptionCtrl', q=True, itemListLong=True)
    if items:
        cmds.deleteUI(items)
    
    for file in files:
        match = re.search(r'(.+)_(BaseColor|Height|Normal|Roughness|Metalness)\.([\d]{4})', file)
        
        if match:
            texData = match.groups()
            textures.append(TextureInfo(texData[0], texData[1], texData[2]))
            
    for tex in {t.name for t in textures}:
        cmds.menuItem(label=tex)
    
    cmds.optionMenu(textureOptionCtrl, edit=True, enable=True, changeCommand=change_texture_map)
    change_texture_map(textures[0].name)
    
def create_material(*args):
    baseDir = cmds.textField('dirTextCtrl', q=True, text=True)
    baseName = cmds.optionMenu(textureOptionCtrl, q=True, value=True)
    camelCaseTitle = baseName.title().replace('_', '')

    baseColorFile = cmds.createNode('file', n='baseColorFile')
    heightFile = cmds.createNode('file', n='heightFile')
    normalFile = cmds.createNode('file', n='normalFile')
    roughnessFile = cmds.createNode('file', n='roughnessFile')
    metalnessFile = cmds.createNode('file', n='metalnessFile')

    cmds.setAttr(baseColorFile + '.fileTextureName', '{}/{}_BaseColor.1001.png'.format(baseDir, baseName), type='string')
    cmds.setAttr(heightFile + '.fileTextureName', '{}/{}_Height.1001.png'.format(baseDir, baseName), type='string')
    cmds.setAttr(normalFile + '.fileTextureName', '{}/{}_Normal.1001.png'.format(baseDir, baseName), type='string')
    cmds.setAttr(roughnessFile + '.fileTextureName', '{}/{}_Roughness.1001.png'.format(baseDir, baseName), type='string')
    cmds.setAttr(metalnessFile + '.fileTextureName', '{}/{}_Metalness.1001.png'.format(baseDir, baseName), type='string')
    
    normalBump = cmds.createNode('bump2d', n='normalBump')
    heightBump = cmds.createNode('bump2d', n='heightBump')
    
    matNode = cmds.createNode('aiStandardSurface', n=camelCaseTitle + '_MAT')
    
    cmds.connectAttr(baseColorFile + '.outColor', matNode + '.baseColor')
    cmds.connectAttr(roughnessFile + '.outAlpha', matNode + '.specularRoughness')
    cmds.connectAttr(metalnessFile + '.outAlpha', matNode + '.metalness')
    
    cmds.setAttr(baseColorFile + '.uvTilingMode', 3)
    cmds.setAttr(heightFile + '.uvTilingMode', 3)
    cmds.setAttr(normalFile + '.uvTilingMode', 3)
    cmds.setAttr(roughnessFile + '.uvTilingMode', 3)
    cmds.setAttr(metalnessFile + '.uvTilingMode', 3)
    
    cmds.setAttr(heightFile + '.colorSpace', 'Raw', type='string')
    cmds.setAttr(roughnessFile + '.colorSpace', 'Raw', type='string')
    cmds.setAttr(metalnessFile + '.colorSpace', 'Raw', type='string')
    cmds.setAttr(normalFile + '.colorSpace', 'Raw', type='string')
    
    cmds.setAttr(heightFile + '.alphaIsLuminance', True)
    cmds.setAttr(roughnessFile + '.alphaIsLuminance', True)
    cmds.setAttr(metalnessFile + '.alphaIsLuminance', True)
    
    cmds.setAttr(normalBump + '.bumpInterp', 1)
    cmds.setAttr(normalBump + '.aiFlipR', True)
    
    cmds.connectAttr(heightFile + '.outAlpha', heightBump + '.bumpValue')
    cmds.connectAttr(normalFile + '.outAlpha', normalBump + '.bumpValue')
    cmds.connectAttr(heightBump + '.outNormal', normalBump + '.normalCamera')
    cmds.connectAttr(normalBump + '.outNormal', matNode + '.normalCamera')
        
# ===== UI ========================================================================================
    
if cmds.window(WINDOW_ID, exists=True):
    cmds.deleteUI(win)

win = cmds.window(title='Substance Painter importer', widthHeight=(350, 305), mxb=False, mnb=False, s=False)
form = cmds.formLayout(numberOfDivisions=100)

colLayout = cmds.columnLayout(adjustableColumn=True, rowSpacing=10)

dirSelectorLayout = cmds.rowLayout(
    numberOfColumns=3,
    columnWidth3=(100, 210, 20),
    adjustableColumn=2,
    columnAlign=(1, 'right'),
    columnAttach=[
        (1, 'both', 0),
        (2, 'both', 0),
        (3, 'both', 0)
    ]
)

dirLabelCtrl = cmds.text(label='Directory')

if DEBUG:
    dirTextCtrl = cmds.textField('dirTextCtrl', text='/Users/master/Documents/maya/projects/TestProj/sourceimages') # WARNING: DEBUG!
else:
    dirTextCtrl = cmds.textField('dirTextCtrl')

dirBtnCtrl = cmds.iconTextButton(style='iconOnly', image='fileOpen.png', command=select_input_dir)

cmds.setParent('..')

cmds.button('loadButtonCtrl', label='Load', command=get_textures_info, en=DEBUG)
cmds.separator()
textureOptionCtrl = cmds.optionMenu('textureOptionCtrl', label='Texture', enable=False)

cmds.columnLayout(adjustableColumn=True, rowSpacing=3)
baseColorTextCtrl = cmds.text(label="Base color", bgc=[0, 0, 0], ebg=True, height=20)
metalnessTextCtrl = cmds.text(label="Metalness", bgc=[0, 0, 0], ebg=True, height=20)
roughnessTextCtrl = cmds.text(label="Roughness", bgc=[0, 0, 0], ebg=True, height=20)
normalTextCtrl = cmds.text(label="Normal", bgc=[0, 0, 0], ebg=True, height=20)
heightTextCtrl = cmds.text(label="Height", bgc=[0, 0, 0], ebg=True, height=20)
cmds.setParent('..')

cmds.button('createMatButtonCtrl', label='Create full material', command=create_material, enable=False)
cmds.button('createAnywayButtonCtrl', label='Create anyway (may causes errors!)', command=create_material, en=False)

cmds.formLayout(form, edit=True, attachForm=[
    (colLayout, 'top', 5),
    (colLayout, 'left', 5)
])

cmds.showWindow(win)
