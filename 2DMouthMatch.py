import maya.cmds as cmds
import json

window = cmds.window( title="2D Mouth Match", iconName='2DMouthMatch', widthHeight=(500, 300) )

cmds.frameLayout(label='Set Parameters', labelAlign='top')
cmds.rowColumnLayout( numberOfColumns=2, columnWidth=[(1, 400), (2, 100)], adjustableColumn=True )

cmds.text( label='Phoneme Mouth Shape AttrName' )
phonemeMouthShapeName = cmds.textField()
cmds.text( label='Consonant Shape Index' )
consonantIndex = cmds.textField()
cmds.text( label='th/dh Shape Index' )
th_dhIndex = cmds.textField()
cmds.text( label='u/oo Vowel Shape Index' )
uVowelIndex = cmds.textField()
cmds.text( label='ee Vowel Shape Index' )
eeVowelIndex = cmds.textField()
cmds.text( label='Short Vowel Shape Index' )
shortVowelIndex = cmds.textField()

cmds.textField(phonemeMouthShapeName, edit=1)
cmds.textField(consonantIndex, edit=1)
cmds.textField(th_dhIndex, edit=1)
cmds.textField(uVowelIndex, edit=1)
cmds.textField(shortVowelIndex, edit=1)

cmds.setParent('..')
cmds.setParent('..')

chosenFile = ''
scnFilter = "JSON files (*.json);;All Files (*.*)"

cmds.frameLayout(label='Run', labelAlign='top')
cmds.rowColumnLayout(adjustableColumn=True)
cmds.button( label='Select JSON File', command='chosenFile=showFileWindow()')
cmds.button( label='Parse JSON File', command='parseFile(chosenFile)')
cmds.button( label='Close', command=('cmds.deleteUI(\"' + window + '\", window=True)') )

cmds.setParent( '..' )
cmds.setParent( '..' )

cmds.showWindow( window )

# 0 = consonants, 1 = th/dh, 2 = u/oos, 3 = ee, 4 = short vowels
mouthArray = []

def showFileWindow():
    f = cmds.fileDialog2(fm=1, ds=0, cap="Open", ff=scnFilter ,okc="Select JSON file", hfe=0)
    return f
    
def setParams():
    global mouthAttrName
    mouthAttrName = cmds.textField(phonemeMouthShapeName, query=True, text=True)
    
    global consonantIndex
    mouthArray.append(cmds.textField(consonantIndex, query=True, text=True))
    global th_dhIndex
    mouthArray.append(cmds.textField(th_dhIndex, query=True, text=True))
    global uVowelIndex
    mouthArray.append(cmds.textField(uVowelIndex, query=True, text=True))
    global eeVowelIndex
    mouthArray.append(cmds.textField(eeVowelIndex, query=True, text=True))
    global shortVowelIndex
    mouthArray.append(cmds.textField(shortVowelIndex, query=True, text=True))
    
    #print(mouthArray)
    
def parseFile(filePath):   
    if len(filePath) == 0:
        print('No File Selected')
        return
        
    filePath = filePath[0]
    setParams()
    f = open(filePath)
    data = json.load(f)
    words = data["words"]
    for i in words:
        #print(i['word'])
        if i['case'] == 'success':
            start = i['start']
            startOff = i['startOffset']
            newTime = start
            for j in i['phones']:
                ph = j['phone'].split('_')[0]
                shape = createKeys(ph)
                cmds.setKeyframe(value=shape, attribute=mouthAttrName, time='{:2.4}sec'.format(newTime))
                #print('Phoneme: {} - startTime: {:2.4}'.format(j['phone'], newTime))
                newTime = start + j['duration']
            
    f.close()
    
def createKeys(phoneme):
    if phoneme == 'th' or phoneme == 'dh' or phoneme[0] == 'l':
        return int(mouthArray[1])
    elif phoneme in ['uw', 'oo', 'aw', 'ow', 'oov', 'ao']:
        return int(mouthArray[2])
    elif phoneme in ['iy', 'ee', 'ey', 's', 't']:
        return int(mouthArray[3])
    elif phoneme[0] in 'bcdfghjkmnpqrvwz':
        return int(mouthArray[0])
    else:
        return int(mouthArray[4])
    