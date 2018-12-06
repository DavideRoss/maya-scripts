# maya-scripts
Collection of scripts written by myself for living Autodesk Maya hell better.

## substance-importer
### Changelog
- **Version 1.0.1**
  - Added version number, starting from 1.0.1
  - Fixed attribute "Flip G" on normal bump node

---

## autorig-hand
### Description
Script to rig an hand with three joints per finger, all children of a common wrist joint. It creates custom attributes for each finger joint on wrist control, plus a master fist control summed with PlusMinusAverage node to single finger joint control rotation, on specified axis (change line 12).

### Instruction
- Rename joints following these rules:
    - **Wrist**: \[Side\]\_Wrist_JNT *(ex. L_Wrist_JNT)*
    - **Each finger joint**: \[Side\]\_\[Finger\]\_\[Index\] *(ex. L_Thumb_0)*
        - Index is a progressive number, starting from 0 (the base of the finger)
        - No limitation on finger name, nor on finger count
- Rotate and freeze all joints
- Select wrist join
- Run script

### Caveats
There are no consistency controls on name and joint parenting on transformation. If there are objects with same name the script will return error (and probably some unexpected results).

### Changelog
- **Version 1.0.0**
    - Initial commit

---

## colorize-orange
### Description
Activate display ovveride of the shape of selected object, set the color on RGB and the swatch to orange.

### Instruction
- Select objects to colorize
- Run the script
- Profit

### Caveats

The script automatically prepend 'Shape' to the name and check if the object exists, so if it's not working is because your selection doesn't have a shape. The shape check will fail silently, the message will be added in next versions.

### Changelog
- **Version 1.0.0**
    - Initial commit

---

## create-control-group
### Description
Create a circular control, group it and match the transformation of the group with selected joint.

### Instruction
- Select joint
- Run the script
- Enjoy

### Caveats
Not a single one, if any check will fail (no object selected or selected object is not a joint) it will fail with a message on viewport (top left corner) and abort.

### Changelog
- **Version 1.0.0**
    - Initial commit