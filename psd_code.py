c = nuke.thisNode()['codeDefs'].getText()
exec(c) ##import defs
psdTooldNode = nuke.thisNode()
psdFileNode = psdTooldNode.input(0)
if psdFileNode == None:
    raise Exception('PSD File Not Connected')

a = []
fn = nuke.thisNode()

AllDeps = AllDependentNodes(a,fn) ##sortetbyCreation
mergesReadgTuple = []
if check == 1:
    fn['dontrender'].setValue(1)      ##<only udate List
else:
    fn['dontrender'].setValue(0)      ##reconvert and new passes
fn['AutoCreateMerges'].setValue(0)

lnods = []
lnames = []
for dep in AllDeps:
    if dep.name()[0] == '_':
        lnames.append(dep.name().split('_')[2])
        lnods.append(dep)

doubles = []
for l,n in zip(lnames,lnods):
    for l2,n2 in zip(lnames,lnods):
        if l == l2:
            if n != n2:
                if n.name()[0:6] == '_Read_':
                    doubles.append(n.name()+'&'+n2.name())

##reconvert
c = fn['codeConvert'].getText()
exec(c)
newtext = fn['ListLayers'].getText()
newlist = newtext.split('\n\n')
rows = []

for duble in doubles:
    dublesSplited = duble.split("&")[0:2]
    mergeNode = nuke.toNode(dublesSplited[1])
    readerNode = nuke.toNode(dublesSplited[0])
    layerNum = dublesSplited[1][1:4]
    layerName = dublesSplited[0].split("_")[2]
    blend = mergeNode['label'].getText().split('_')[0]
    opp = mergeNode['opacity'].getValue()
    row = layerNum +'_' + blend + '_' + str(int(opp)) + '_' + layerName +'||'+ readerNode.name() + '||' + mergeNode.name() + '||\n'
    rows.append(layerNum +'_' + blend + '_' + str(int(opp)) + '_' + layerName)
    newLayerslist = matchListsReplaceParms(newlist,row,fn)


AllDeps = AllDependentNodes(a,fn)



lnames = []
for dep in AllDeps:
    if dep.name()[0] == '_':
        if dep.name()[0:6] != '_Read_':
            lnames.append(dep.name().split('_')[2])


#for nl in newLayerslist:
#   rows.append(nl.split('||')[0])

Llist = newtext.split('\n\n')
text = ''
i = 0
for r  in lnames:
    if r != '':
        text +=  'order inNuke - ' + '{'+ r +'} >>> '+ Llist[i].split('||')[0].split('_')[0] + '_{' + Llist[i].split('||')[0].split('_')[3] + '} - order in PSD\n' + '\n'
        i+=1

fn['oldtree'].setText(text)

if len(newLayerslist) != 1:
    newText = '\n\n'.join(newLayerslist)
    fn.setXpos(int(fn['xpos'].getValue()+400))
    deps = fn.dependent()
    for dep in deps:
        dep.setInput(0,None)
    firstNODE = createMerges(fn, newText)
    firstNODE.setName("UPDATED_LAYERS")
    for dep in deps:
        dep.setInput(0,fn)

--------------------------------------------------------------------------------------------------------------------
#!/bin/python
# -*- coding: utf-8 -*-
import re
import os
def transliterate(string):
    capital_letters = {u'А': u'A', u'Б': u'B', u'В': u'V', u'Г': u'G',u'Д': u'D',u'Е': u'E',u'Ё': u'E',u'З': u'Z',u'И': u'I',u'Й': u'Y',u'К': u'K',u'Л': u'L',u'М': u'M',u'Н': u'N',u'О': u'O',u'П': u'P',u'Р': u'R',u'С': u'S',u'Т': u'T',u'У': u'U',u'Ф': u'F',u'Х': u'H',u'Ъ': u'',u'Ы': u'Y',u'Ь': u'',u'Э': u'E',}
    capital_letters_transliterated_to_multiple_letters = {u'Ж': u'Zh',u'Ц': u'Ts',u'Ч': u'Ch',u'Ш': u'Sh',u'Щ': u'Sch',u'Ю': u'Yu',u'Я': u'Ya',}
    lower_case_letters = {u'а': u'a',u'б': u'b',u'в': u'v',u'г': u'g',u'д': u'd',u'е': u'e',u'ё': u'e',u'ж': u'zh',u'з': u'z',u'и': u'i',u'й': u'y',u'к': u'k',u'л': u'l',u'м': u'm',u'н': u'n',u'о': u'o',u'п': u'p',u'р': u'r',u'с': u's',u'т': u't',u'у': u'u',u'ф': u'f',u'х': u'h',u'ц': u'ts',u'ч': u'ch',u'ш': u'sh',u'щ': u'sch',u'ъ': u'',u'ы': u'y',u'ь': u'',u'э': u'e',u'ю': u'yu',u'я': u'ya',}
    for cyrillic_string, latin_string in capital_letters_transliterated_to_multiple_letters.iteritems():
        string = re.sub(ur"%s([а-я])" % cyrillic_string, ur'%s\1' % latin_string, string)
    for dictionary in (capital_letters, lower_case_letters):
        for cyrillic_string, latin_string in dictionary.iteritems():
            string = string.replace(cyrillic_string, latin_string)
    for cyrillic_string, latin_string in capital_letters_transliterated_to_multiple_letters.iteritems():
        string = string.replace(cyrillic_string, latin_string.upper())
    return string

def getLayers(node):
    #print '-----------------get Layers-----------------------'
    metaString = 'input/psd/layers/'
    layers = []
    for k, v in node.metadata().iteritems():
        if 'name' in k and 'layers' in k:
            numberLayer = k.split('/')[3]
            r = transliterate(v.decode('cp1251'))
            nameWSpace = "".join([z for d in ' '.join(a for a in r.split()) for x in d for z in x if z.isalnum() or z ==' ']).replace("  ", " ")
            name = ''.join((nameWSpace.split(' ')))
            if node.metadata( metaString + numberLayer + '/flags' ) == 10:
                name = 'disabled' + name
            if node.metadata( metaString + numberLayer + '/flags' ) == 24 or node.metadata( metaString + numberLayer + '/flags' ) == 26:
                if node.metadata( metaString + numberLayer + '/mask/flags') == 0:
                    name = 'adj' + name
                elif node.metadata( metaString + numberLayer + '/nukeName' ) == '__Layer_group_':
                  name = 'ingrp' + name
                else:
                  name = 'outgrp' + name
            nukeName = node.metadata( metaString + numberLayer + '/nukeName' )
            blendmodeSpace = node.metadata( metaString + numberLayer + '/blendmode' )
            blendmode =  ''.join((blendmodeSpace.split(' ')))
            opasity = node.metadata( metaString + numberLayer + '/opacity' )
            crops = (node.metadata( metaString + numberLayer + '/x' ), node.metadata( metaString + numberLayer + '/y' ), node.metadata( metaString + numberLayer + '/r' ),node.metadata( metaString + numberLayer + '/t' ))
            layers.append(numberLayer.zfill(3) +'||'+ name +'||'+ nukeName +'||'+ blendmode +'||'+ str(opasity) +'||'+ str(crops))
    return sorted(layers)

def getCreatedConvertVersionFolder(psdname,update=0):
    nkpathname = nuke.root().name()
    layerfolder = '/'.join((nkpathname.split('/')[:-2])) + '/layers/PSDtoEXRLayers/' + psdname.split('.')[0] + '_000'
    if not os.path.isdir(layerfolder):
        os.makedirs(layerfolder)
    else:
        finded = 0
        i = 1
        while finded != 1:
            folderwithoutVercionNum = layerfolder[:-3]
            layerfolder = folderwithoutVercionNum + str(i).zfill(3)
            
            if not os.path.isdir(layerfolder):
                if update != 1:
                    os.makedirs(layerfolder)
                    finded = 1
                else:
                    layerfolder = folderwithoutVercionNum + str(i-1).zfill(3)
                    finded = 1
            else:
                i+=1
    return layerfolder

def checkNonUniqueNames(list_layers):
    listTuples = []
    names = []
    error_Value = []
    error_layer = []
    for layer in list_layers:
        listTuples.append((layer.split('||')[2],layer.split('||')[1]))
        if not layer.split('||')[2] in names:
            if layer.split('||')[2] != '__Layer_group_':
                names.append(layer.split('||')[2])
        else:
            error_Value.append(layer.split('||')[2])
    for er in error_Value:
        for tu in listTuples:
            if er in tu:
                error_layer.append(tu[1])
    return len(error_layer), error_layer

psdTooldNode = nuke.thisNode()## <--------------------------------------------
psdFileNode = psdTooldNode.input(0)
if nuke.root().name() == 'Root':
    raise Exception('Save Nk File!')
if psdFileNode == None:
    raise Exception('PSD File Not Connected!')
else:
    #fpspl = psdFileNode['file'].getValue().split('/')[:-1]
    psdname = psdFileNode['file'].getValue().split('/')[-1]
    #pngnameFolder = '.'.join(psdname.split('.')[:-1])
    #folderPSDPath = '/'.join(fpspl)
    #folderPNGPath = folderPSDPath+'/'+pngnameFolder
    if psdTooldNode['dontrender'].getValue() == 1:
        folderPNGPath = getCreatedConvertVersionFolder(psdname,1)
    else:
        folderPNGPath = getCreatedConvertVersionFolder(psdname)
    psdwidth = psdFileNode.width()
    psdheight = psdFileNode.height()
    psdTooldNode['box_width'].setValue(psdwidth)
    psdTooldNode['box_height'].setValue(psdheight)
    layers = getLayers(psdFileNode)
    if len(layers) > 30:
        if not nuke.ask('The number of layers  '+ str(len(layers)) +' is more than 30 continue?'):
            raise Exception
    g = checkNonUniqueNames(layers)
if g[0] == 0:
    psdTooldNode['PNGFolder'].setValue(folderPNGPath)
    if not os.path.isdir(folderPNGPath):
        os.mkdir(folderPNGPath)
    files = []
    listText = ''
    for layer in layers:
        if layer.split('||')[1][0:5] == 'ingrp' or layer.split('||')[1][0:6] == 'outgrp' or layer.split('||')[1][0:3] == 'adj' :
            ##create Empty named GroupName file 0_blend_
            num = layer.split('||')[0]
            lname = layer.split('||')[1]
            blend = layer.split('||')[3]
            opacity = layer.split('||')[4]
            listText += num.zfill(3)+'_'+blend+'_'+opacity+'_'+lname+'||This_Group_or_Adjustment'  + '\n\n'
            pathEMPTY = folderPNGPath +'/'+ num.zfill(3) +'_'+ blend +'_'+ lname + '.empty'
            files.append(pathEMPTY)
            open(pathEMPTY, 'a').close()
        else:
            ##check crop
            cropsStr = layer.split('||')[5][1:-1].split(', ')
            x = 0; y = psdheight; r = psdwidth; t = 0;
            if int(cropsStr[0]) > x:
                x = cropsStr[0]
            if int(cropsStr[1]) < y:
                y = cropsStr[1]
            if int(cropsStr[2]) < r:
                r = cropsStr[2]
            if int(cropsStr[3]) > t:
                t = cropsStr[3]
            #print x,y,r,t
            ##set crop Parms
            psdTooldNode['box'].setValue((x,y,r,t))
            ##setPath png file 0_norm_NAME_x_y_r_t.png
            num = layer.split('||')[0]
            lname = layer.split('||')[1]
            blend = layer.split('||')[3]
            opacity = layer.split('||')[4]
            crops = cropsStr
            
            pathPNG = folderPNGPath +'/'+ num.zfill(3) +'_'+ blend  +'_'+ opacity +'_'+ lname + '_' + str(x)+ '_' + str(y)+ '_' + str(r)+ '_' + str(t) + '.exr'
            listText += num.zfill(3)+'_'+blend+'_'+opacity+'_'+lname+'||'+ pathPNG +'\n\n'
            #print pathPNG
            psdTooldNode['in'].setValue(layer.split('||')[2])
            psdTooldNode['file'].setValue(pathPNG)
            if psdTooldNode['dontrender'].getValue() != 1:
                nuke.execute( psdTooldNode.name(), 1, 1 ) ##                  <<< RENDER COMMENT >>>
            files.append(pathPNG)
    nuke.thisNode()['ListLayers'].setValue(listText)
    c = nuke.thisNode()['codeDefs'].getText()
    exec(c)
    #nuke.root().begin()
    #grp = createReadersGroup(files)
    #psdTooldNode.setInput(2,grp)
    #yp = int(psdTooldNode['ypos'].value())
    #xp = int(psdTooldNode['xpos'].value())
    #grp.setYpos(yp-200)
    #grp.setXpos(xp)
else:
    raise Exception('NOT unique names OR\nNOT the unique length of the name from Cyrillic characters\nin this Layers:\n\n' + str(g[1:])[2:-3])

----------------------------------------------------------------------------------------------------------------------

def CreateReader(mergeNode,prevNode,file,toolNode):
    if file != 'This_Group_or_Adjustment':
        pathfrom = toolNode.fullName() + '.ReadLayer'
        xpos =  mergeNode['xpos'].getValue()
        ypos =  mergeNode['ypos'].getValue()
        nuke.selectAll()
        nuke.invertSelection()
        pathto = nuke.createNode('Dot')
        pathto.setInput(0,prevNode)
        readgroup = CopyPasteWithPath(pathfrom,pathto.fullName())
        nuke.delete(pathto)
        readgroup.setXpos(int(xpos-85))
        readgroup.setYpos(int(ypos-65))
        mergeNode.setInput(1,readgroup)
        readgroup['file'].setValue(file)
        filename = file.split('/')[-1]
        px = filename.split('_')[-4]
        py = filename.split('_')[-1].split('.')[0]
        readgroup['translate'].setValue(( int(px), int(py)))
        ms = filename.split('/')[-1].split('_')[0] +'_'+filename.split('/')[-1].split('_')[3]
        readgroup['message'].setValue(ms)
        if filename.split('/')[-1].split('_')[3][0:8] == 'disabled':
            readgroup['disable'].setValue(1)
        readgroup.setName('_Read_'+filename.split('/')[-1].split('_')[3]+'_')
        return readgroup

def createReadersGroup(files):
    nuke.selectAll()
    nuke.invertSelection()
    grp = nuke.createNode('Group')
    grp.setName('LAYERS')
    grp.begin()
    rmNodes = []
    shflNodes = []
    xpos = 0
    for f in files:
        print f
        if f[-5:] != 'empty':
            r = nuke.createNode('Read')
            r.setXpos(xpos)
            xpos += 300
            r['file'].setValue(f)
            tx = nuke.createNode('Text')
            tx['xjustify'].setValue('center')
            tx['yjustify'].setValue('center')
            tx['output'].setValue('mask')
            tx['font'].setValue('//server-3d/Project/lib/python/font/verdana.ttf')
            tx['size'].setValue(20)
            ms = f.split('/')[-1].split('_')[0] +'_'+f.split('/')[-1].split('_')[3]
            tx['message'].setValue(ms)
            bo = nuke.createNode('BlackOutside')
            po = nuke.createNode('Position')
            px = f.split('_')[-4]
            py = f.split('_')[-1].split('.')[0]
            po['translate'].setValue(( int(px), int(py)))
            sh = nuke.createNode('Shuffle')
            lnames = f.split('/')[-1].split('_')[3:-4]
            lnameS = '_'.join(lnames)
            spaseceNspl = lnameS.split(' ')
            lname = '_'.join(spaseceNspl)
            #print f
            #print lname
            nuke.Layer(lname, [lname+'.red', lname+'.green', lname+'.blue', lname+'.alpha'])
            sh['out'].setValue(lname)
            rm = nuke.createNode('Remove')
            rm['operation'].setValue('remove')
            rm['channels'].setValue('rgba')
            rmNodes.append(rm)
            shflNodes.append(sh)
        else:
            pass
    nuke.selectAll()
    nuke.invertSelection()
    mg = nuke.createNode('Merge2')
    mg['also_merge'].setValue('all')
    nuke.createNode('Output')
    nuke.selectAll()
    nuke.invertSelection()
    mgmat = nuke.createNode('Merge2')
    mgmat['sRGB'].setValue(1)
    mgmat['operation'].setValue('matte')
    i = 0
    for shuffleNodes, removeNodes in zip(shflNodes,rmNodes):
        if i == 2:
            i+=1
        mgmat.setInput(i,shuffleNodes)
        mg.setInput(i,removeNodes)
        i+=1
    mgmat.setName('PreviewMegrePassesAsMatteBlending')
    grp.end()
    return grp

def CopyPasteWithPath(absCopyNodePath,AbsPasteBeforePath):
    #absCopyNodePath = 'Group1.ColorLookup1.ColorLookup1' <- Example (node.fullName())
    nuke.root().begin()
    listfrom = absCopyNodePath.split('.')
    listto = AbsPasteBeforePath.split('.')
    deep = len(listfrom)
    i = 0
    for grp in listfrom:
        i += 1
        if grp != '':
            node = nuke.toNode(grp)
            if deep != i:
                node.begin()
            else:
                nuke.selectAll()
                nuke.invertSelection()
                n = nuke.toNode(grp)
                n.setSelected(1)
                nuke.nodeCopy("%clipboard%")
    nuke.root().begin()
    deep = len(listto)
    i = 0            
    for grp in listto:
        i += 1
        if grp != '':
            node = nuke.toNode(grp)
            if deep != i:
                node.begin()
            else:
                nuke.selectAll()
                nuke.invertSelection()
                n = nuke.toNode(grp)
                n.setSelected(1)
                PastedNode = nuke.nodePaste("%clipboard%")
    return PastedNode

def allLayersOrSelective(allayers=1):
    p = nuke.thisNode()
    gf = int(nuke.toNode('preferences')['goofy_foot'].getValue())
    gfset = 0
    if gf == 1:
      gfset = 1
      nuke.toNode('preferences')['goofy_foot'].setValue(0)
    if allayers == 1 :
        text = p['ListLayers'].getText()
        lastmerge = createMerges(p,text)[1]
        ## Last Merge Create renderNode
        if p['AddRenderNode'].getValue() == 1:
            ProjectPaste(p,lastmerge)
    else:
        text = p['listMerges'].getText()
        lists = text.split('{BREAK}')
        firstNodes = []
        p.setXpos(int(p['xpos'].getValue()-400))
        for l in lists:
            p.setXpos(int(p['xpos'].getValue()+400))
            firstNode,lastmerge = createMerges(p,l)
            firstNodes.append(firstNode)
            firstNode.setInput(0,None)
            ## Last Merge Create renderNode
            if p['AddRenderNode2'].getValue() == 1:
                ProjectPaste(p,lastmerge)
        for firstN in firstNodes:
            firstN.setInput(0,p)
    if gfset == 1:
      nuke.toNode('preferences')['goofy_foot'].setValue(1)

def CreateCustomMerge(insertbeforeNode, parms, psdNode):
    lastMergeNode = 'lastmerge'
    l = parms
    if l != '':
      blend = l.split('_')[1]
      op = l.split('_')[2]
      lnamePalki = l.split('_')[3]
      lname = lnamePalki.split('||')[0]
      file = l.split('||')[1]
      number = l.split('_')[0]
      pathfrom = psdNode.fullName() + '.' + blend
      lastMergeNode = CopyPasteWithPath(pathfrom,insertbeforeNode)
      lastMergeNode['CopyAlphaFromB'].setValue(1)
      lastMergeNode['opacity'].setValue(int(op))
      lastMergeNode.setName('_'+number +'_'+ lname+ '_')
    return lastMergeNode,file

def createMerges(psdNode, List):
    listSpl = List.split('\n\n')
    firstNode= nuke.toNode('firstFormatPSD')
    firstNode['box_width'].setValue(psdNode['box_width'].getValue())
    firstNode['box_height'].setValue(psdNode['box_height'].getValue())
    formatpath =  firstNode.fullName()
    pathto = CopyPasteWithPath(formatpath,psdNode.fullName())
    firstNode = pathto
    offset = 0
    thisGroup = 0
    xpos = pathto['xpos'].getValue()
    lastReader = None
    UPLtCCMLayers = []
    yoffsetUPLtCCM = 0
    for l in listSpl:
        thisgroup = 0
        if l != '':
          blend = l.split('_')[1]
          op = l.split('_')[2]
          lnamePalki = l.split('_')[3]
          lname = lnamePalki.split('||')[0]
          file = l.split('||')[1]
          number = l.split('_')[0]
          if lname[0:3] == 'adj':
              blend = 'Adjustment'
          if lname[0:5] == 'ingrp':
              shortName  = 'endgrp'
              thisgroup = 1
              blend = 'PSDGroup'
              offset += 100
          elif lname[0:6] == 'outgrp':
              shortName  = lname[6:].upper()
              thisgroup = 1
              blend = 'PSDGroup'
          else: pass
          pathfrom = psdNode.fullName() + '.' + blend
          parentNode = pathto
          yposParent = parentNode['ypos'].getValue()
          if 'UPLtCCM' in lname:
              UPLtCCMLayers.append(l +'&'+lastReader.name())
              yoffsetUPLtCCM += 65
          else:
              pathto.setYpos(int(pathto['ypos'].getValue())+yoffsetUPLtCCM)
              pathto = CopyPasteWithPath(pathfrom,pathto.fullName())
              ypos = pathto['ypos'].getValue()
              pathto['in'].setValue(lname)
              pathto['opacity'].setValue(int(op))
              pathto.setXpos(int(xpos)+offset)
              pathto.setName('_'+number +'_'+ lname+ '_')
              if thisgroup == 1:
                  pathto.setName('grp_' + shortName)
              if lname[0:6] == 'outgrp':
                  offset -= 100
              else: pass
              if lname[0:8] == 'disabled':
                  pathto['disable'].setValue(1)
              if lname == 'Background':
                  pathto['set_white_alpha'].setValue(1)
              pathto.setYpos(int(ypos)+65)
              lastReader = CreateReader(pathto,parentNode,file,psdNode)
              yoffsetUPLtCCM = 0
    ## Create Use prev Layer to Create Cliping Mask
    setupto = ''
    lastOTL = ''
    yposoffset = 0
    print UPLtCCMLayers
    if len(UPLtCCMLayers) > 0 :
        for otl in UPLtCCMLayers:
            parentNode = nuke.toNode(otl.split('&')[-1])
            ypos = int(parentNode['ypos'].getValue())
            l = otl.split('&')[0]
            if otl.split('&')[-1] != lastOTL:
                setupto = otl.split('&')[-1]
                newmerge,file = CreateCustomMerge(setupto,l,psdNode)
                yposoffset = 0
            else:
                newmerge,file = CreateCustomMerge(setupto,l,psdNode)
            lastOTL = otl.split('&')[-1]
            yposoffset += 65 
            newmerge.setYpos(ypos+yposoffset)
            setupto = newmerge.name()
            upltccmReader = CreateReader(newmerge,parentNode,file,psdNode)
            upltccmReader.setYpos(int(upltccmReader['ypos'].getValue()+35))
    return firstNode, pathto

def AllDependentNodes(a,n):
    deps = n.dependent()
    for dep in deps:
        if dep not in a:
            a.append(dep)
            AllDependentNodes(a,dep)
    return a
    
def TogglePostageReads(listdeps):
    i = 2
    for dep in listdeps:
        if dep.name()[0:6] == '_Read_':
            if i == 2:
                if dep['postage_stamp'].getValue() == 1:
                    dep['postage_stamp'].setValue(0)
                    i = 0
                else:
                    dep['postage_stamp'].setValue(1)
                    i = 1
            else:
                dep['postage_stamp'].setValue(i)
    
def viewNames(list_deps):
    i = 2
    for dep in list_deps:
        if dep.name()[0:6] == '_Read_':
            if i == 2:
                if dep['viewName'].getValue() == 1:
                    dep['viewName'].setValue(0)
                    i = 0
                else:
                    dep['viewName'].setValue(1)
                    i = 1
            else:
                dep['viewName'].setValue(i)

def replaceNodewithSaveConnections(sourceNODEfullname,destNodefullname):
    nuke.root().begin()
    listfrom = sourceNODEfullname.split('.')
    listto = destNodefullname.split('.')
    deep = len(listfrom)
    i = 0
    for grp in listfrom:
        i += 1
        if grp != '':
            node = nuke.toNode(grp)
            if deep != i:
                node.begin()
            else:
                nuke.selectAll()
                nuke.invertSelection()
                n = nuke.toNode(grp)
                n.setSelected(1)
                nuke.nodeCopy("%clipboard%")
    nuke.root().begin()
    deep = len(listto)
    i = 0
    for grp in listto:
        i += 1
        if grp != '':
            node = nuke.toNode(grp)
            if deep != i:
                node.begin()
            else:
                nuke.selectAll()
                nuke.invertSelection()
                PastedNode = nuke.nodePaste("%clipboard%")
    outputs = node.dependencies()
    inputs = node.dependent()
    i=0
    for o in outputs:
        PastedNode.setInput(i,o)
        i+=1
    for inp in inputs:
        i = 0
        for conection in inp.dependencies():
            if conection.name() == node.name():
                inp.setInput(i,PastedNode)
            i+=1
    px = node['xpos'].getValue()
    py = node['ypos'].getValue()
    nuke.delete(node)
    PastedNode.setXYpos(int(px),int(py))
    return PastedNode

def matchListsReplaceParms(newlist, oldrow, PSDTool):
    for newrow in newlist:
        if newrow != '':
            if oldrow.split('||')[0].split('_')[3] in newrow.split('_')[3]:
                newlist.remove(newrow)
                mNode = nuke.toNode(oldrow.split('||')[2])
                readnode = nuke.toNode(oldrow.split('||')[1])
                readnode['file'].setValue(newrow.split('||')[1])
                filename = newrow.split('||')[1].split('/')[-1]
                px = filename.split('_')[-4]
                py = filename.split('_')[-1].split('.')[0]
                readnode['translate'].setValue(( int(px), int(py)))
                ##blendmode
                if oldrow.split('_')[1] != newrow.split('_')[1]:
                    ##Replace BLEND MODE And set new Opacity set name
                    newBlendfrom = PSDTool.fullName() + '.' + newrow.split('_')[1]
                    mergeFullPath = mNode.fullName()
                    replaced_merge = replaceNodewithSaveConnections(newBlendfrom,mergeFullPath)
                    number = oldrow.split('||')[0].split('_')[0]
                    lname = oldrow.split('||')[0].split('_')[3]
                    op = newrow.split('_')[2]
                    replaced_merge['opacity'].setValue(int(op))
                    replaced_merge.setName('_'+number +'_'+ lname+ '_')
                else:
                    if oldrow.split('_')[2] != newrow.split('_')[2]:
                        mNode['opasity'].setValue(int(newrow.split('_')[2]))
                    else:pass
            else:pass
    return newlist

def ProjectPaste(psdToolNode, toNode):
    rnode = '.Project_or_Panorama_RenderGroup'
    absrpathFrom = psdToolNode.fullName() + rnode
    absrpathTO = toNode.fullName()
    rN = CopyPasteWithPath(absrpathFrom,absrpathTO)
    return rN

def toFullNode(fullName): ##Exmaple: fullname = "PSDTools.firstFormatPSD"
    if fullName == '':
        return nuke.root()
    listto = fullName.split('.')
    deep = len(listto)
    i = 0
    for grp in listto:
        i += 1
        if grp != '':
            node = nuke.toNode(grp)
            if deep != i:
                try:
                    node.begin()
                except:
                    nuke.message('This Knob:\n' + fullName+'\n\nNeed FullName')
            else:
                return nuke.toNode(grp)

def OpenPSD():
    node = nuke.thisNode()
    if node.input(0):
        lpth = node.input(0)['file'].getValue()
        psdfile = lpth.replace('/','\\')
        if os.path.isfile(lpth):
            f = 'C:/Program Files/Adobe'
            pexe = ''
            for item in os.listdir(f):
                if 'CS6' in item:
                #if 'CC' in item:
                    if os.path.isdir(f + '/' + item):
                        for fi in os.listdir(f + '/' + item):
                            if fi == 'Photoshop.exe':
                                pexe = f + '/' + item + '/' +'Photoshop.exe'
            args = pexe + ' ' + psdfile
            print args
            subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
