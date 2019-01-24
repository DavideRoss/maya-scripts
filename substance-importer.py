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
    def __init__(self, file_name, name, tex_type, is_tiled):
        self.file_name = file_name
        self.name = name
        self.type = tex_type
        self.is_tiled = is_tiled

    def set_udim(self, udim):
        self.udim = udim

    def set_material_name(self, mat):
        self.material_name = mat
        
    def __str__(self):
        return 'Name: {}, type: {}, is tiled: {}'.format(self.name, self.type, self.is_tiled)
        
# ===== CALLBACKS =================================================================================

def select_input_dir(*args):
    dir = cmds.fileDialog2(fm=2, ds=2, okc='Select')
    if dir is None:
        return

    cmds.textField('dirTextCtrl', e=True, text=dir[0])
    cmds.button('loadButtonCtrl', e=True, en=True)
    
def change_texture_map(tex):
    global textures

    baseName = cmds.optionMenu(textureOptionCtrl, q=True, value=True)

    baseColor = next((x for x in textures if x.name == tex and x.type == 'BaseColor'), None)
    metalness = next((x for x in textures if x.name == tex and x.type == 'Metalness'), None)
    roughness = next((x for x in textures if x.name == tex and x.type == 'Roughness'), None)
    normal = next((x for x in textures if x.name == tex and x.type == 'Normal'), None)
    height = next((x for x in textures if x.name == tex and x.type == 'Height'), None)

    canCreate = True
    cmds.textField('matNameCtrl', edit=True, text='{}_MAT'.format(baseName))
    
    if baseColor:
        maps = sum(1 for x in textures if x.name == tex and x.type == 'BaseColor')
        cmds.text(baseColorTextCtrl, edit=True, bgc=GREEN_COLOR, label='{} ({})'.format(baseColor.file_name, 'non-tiled' if not baseColor.is_tiled else '{} UDIM'.format(maps)))
    else:
        cmds.text(baseColorTextCtrl, edit=True, bgc=RED_COLOR, label='Base color map not found!')
        canCreate = False
        
    if metalness:
        maps = sum(1 for x in textures if x.name == tex and x.type == 'Metalness')
        cmds.text(metalnessTextCtrl, edit=True, bgc=GREEN_COLOR, label='{} ({})'.format(metalness.file_name, 'non-tiled' if not metalness.is_tiled else '{} UDIM'.format(maps)))
    else:
        cmds.text(metalnessTextCtrl, edit=True, bgc=RED_COLOR, label='Metalness map not found!')
        canCreate = False
        
    if roughness:
        maps = sum(1 for x in textures if x.name == tex and x.type == 'Roughness')
        cmds.text(roughnessTextCtrl, edit=True, bgc=GREEN_COLOR, label='{} ({})'.format(roughness.file_name, 'non-tiled' if not roughness.is_tiled else '{} UDIM'.format(maps)))
    else:
        cmds.text(roughnessTextCtrl, edit=True, bgc=RED_COLOR, label='Roughness map not found!')
        canCreate = False
        
    if normal:
        maps = sum(1 for x in textures if x.name == tex and x.type == 'Normal')
        cmds.text(normalTextCtrl, edit=True, bgc=GREEN_COLOR, label='{} ({})'.format(normal.file_name, 'non-tiled' if not normal.is_tiled else '{} UDIM'.format(maps)))
    else:
        cmds.text(normalTextCtrl, edit=True, bgc=RED_COLOR, label='Normal map not found!')
        canCreate = False
        
    if height:
        maps = sum(1 for x in textures if x.name == tex and x.type == 'Height')
        cmds.text(heightTextCtrl, edit=True, bgc=GREEN_COLOR, label='{} ({})'.format(height.file_name, 'non-tiled' if not height.is_tiled else '{} UDIM'.format(maps)))
    else:
        cmds.text(heightTextCtrl, edit=True, bgc=RED_COLOR, label='Height map not found!')
        canCreate = False

    cmds.button('createMatButtonCtrl', e=True, en=canCreate)  

def get_textures_info(*args):
    global textures
    
    dir = cmds.textField('dirTextCtrl', q=True, text=True)
    files = cmds.getFileList(folder=dir, filespec='*.png')
    files.sort()
    textures = []

    items = cmds.optionMenu('textureOptionCtrl', q=True, itemListLong=True)
    if items:
        cmds.deleteUI(items)
    
    for file_name in files:
        match = re.search(r'(.+)_(BaseColor|Height|Normal|Roughness|Metalness)\.(.+)\.', file_name)
        
        if match:
            texData = match.groups()
            new_tex = TextureInfo(file_name, texData[0], texData[1], texData[2].isdigit())

            if new_tex.is_tiled:
                new_tex.set_udim(texData[2])
            else:
                new_tex.set_material_name(texData[2])

            textures.append(new_tex)
            
    for tex in {t.name for t in textures}:
        cmds.menuItem(label=tex)
    
    cmds.optionMenu(textureOptionCtrl, edit=True, enable=True, changeCommand=change_texture_map)
    change_texture_map(textures[0].name)
    
def create_material(*args):
    global textures

    baseDir = cmds.textField('dirTextCtrl', q=True, text=True)
    baseName = cmds.optionMenu(textureOptionCtrl, q=True, value=True)
    matName = cmds.textField('matNameCtrl', q=True, text=True)

    baseColor = next((x for x in textures if x.name == baseName and x.type == 'BaseColor'), None)
    metalness = next((x for x in textures if x.name == baseName and x.type == 'Metalness'), None)
    roughness = next((x for x in textures if x.name == baseName and x.type == 'Roughness'), None)
    normal = next((x for x in textures if x.name == baseName and x.type == 'Normal'), None)
    height = next((x for x in textures if x.name == baseName and x.type == 'Height'), None)

    matNode = cmds.shadingNode('aiStandardSurface', n=matName, asShader=True)

    # =============================================================================================
    # ===== BASE COLOR ============================================================================
    # =============================================================================================

    baseColorFile = cmds.shadingNode('file', n='baseColorFile', asTexture=True)
    cmds.setAttr(baseColorFile + '.fileTextureName', '{}/{}'.format(baseDir, baseColor.file_name), type='string')

    if baseColor.is_tiled:
        cmds.setAttr(baseColorFile + '.uvTilingMode', 3)

    cmds.connectAttr(baseColorFile + '.outColor', matNode + '.baseColor')

    # =============================================================================================
    # ===== METALNESS =============================================================================
    # =============================================================================================

    metalnessFile = cmds.shadingNode('file', n='metalnessFile', asTexture=True)
    cmds.setAttr(metalnessFile + '.fileTextureName', '{}/{}'.format(baseDir, metalness.file_name), type='string')

    cmds.setAttr(metalnessFile + '.colorSpace', 'Raw', type='string')
    cmds.setAttr(metalnessFile + '.alphaIsLuminance', True)

    if metalness.is_tiled:
        cmds.setAttr(metalnessFile + '.uvTilingMode', 3)

    cmds.connectAttr(metalnessFile + '.outAlpha', matNode + '.metalness')

    # =============================================================================================
    # ===== ROUGHNESS =============================================================================
    # =============================================================================================

    roughnessFile = cmds.shadingNode('file', n='roughnessFile', asTexture=True)
    cmds.setAttr(roughnessFile + '.fileTextureName', '{}/{}'.format(baseDir, roughness.file_name), type='string')

    cmds.setAttr(roughnessFile + '.colorSpace', 'Raw', type='string')
    cmds.setAttr(roughnessFile + '.alphaIsLuminance', True)

    if roughness.is_tiled:
        cmds.setAttr(roughnessFile + '.uvTilingMode', 3)

    cmds.connectAttr(roughnessFile + '.outAlpha', matNode + '.specularRoughness')

    # =============================================================================================
    # ===== NORMAL ================================================================================
    # =============================================================================================

    normalFile = cmds.shadingNode('file', n='normalFile', asTexture=True)
    cmds.setAttr(normalFile + '.fileTextureName', '{}/{}'.format(baseDir, normal.file_name), type='string')

    cmds.setAttr(normalFile + '.colorSpace', 'Raw', type='string')

    if normal.is_tiled:
        cmds.setAttr(normalFile + '.uvTilingMode', 3)

    normalBump = cmds.shadingNode('bump2d', n='normalBump', asUtility=True)
    cmds.setAttr(normalBump + '.bumpInterp', 1)
    cmds.setAttr(normalBump + '.aiFlipR', True)
    cmds.setAttr(normalBump + '.aiFlipG', False)

    cmds.connectAttr(normalFile + '.outAlpha', normalBump + '.bumpValue')
    cmds.connectAttr(normalBump + '.outNormal', matNode + '.normalCamera')

    # =============================================================================================
    # ===== HEIGHT ================================================================================
    # =============================================================================================

    heightFile = cmds.shadingNode('file', n='heightFile', asTexture=True)
    cmds.setAttr(heightFile + '.fileTextureName', '{}/{}'.format(baseDir, height.file_name), type='string')

    cmds.setAttr(heightFile + '.colorSpace', 'Raw', type='string')
    cmds.setAttr(heightFile + '.alphaIsLuminance', True)

    if height.is_tiled:
        cmds.setAttr(heightFile + '.uvTilingMode', 3)

    heightBump = cmds.shadingNode('bump2d', n='heightBump', asUtility=True)
    cmds.setAttr(heightBump + '.bumpDepth', 0)

    cmds.connectAttr(heightFile + '.outAlpha', heightBump + '.bumpValue')
    cmds.connectAttr(heightBump + '.outNormal', normalBump + '.normalCamera')
        
# ===== UI ========================================================================================
    
if cmds.window(WINDOW_ID, exists=True):
    cmds.deleteUI(win)

win = cmds.window(title='Substance Painter Importer', widthHeight=(350, 305), mxb=False, mnb=False, s=False)
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
    dirTextCtrl = cmds.textField('dirTextCtrl', text='/Users/master/Documents/maya/projects/__Shader_Ball_TEST/sourceimages/pressa') # WARNING: DEBUG!
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

dirSelectorLayout = cmds.rowLayout(
    numberOfColumns=2,
    columnWidth2=(100, 230),
    adjustableColumn=1,
    columnAlign=(1, 'right'),
    columnAttach=[
        (1, 'both', 0),
        (2, 'both', 0)
    ]
)

matNameLabelCtrl = cmds.text(label='Mat. name')
matNameCtrl = cmds.textField('matNameCtrl')
cmds.setParent('..')

cmds.button('createMatButtonCtrl', label='Create material', command=create_material, enable=False)

cmds.formLayout(form, edit=True, attachForm=[
    (colLayout, 'top', 5),
    (colLayout, 'left', 5)
])

cmds.showWindow(win)