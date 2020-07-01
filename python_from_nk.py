#!/bin/python
import os,time,datetime,subprocess,getpass
from PySide import QtGui
from shutil import copyfile

def isdirorfileRaise(dirfile):
    if os.path.isdir(dirfile) or os.path.isfile(dirfile):
        pass
    else:
        raise Exception('Directory or File not Found:\n'+dirfile)

def CheckPathLowersUppers(path):
   pass # Found from Input DirPath or FilePath PathWithDirmapsWhere is Server-3d Mounted And Check LowerUpper Symvols 



def pathToLinnux(path_or_askLinux):
    '''
        if os is linux convert path from // to /
    '''
    #get Platform:
    from sys import platform as _platform
    if _platform == "linux" or _platform == "linux2":
        if path_or_askLinux ==  'LINUX?':
            return 1
        path = path_or_askLinux.replace('//','/')
    elif _platform == "darwin":
        if path_or_askLinux ==  'LINUX?':
            return 1
        path = path_or_askLinux.replace('//','/')
    elif _platform == "win32" or _platform == "win64":
        if path_or_askLinux ==  'LINUX?':
            return 0
        return path_or_askLinux
    return path

def panelGetProject(Button=0):
    #+++++++++PROJECTSETTINGS+++++++++++#
    Projects = ['00_UrfinJuse2','01_Piramidy','02_UrfinJuse2_dataserver','03_MALYSH']
    resolutions = ['2132X870','2048X1107','2132X870','2048X858']
    stereo_enb = [1, 0, 1, 0 ]
    
    managefolders = [pathToLinnux('//server-3d/Project/UrfinJuse2/lib/ComposeManager/ScriptsLog/'),
                      pathToLinnux('//server-3d/Project/Piramidy/lib/ComposeManager/ScriptsLog/'),
                        pathToLinnux('//dataserver/Project/UrfinJuse2/lib/ComposeManager/ScriptsLog/'),
                         pathToLinnux('//dataserver/Project/MALYSH/lib/ComposeManager/ScriptsLog/')]
    
    projectFolders = [pathToLinnux('//server-3d/Project/UrfinJuse2/scenes/'),
                        pathToLinnux('//server-3d/Project/Piramidy/scenes/'),
                          pathToLinnux('//dataserver/Project/UrfinJuse2/scenes/'),
                            pathToLinnux('//dataserver/Project/MALYSH/scenes/')]

    #projecttemplates nkfiles;pngrender;dailies;
    projectTemplates = ['ep<EP>/ep<EP>sc<SC>/compose/nuke;ep<EP>/ep<EP>sc<SC>/compose/render;ep<EP>/ep<EP>sc<SC>/compose/dailies',
                        'ep<EP>/ep<EP>sc<SC>/compose/nuke;ep<EP>/ep<EP>sc<SC>/compose/render;ep<EP>/ep<EP>sc<SC>/compose/dailies',
                        'ep<EP>/ep<EP>sc<SC>/compose/nuke;ep<EP>/ep<EP>sc<SC>/compose/render;ep<EP>/ep<EP>sc<SC>/compose/dailies',
                        'ep<EP>/ep<EP>sc<SC>/compose/nuke;ep<EP>/ep<EP>sc<SC>/compose/render;ep<EP>/ep<EP>sc<SC>/compose/dailies']
    
    outputfolders = [pathToLinnux('//server-3d/Project/UrfinJuse2/output/'),
                       pathToLinnux('//server-3d/Project/Piramidy/output/'),
                         pathToLinnux('//dataserver/Project/UrfinJuse2/output/'),
                           pathToLinnux('//dataserver/Project/MALYSH/output/')]

    #outputTemplates dpxleftfolder;dpxRightfolder;aviLeftFile;aviRightFile;
    outputTemplates = ['ep<EP>/render_dpx/ep<EP>sc<SC>/ep<EP>sc<SC>_left;ep<EP>/render_dpx/ep<EP>sc<SC>/ep<EP>sc<SC>_right;ep<EP>/ep<EP>sc<SC>_left.avi;ep<EP>/ep<EP>sc<SC>_right.avi',
                       'ep<EP>/render_dpx/ep<EP>sc<SC>/ep<EP>sc<SC>_left;ep<EP>/render_dpx/ep<EP>sc<SC>/ep<EP>sc<SC>_right;ep<EP>/ep<EP>sc<SC>_left.avi;ep<EP>/ep<EP>sc<SC>_right.avi',
                       'ep<EP>/render_dpx/ep<EP>sc<SC>/ep<EP>sc<SC>_left;ep<EP>/render_dpx/ep<EP>sc<SC>/ep<EP>sc<SC>_right;ep<EP>/ep<EP>sc<SC>_left.avi;ep<EP>/ep<EP>sc<SC>_right.avi',
                       'ep<EP>/render_tiff/ep<EP>sc<SC>;ep<EP>/ep<EP>sc<SC>.avi']
    
    sourcesFolders = [pathToLinnux('//renderserver/Project/UrfinJuse2/scenes/'),
                        pathToLinnux('//renderserver/Project/Piramidy/scenes/'),
                          pathToLinnux('//dataserver/Project/UrfinJuse2/scenes/'),
                            pathToLinnux('//dataserver/Project/MALYSH/scenes/')]
    
    #sourcetemplate
    sourcesTemplates = ['ep<EP>/ep<EP>sc<SC>/compose/',
                        'ep<EP>/ep<EP>sc<SC>/compose/',
                        'ep<EP>/ep<EP>sc<SC>/compose/',
                        'ep<EP>/ep<EP>sc<SC>/compose/']
    
    assetFolders = [pathToLinnux('//server-3d/Project/UrfinJuse2/lib/ComposeManager/Asset/'),
                      pathToLinnux('//server-3d/Project/Piramidy/lib/ComposeManager/Asset/'),
                        pathToLinnux('//dataserver/Project/UrfinJuse2/lib/ComposeManager/Asset/'),
                          pathToLinnux('//dataserver/Project/MALYSH/lib/ComposeManager/Asset/')]
    assetMirrorFolders = ['','','','']
    
    #+++++++++PROJECTSETTINGS+++++++++++#
    node = nuke.thisNode()
    #node = nuke.toNode('Manager')
    lastprojectfile = os.environ['HOME']+'\\ScriptManagerLastProject'
    from sys import platform as _platform
    if _platform == "linux" or _platform == "linux2":
        lastprojectfile = os.environ['HOME']+'/ScriptManagerLastProject'
    SetprojectNum = 0
    if Button == 1:
        p = nuke.Panel('Set Current Project')
        p.addEnumerationPulldown('Select Project:', ' '.join(Projects))
        p.addButton('Cancel')
        p.addButton('Set Project')
        result = p.show()
        if result != 0:
            userChoise = p.value('Select Project:')
            SetprojectNum = int(userChoise.split('_')[0])
            #writefileHistory
            with open(lastprojectfile,'w') as l:
                l.write(str(SetprojectNum))
        else:
            return
    else:
        #SaveContentOfBuffersOrRestore(1)
        #getSnippetCollectionForProject
        if os.path.isfile(lastprojectfile):
            with open(lastprojectfile,'r') as l:
                SetprojectNum = int(l.read())
        else:
            nuke.message('LastProject file NotFound/nSet Current Project in Preferences')
        
    node['Project'].setText(Projects[SetprojectNum])
    node['res_x'].setValue(int(resolutions[SetprojectNum].split('X')[0]))
    node['res_y'].setValue(int(resolutions[SetprojectNum].split('X')[1]))
    node['stereo'].setValue(int(stereo_enb[SetprojectNum]))
    node['mfolder_line'].setText(managefolders[SetprojectNum])
    node['a_line'].setText(assetFolders[SetprojectNum])
    node['a2_line'].setText(assetMirrorFolders[SetprojectNum])
    node['p_line'].setText(projectFolders[SetprojectNum])
    node['pt_line'].setText(projectTemplates[SetprojectNum])
    node['o_line'].setText(outputfolders[SetprojectNum])
    node['ot_line'].setText(outputTemplates[SetprojectNum])
    node['s_line'].setText(sourcesFolders[SetprojectNum])
    node['st_line'].setText(sourcesTemplates[SetprojectNum])
    Snippet()
    searchListScriptManager()
    return SetprojectNum

def getVariable(node,num=0,ep='00',sc='00',check=0):
   # 0 - User 
   # 1 - Scriptlogfolder 
   # 2 - assetFolder
   # 3 - nkscriptsFolder 
   # 4 - pngRenderFolder
   # 5 - dailiesFolder
   # 6 - outputFolder0(left)
   # 7 - outputFolder1(right)
   # 8 - outputFolder2(leftavifile) 
   # 9 - outputFolder2(rightavifile) 
   # 10 - SourceFolder
   # 11 - GlobalOutputFolder
   # 12 - EpOutputFolder
   # 13 - Template NK File
    if num == 0:
        val = node['u_line'].getText()
        if val == '$USER' or val == '':
            var = getpass.getuser()
            return var
        else:
            return val
    elif num == 1:
        val = node['mfolder_line'].getValue()
        if val != '':
            return val
        else:
            return None
    elif num == 2:
        val = node['a_line'].getValue()
        val2 = node['a2_line'].getValue()
        if val != '' or val2 != '':
            return [val,val2]
        else:
            return None
    elif num == 3 or num == 4 or num == 5:
        p = node['p_line'].getValue()
        t = node['pt_line'].getValue()
        if p != '' and t != '':
            path = p + t.split(';')[num-3].replace('<EP>',ep).replace('<SC>',sc)
            if check == 1: isdirorfileRaise(path)
            return path
    elif num == 6 or num == 7 or num == 8 or num == 9:
        o = node['o_line'].getValue()
        ot = node['ot_line'].getValue()
        if o != '' and ot != '':
            path = o + ot.split(';')[num-6].replace('<EP>',ep).replace('<SC>',sc)
            if check == 1: isdirorfileRaise(path)
            return path
    elif num == 10:
        s = node['s_line'].getValue()
        st = node['st_line'].getValue()
        if s != '' and st != '':
            path = s + st.replace('<EP>',ep).replace('<SC>',sc)
            if check == 1: isdirorfileRaise(path)
            return path
    elif num == 11:
        s = node['o_line'].getValue()
        isdirorfileRaise(s)
        return s
    elif num == 12:
        s = node['o_line'].getValue()
        path = s + 'ep' + ep
        if check == 1: isdirorfileRaise(path)
        return path
    elif num == 13:
        s = node['mfolder_line'].getValue()
        nktemplatefile =  '/'.join(s.split('/')[:-2])+'/template.nk'
        return nktemplatefile
    else:
        return None


def getLogData(scriptlogDir='',username='all',timerange=''):
    if timerange != '':
        ts = -int(timerange.split('-')[0]+'000000')
        te = -int(timerange.split('-')[1]+'999999')
    if scriptlogDir != '':
        if not os.path.isdir(scriptlogDir):
            os.makedirs(scriptlogDir)
        files = os.listdir(scriptlogDir)
        if username != 'all':
            for f in files:
                if username in f:
                    files = []
                    files.append(f)
        data = {}
        for f in files:
            fullpathfile = scriptlogDir + '/' + f
            if os.path.isfile(fullpathfile):
               with open(fullpathfile, 'r') as infile:
                   i = 0
                   limmitlinesperfile = 1000
                   for line in infile:
                       if i < limmitlinesperfile:
                           if timerange != '':
                               el = line.split('  ->  ')
                               time = -int(el[0].split('_')[1])
                               key = -int(el[0].split('_')[1]+el[0].split('_')[0]+el[0].split('_')[2])
                               if time<ts and time>te:
                                   data[key] = (el[1],el[2],el[3])
                               else:
                                   i-=1
                           else:
                               el = line.split('  ->  ')
                               key = -int(el[0].split('_')[1]+el[0].split('_')[0]+el[0].split('_')[2])
                               data[key] = (el[1],el[2],el[3])
                       i+=1
        return data

def searchPatternToTuple(searchpattern):
    excludePatterns = []
    includePatterns = []
    if searchpattern != '':
        if ';' in searchpattern:
            splist = searchpattern.split(';')
            for sp in splist:
                if sp != '':
                    if sp[0] == '^':
                        sp = sp[1:]
                        excludePatterns.append(sp)
                    else:
                        includePatterns.append(sp)
        else:
            if searchpattern[0] == '^':
                sp = searchpattern[1:]
                excludePatterns.append(sp)
            else:
                includePatterns.append(searchpattern)
        search_INCLUDE_EXCLUDE_Tuple = (includePatterns,excludePatterns)
    else:
        search_INCLUDE_EXCLUDE_Tuple = 'ALL'
    return search_INCLUDE_EXCLUDE_Tuple

def dataToLine(timestamp, scene, nkfile, actionArtist, searchPatternTuple):
    ts = abs(timestamp).__str__()
    timestamp = str(int(ts[12:16])-1000).zfill(4) + '|' +  ts[4:6]+'.'+ts[2:4]+'.20'+ts[:2]+'|'+ts[6:8]+':'+ts[8:10]+'|'+ts[16:20]
    sep = ' \t'
    ReadibleLine = sep + scene + sep + nkfile + sep + actionArtist[:-1]
    found = 0
    if searchPatternTuple != 'ALL':
        found = 0
        if len(searchPatternTuple[0]) != 0:
            for includePattern in searchPatternTuple[0]:
                if includePattern.lower() in ReadibleLine.lower():
                    found += 1
        else:
            found = 1
        if len(searchPatternTuple[1]) != 0:
            for excludePattern in searchPatternTuple[1]:
               if excludePattern.lower() in ReadibleLine.lower():
                   found = 0
        if found > 0:            
            return timestamp + ReadibleLine
        else:
            return ''
    else:
        return timestamp +ReadibleLine

def SortTextByID(dictKeyText):
    datakeys = reversed(sorted(dictKeyText))
    text = ''
    for i in datakeys:
        text += dictKeyText[i] + '\n'
    return text
    
def DataSortSearch(data, searchPattern='', ignoreRepetitions=1, maxitems=30, sortbyMontageID=0):
    datakeys = sorted(data)
    Scenes = []
    text = ''
    SearchTuple = searchPatternToTuple(searchPattern)
    if sortbyMontageID > 0:
        dictID_Readlines = {}
    i = 0
    for key in datakeys:
        if i<maxitems:
            if sortbyMontageID > 0:
                idkey = abs(key).__str__()
                if sortbyMontageID != 1:
                  ep = data[key][0].split('.')[0]
                  idkey = -int(ep+idkey[12:-4]+idkey[:-9])
                else:
                  idkey = -int(idkey[12:-4]+idkey[:-9])
            if ignoreRepetitions==1:
                if data[key][0] not in Scenes:
                    Scenes.append(data[key][0])
                    readline = dataToLine(key,data[key][0],data[key][1],data[key][2],SearchTuple)
                    if readline != '':
                        if i == 0 : sep = ''
                        else: sep = '\n'
                        text += sep + readline
                        if sortbyMontageID > 0:
                            dictID_Readlines[idkey] = readline
                        i += 1
            else:
                readline = dataToLine(key,data[key][0],data[key][1],data[key][2],SearchTuple)
                if readline != '':
                    if i == 0 : sep = ''
                    else: sep = '\n'
                    text += sep+ readline
                    if sortbyMontageID > 0:
                        dictID_Readlines[idkey] = readline
                    i += 1
    if sortbyMontageID > 0:
        text = SortTextByID(dictID_Readlines)
    return text

def dataToHEX(data):
    ##25.09.2017 to 170925
    dataspl = data.split('.')
    return dataspl[2][2:4]+dataspl[1]+dataspl[0]

def searchListScriptManager(newLinetoCopy=''):
    node = nuke.thisNode()
    maxitems = node['maxitems'].getValue()
    sorttype = 0
    byID = int(node['sortbyID'].getValue())
    byepID = int(node['sortepid'].getValue())
    sorttype = byID + byepID
    if byepID == 1:
      sorttype = 2
    showall = int(node['showallop'].getValue())
    searchpattern = node['searchtext'].getText()
    sortmy = 'all'
    if node['sortmy'].getValue() == 1:
        sortmy = getVariable(node,0)
    start = node['startdate'].getText()
    end = node['enddate'].getText()
    if start == '' or end == '':
        timerange = ''
    else:
        start = dataToHEX(start)
        end = dataToHEX(end)
        timerange = start +'-'+ end
        if len(timerange) != 13:
            timerange = ''
    data = getLogData(getVariable(node,1),sortmy,timerange)
    text = DataSortSearch(data, searchpattern, showall, maxitems,sorttype)
    node['last_changes_list'].setText(text)
    if newLinetoCopy != '':
       QtGui.QApplication.clipboard().setText(newLinetoCopy)


def timeStamp():
    TS = datetime.datetime.fromtimestamp(time.time()).strftime('%y%m%d%H%M%S')
    return TS

def addLineLog(node,oldline,newOperation='',newNKName=''):
    ## get User NAme getvariable
    user = getVariable(node,0)
    ## get dir 
    pathtofile = getVariable(node,1)+user+'_scriptsLog.txt'
    sep = '  ->  '
    sepl = ' \t'
    splitedold = oldline.split(sepl)
    montageid = str(int(splitedold[0].split('|')[0])+1000)
    durframes = splitedold[0].split('|')[-1]
    if newOperation[:6] == 'NEWID=':
        montageid = str(int(newOperation[6:])+1000)
    if newOperation[:12] == 'NEWDURATION=':
        durframes = newOperation[12:]
    ts = timeStamp()
    error = 0
    if newNKName == '' and newOperation == '':#525252#FFFFFF#FFFFFF#FFFFFF
        error = 1
    if newNKName == '':
        newNKName = splitedold[2]
    if newOperation == '':
        newOperation = '@' + user +' OPEN_NEW_VERSION'
    else:
        newOperation = '@' + user + ' ' + newOperation
    newLine = montageid + '_'+ ts +'_'+ durframes + sep + splitedold[1]+ sep + newNKName + sep + newOperation + '\n'
    newReadLine = str(int(montageid)-1000).zfill(4) + '|d|t|'+ durframes + sepl + splitedold[1]+ sepl + newNKName + sepl + newOperation + '\n'
    if error != 1:
        if not os.path.isfile(pathtofile):
            with open(pathtofile, 'w') as f:
               pass
        with open(pathtofile, 'r+') as f:
            lines = f.readlines()
            f.seek(0)
            f.write(newLine)
            f.writelines(lines)
    return newReadLine

def ViewChanges(current=0):
    node = nuke.thisNode()
    line = str(QtGui.QApplication.clipboard().text().encode('utf8', 'ignore'))
    if current == 0:
      epscnk = getEPSCformLine(line)
      searchpattern = line.split(' \t')[1] + ' '
    else:
      searchpattern = getEPSCCurent()
    data = getLogData(getVariable(node,1))
    text = DataSortSearch(data, searchpattern, 0, 100)
    node['last_changes_list'].setText(text)

def OpenWith(newSession=0,disLog=0):
    node = nuke.toNode('Manager')
    line = str(QtGui.QApplication.clipboard().text().encode('utf8', 'ignore'))
    epscnk = getEPSCformLine(line)
    dirnk = getVariable(node, 3 ,epscnk[0] ,epscnk[1],1)
    thisFile = nuke.root().name()
    nkFile = dirnk + '/' + epscnk[2]
    if newSession == 0: # Open as Source
        #save this file, delete all nodes except Maneger, and source NKfile
        save = 1
        if nuke.root().name() == 'Root':
            ask = nuke.ask('Current nk UNTITLED and NOT Saved! \nSource?:\n'+ nkFile)
            save = 0
        else:
            ask = nuke.ask('Save Current Script to:\n'+thisFile+'\n\nand Source?:\n'+ nkFile)
        if ask:
            nuke.root().begin()
            if save == 1:
                nuke.scriptSave()
            g = nuke.allNodes()
            for n in g:
                if n != node:
                    nuke.delete(n)
            nuke.scriptSource(nkFile)
            nuke.scriptSaveAs(nkFile,overwrite = 1)
            nuke.delete(nuke.toNode('Manager1'))
            nuke.delete(nuke.toNode('Manager2'))
            nuke.delete(nuke.toNode('Manager3'))
            addLineLog(node, line, 'OPEN')
    else: #Open with newSession
        if os.path.isfile(nkFile):
            nuke.scriptOpen(nkFile)
            if disLog==0:
                addLineLog(node, line, 'OPEN')

def getlastFile(directory,endfile='.nk'):
    search_dir = directory
    os.chdir(directory)
    files = filter(os.path.isfile, os.listdir(search_dir))
    files.sort(key=lambda x: os.path.getmtime(x))
    lastfile = ''
    for f in reversed(files):
        if f[-3:] == endfile:
            lastfile = f
            break
    return lastfile

def getEPSCformLine(line):
    error = 0
    if ' \t' in line:
        linespl = line.split(' \t')
        if len(linespl) == 4:
            ep = linespl[1].split('.')[0]
            sc = linespl[1].split('.')[1]
            nkfile = linespl[2]
            return [ep,sc,nkfile]
        else:
            error = 1
    else:
        error = 1
    if error == 1:
        raise Exception('For This Operation Copy to Buffer One Line from List')

def findLastNKFile(checkFile=0):
    node = nuke.thisNode()
    line = str(QtGui.QApplication.clipboard().text().encode('utf8', 'ignore'))
    epscnk = getEPSCformLine(line)
    ep = epscnk[0]
    sc = epscnk[1]
    dirNk = getVariable(node, 3 ,ep ,sc,1)
    if os.path.isdir(dirNk):
        LastFile = getlastFile(dirNk)
        if checkFile==1 or checkFile==0:
            if not os.path.isfile(dirNk+'/'+LastFile):
                raise Exception('Files not Found:\n'+dirNk+'\nUse Create New Project')
        askopen = 0
        if epscnk[2] == LastFile:
            #this LastFile in line
            askopen = nuke.ask('This NK file is Last.\nSource NK?\n\n'+LastFile)
            #return epscnk[2]
        else:
            #set newLineLog 
            nl = addLineLog(node, line, newNKName=LastFile)
            searchListScriptManager(nl)
            #askopen = nuke.ask('Founded New Version NK.\nSource NK?\n\n'+LastFile)
            #return LastFile
        #if askopen:
        #    print 'Find and Open'
        #    OpenWith()
        return LastFile
    else:
        raise Exception('Folder not Found:\n'+dirNk)

def setLastNK():
    node = nuke.thisNode()
    line = str(QtGui.QApplication.clipboard().text().encode('utf8', 'ignore'))
    epscnk = getEPSCformLine(line)
    pathfiles = getVariable(node,3,epscnk[0],epscnk[1],1)
    if os.path.isdir(pathfiles):
        #pathfiles = '//server-3d/project/UrfinJuse/scenes/ep121/ep121sc46/compose/nuke'
        os.chdir(pathfiles)
        files = filter(os.path.isfile, os.listdir(pathfiles))
        files.sort(key=lambda x: os.path.getmtime(x))
        files.reverse()
        strlist = ''
        for item in files:
            if os.path.isfile(pathfiles+'/'+item):
                strlist += ' '+item.replace(' ','__')
        p = nuke.Panel('Set Current File')
        p.addEnumerationPulldown('Select File:', strlist)
        p.addButton('Cancel')
        p.addButton('OpenAsNewSession')
        result = p.show()
        if result != 0:
            userChoise = p.value('Select File:')
            userChoise = userChoise.replace('__',' ')
            if epscnk[2] == userChoise:
                #this LastFile in line
                OpenWith(1)
                return epscnk[2]
            else:
                #set newLineLog 
                nl = addLineLog(node, line, newNKName=userChoise)
                QtGui.QApplication.clipboard().setText(nl.replace('  ->  ',' \t'))
                searchListScriptManager(nl)
                OpenWith(1)
                return userChoise
    else:
        raise Exception('Folder not Found:\n'+pathfiles)

def CheckID(f):
    error = 0
    if f.isdigit():
        return f
    else:
        if f.count('.') == 1:
            if f.split('.')[0].isdigit() and f.split('.')[1].isdigit():
                if len(f.split('.')[1]) == 1:
                    return f
                else:
                    error = 1
            else:
                error = 1
        else:
            error = 1
    if error == 1:
        raise Exception('Set ID to Number or Float (example: 22.1)\n\nwith one digit after the point\n\nCurrent: ' + str(f))

def setStatus(thisSession=0,newID=0,newDuration=0):
    node = nuke.thisNode()
    if thisSession == 0:
        line = str(QtGui.QApplication.clipboard().text().encode('utf8', 'ignore'))
        epscnk = getEPSCformLine(line)
    else:
        epscnk = getEPSCCurent(1)
        line = epscnk[3]
    if newID == 0 and newDuration == 0:
        note = node['note_line'].getText()
        nl = addLineLog(node,line,note)
        searchListScriptManager(nl)
    else:
        if newID == 1:
            checkedID = CheckID(node['inputID'].getValue())
            idfromParm = str(int(10*float(checkedID))).zfill(4)
            note = 'NEWID='+ idfromParm
            nl = addLineLog(node,line,note)
            searchListScriptManager(nl)
        if newDuration == 1:
            dpxfolder = getVariable(node,6,epscnk[0],epscnk[1],1)
            numframes = 0
            for item in os.listdir(dpxfolder):
                if item[-3:] == 'dpx':
                    numframes+=1
            note = 'NEWDURATION='+ str(numframes).zfill(4)
            nl = addLineLog(node,line,note)
            searchListScriptManager(nl)

def getEPSCCurent(astuple=0):
    f = nuke.root().name()
    epsc = ''
    nkname = f.split('/')[-1]
    for el in f.split('/'):
            if 'ep' in el and 'sc' in el:
                if epsc == '':
                    epsc = el.replace('ep','').replace('sc','.')
    ep = epsc.split('.')[0]
    sc = epsc.split('.')[1]
    oldline = 'ts \t'+ep+'.'+sc+' \t'+nkname+' \toldoperation'
    epscnk = [ep,sc,nkname,oldline]
    if astuple == 1:
        return epscnk
    return epsc+ ' '

def createNewProjectOrAddCreated(ForceCreateNew=0):
    node = nuke.thisNode()
    nep = node['new_ep'].getText()
    nsc = node['new_sc'].getText()
    notdirandsc = 0
    if nep != '' or nsc != '':
        dirNK = getVariable(node,3,nep,nsc)
        oldline = '000|ts|0000 \t'+nep+'.'+nsc+' \told.nk \toldoperation'
        QtGui.QApplication.clipboard().setText(oldline)
        if ForceCreateNew == 1:
            if nuke.ask('Create newProject in:\n' + dirNK + '\n and Create Empty NK File?'):
                if not os.path.isdir(dirNK):
                    os.makedirs(dirNK)
                nkname = 'ep'+nep+'sc'+nsc+'_v001.nk'
                if os.path.isfile(dirNK+'/'+nkname):
                    raise Exception ('The project is already created!\nUse Add Created Project to List')
                nl = addLineLog(node,oldline,newNKName=nkname)
                searchListScriptManager(nl)
                ##Create Template
                nktemplate = getVariable(node,13)
                #copyfile(nktemplate, dirNK+'/'+nkname)
                tr = ''
                with open(nktemplate, 'r') as t:
                    for line in t:
                        tr += line.replace('<EP>',nep).replace('<SC>',nsc)
                with open(dirNK+'/'+nkname, 'w') as f:
                    f.write(tr)
        else:# add to List Created
            founded = ''
            if os.path.isdir(dirNK):
                founded = findLastNKFile(1)
    else:
        nuke.message('Enter the episode and the scene in the fields: <ep> and <sc>')

def DeleteFromList():
   node = nuke.thisNode()
   line = str(QtGui.QApplication.clipboard().text().encode('utf8', 'ignore'))
   epscnk = getEPSCformLine(line)
   nep = epscnk[0]
   nsc = epscnk[1]
   founded = []
   if nep != '' or nsc != '':
      passsearchpattern = ' ' + nep + '.'+ nsc + ' '
      pathtoLog = getVariable(node,1)
      if os.path.isdir(pathtoLog):
         files = os.listdir(pathtoLog)
         for f in files:
            log = []
            pathtofile = pathtoLog+'/'+f
            if os.path.isfile(pathtofile):
               with open(pathtofile, 'r') as f:
                  lines = f.readlines()
                  for l in lines:
                     if passsearchpattern in l:
                        founded.append(l)
                     else:
                        log.append(l)
               with open(pathtofile, 'w') as f:
                  f.writelines(log)
         ##WRITEBACKUP:
         pathtoLogBackup = pathtoLog + '/backup'
         pathtoBackupFile = pathtoLogBackup + '/' + nep + '_' + nsc + '.backup'
         if os.path.isfile(pathtoBackupFile):
            with open(pathtoBackupFile, 'r+') as f:
               f.writelines(founded)
         else:
            with open(pathtoBackupFile, 'w+') as f:
               f.writelines(founded)
      searchListScriptManager()
   else:
      nuke.message('Enter the episode and the scene in the fields: <ep> and <sc>')

def ffmpegCommand(in_path, path_to_file):
    #\\dataserver\Project\lib\soft\ffmpeg\bin
    ffmpeg_command = '//dataserver/Project/lib/soft/ffmpeg/bin/ffmpeg  -r 24 -i ' + in_path + r' -c:v libxvid -q:v 0 -b 100000 -vf colormatrix=bt601:bt709 -g 1 -r 24 ' + path_to_file
    #ffmpeg_command = '//server-3d/project/lib/soft/ffmpeg/bin/ffmpeg  -r 24 -i ' + in_path + r' -c:v mpeg4 -vtag xvid  -q:v 1 -b:v 555k -vf colormatrix=bt601:bt709 -g 1 -r 24 ' + path_to_file
    #args = ['//server-3d/project/lib/soft/ffmpeg/bin/ffmpeg', '-r', '24', '-i', in_path , '-c:v', 'libxvid', '-q:v', '0', '-b','50000', '-vf', 'colormatrix=bt601:bt709', '-g', '1', '-r', '24', path_to_file]
    #subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
    #cmd = 'ffmpeg_command {}'.format(ffmpeg_command)
    print '--------------------------------------------------'
    print ffmpeg_command
    f_ffmpeg = subprocess.call(ffmpeg_command)

def CreateStills(forthissseeion=0,line=''):#Create for episode incremental frames sequence And DailiesStills For SpreadSheet
   node = nuke.thisNode()
   addline = 0
   if line == '':
      addline = 1
      if forthissseeion==0:
         line = str(QtGui.QApplication.clipboard().text().encode('utf8', 'ignore'))
         epsc = getEPSCformLine(line)
      else: 
         epsc = getEPSCCurent(1)
         line = epsc[3]
   else:
      epsc = getEPSCformLine(line)
   pngFolder = getVariable(node,4,epsc[0],epsc[1])
   pngIncrementMontageFolder = '/'.join(pngFolder.split('/')[:-3])+'/montage/incrementMontageSeq/'
   mID = line.split(' \t')[0].split('|')[0]
   fLenght = line.split(' \t')[0].split('|')[-1]
   if mID != '0000' or fLenght != '0000':
       intframes = int(fLenght)
       ##Create Dailie Still For SpreadSheet
       dailiesFolder = getVariable(node,5,epsc[0],epsc[1])
       dailiStillsFolder = dailiesFolder + '/stills/'
       ##Create 10frames
       if mID != '0000' and fLenght !='0000':
          if not os.path.isdir(pngIncrementMontageFolder):
             os.makedirs(pngIncrementMontageFolder)
          incrementfilenums = [1,int(intframes*0.111),int(intframes*0.222),int(intframes*0.333),int(intframes*0.444),int(intframes*0.555),int(intframes*0.666),int(intframes*0.777),int(intframes*0.888),intframes]
          i = (int(mID)-1)*10
          for frame in range(0,9):
             if incrementfilenums[frame] == 0: incrementfilenums[frame] = 1
          for frame in incrementfilenums:
             filePNGfrom = pngFolder + '/ep' + epsc[0] + 'sc' + epsc[1] + '_left_' + str(frame).zfill(4) + '.png'
             frameinIncriment = i+1
             filePNGto = pngIncrementMontageFolder + 'ep' + epsc[0] + '_' + str(frameinIncriment).zfill(4) + '.png'
             i+=1
             copyfile(filePNGfrom, filePNGto)
          if not os.path.isdir(dailiStillsFolder):
             os.makedirs(dailiStillsFolder)
          midFrame = 1#FirstFrame intframes/2
          filePNGto = dailiStillsFolder + 'ep'+ epsc[0] +'sc'+ epsc[1] +'_still_oldv001.png'
          filePNGfrom = pngFolder + '/ep' + epsc[0] + 'sc' + epsc[1] + '_left_' + str(int(midFrame)).zfill(4) + '.png'
          stills = os.listdir(dailiStillsFolder)
          if len(stills) == 0:
             copyfile(filePNGfrom, filePNGto)
             #Copy Mid Still
          else:
             ##Rename Stills in folder with shifft number AndCopy oldv001
             for st in reversed(stills):
                number = st.split('.')[0][-3:]
                NewNum = str(int(number)+1).zfill(3)
                newName = st.replace(number,NewNum)
                os.rename(dailiStillsFolder+st,dailiStillsFolder+newName)
                copyfile(filePNGfrom, filePNGto)
       else:
          raise Exception('For this Operation need Set ID and Frame Duration')

       if addline == 1:
          nl = addLineLog(node,line,'COPYSTILLS')
          searchListScriptManager(nl)
   else:
       return 0

def createAVI(Choise=0, forthissseeion=0,Stills=0):
    node = nuke.thisNode()
    if forthissseeion==0:
        line = str(QtGui.QApplication.clipboard().text().encode('utf8', 'ignore'))
        epsc = getEPSCformLine(line)
    else: 
        epsc = getEPSCCurent(1)
        line = epsc[3]
    if Stills == 1:
        CreateStills(0,line)
    pngFolder = getVariable(node,4,epsc[0],epsc[1])
    dailieFolder = getVariable(node,5,epsc[0],epsc[1])
    dailiePathName = ''
    #Choise = int(node['createavi_menu'].getValue())
    '''if Choise == 0 or Choise == 1: #Create Dalise
        renderfiles = os.listdir(pngFolder)
        renderfiles = sorted(renderfiles)
        firstframe = ''
        for f in renderfiles:
            if firstframe == '':
                if f[-3:] == 'png' or f[-3:] == 'jpg':
                    firstframe = f
                    break
        infile = pngFolder +'/'+ firstframe.replace('0001','%04d')
        dailiePathName = ''
        if os.path.isdir(dailieFolder) == False:
            os.mkdir(dailieFolder)
            dailiePathName =dailieFolder+ '/ep' + epsc[0] + 'sc' + epsc[1] + '_dailies_v001.avi'
        else:
            lastdailie = getlastFile(dailieFolder,endfile='avi')
            if lastdailie != '':
                lastnumber = ''
                ifnumber = 0
                for ch in lastdailie[::-1]:
                    if ch.isdigit():
                        if ifnumber == 0 or ifnumber == 1:
                           ifnumber = 1
                           lastnumber = ch + lastnumber
                    else: #Bukva
                        if ifnumber == 1:
                           break
                padding = len(lastnumber)           
                s = int(lastnumber)+1
                newnumber = str(s).zfill(padding)
                lastdailie = lastdailie.replace(lastnumber,newnumber)
                dailiePathName = dailieFolder+'/'+lastdailie
            else:
                dailiePathName =dailieFolder+ '/ep' + epsc[0] + 'sc' + epsc[1] + '_dailies_v001.avi'
                newnumber = '001'
        print infile,dailiePathName
        ffmpegCommand(infile, dailiePathName)'''
    if Choise == 1 or Choise == 2: ##CreateUncompress
        #get_dpx sequence
        if int(node['stereo'].getValue()) == 0:
            dpxdir = getVariable(node,6,epsc[0],epsc[1],1)
            avifull_path = getVariable(node,7,epsc[0],epsc[1],0)
            
            #avifull_path = '\\'+avifull_path.replace('/','\\')
            dailiePathName = avifull_path
            print dailiePathName
            print dpxdir
            lReader = LoadSequenceFromDir(dpxdir,'tiff')
            print lReader
            #dpxdir = '\\'+dpxdir.replace('/','\\')
            first = int(lReader[0]['first'].getValue())
            last = int(lReader[0]['last'].getValue())
            res_x = int(node['res_x'].getValue())
            res_y = int(node['res_y'].getValue())
            fps = int(nuke.root()['fps'].getValue())
            TS = timeStamp()
            ts = str(TS)
            datatime = ts[6:8]+':'+ts[8:10]+' '+ts[4:6]+'_'+ts[2:4]+'_'+ts[0:2]
            TITLE = 'MLS ep'+epsc[0]+'sc'+epsc[1] +' '+ datatime
            if os.path.isfile(avifull_path):
                os.remove(avifull_path)
            if Choise == 1:
                template_text = r'"\\dataServer\Project\lib\soft\Pdplayer64_1.07\pdplayer64.exe" --timeline='+ str(last+1) + r' --wa_begin='+str(first)+r' --wa_end='+ str(last+1) + r' --time=33 --back_color=0,0,0 --safe_area=none --mask_type=none --mask_size='+ str(res_x) + r','+ str(res_y) + r' --fps='+str(fps)+r' --zoom=100 --pan=0,0 --frame_base=0 --global_aspect=1 --apply_transforms_to_mask=0 --stereo_view=left "'+dpxdir+r'" --name="ep31sc01_left" --begin=1 --alpha=ignore --color_space=default --disable_caching=0 --new_text_layer='+ str(res_x) + r','+ str(res_y) + r','+ str(last+1) + r' --text_align_x=left --text_align_y=bottom --text_font="Arial" --text_size=24 --text_bold=0 --text_italic=0 --text_color=255,255,255 --text_outline_color=none --text_shadow_color=none --text_back_color=none --text_back_cover_layer=0 --text=0,0,"'+ TITLE + r'" --name="text_name" --position=200,-80 --alpha=pm --color_space=default --new_text_layer='+ str(res_x) + r','+ str(res_y) + r','+ str(last+1) + r' --text_align_x=right --text_align_y=bottom --text_font="Arial" --text_size=24 --text_bold=0 --text_italic=0 --text_color=255,255,255 --text_outline_color=none --text_shadow_color=none --text_back_color=none --text_back_cover_layer=0 --text=0,0,"{timeline:frame}" --name="ti_text_name" --position=-241,-80 --alpha=pm --color_space=default  --save_mask_as_sequence='+avifull_path+', --exit'
            if Choise == 2: # Make NoTEXT
                template_text = r'"\\dataServer\Project\lib\soft\Pdplayer64_1.07\pdplayer64.exe" --timeline='+ str(last+1) + r' --wa_begin='+str(first)+r' --wa_end='+ str(last+1) + r' --time=33 --back_color=0,0,0 --safe_area=none --mask_type=none --mask_size='+ str(res_x) + r','+ str(res_y) + r' --fps='+str(fps)+r' --zoom=100 --pan=0,0 --frame_base=0 --global_aspect=1 --apply_transforms_to_mask=0 --stereo_view=left "'+dpxdir+r'" --name="ep31sc01_left" --begin=1 --alpha=ignore --color_space=default --disable_caching=0 --save_mask_as_sequence='+avifull_path+', --exit'
            print 'Generate Avi ------------------- :'
            print template_text
            p = subprocess.Popen(template_text, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            print p
        #with nuke.root().begin():
        #    op = getVariable(node,11)
        #    #path_toVdpx = op + 'ep' + epsc[0] + '/render_dpx/ep' + epsc[0] + 'sc' + epsc[1] + '/ep' + epsc[0] + 'sc' + epsc[1] + '_%V/ep' + epsc[0] + 'sc' + epsc[1] + '_%v_%04d.dpx'
        #    path_toVdpx = op + 'ep' + epsc[0] + '/render_dpx/ep' + epsc[0] + 'sc' + epsc[1] + '/ep' + epsc[0] + 'sc' + epsc[1] + '_%04d.dpx'
        #    dailiePathName = op + 'ep' + epsc[0] + '/ep' + epsc[0] + 'sc' + epsc[1] + '.avi'
        #    w_node = nuke.createNode('Write')
        #    w_node.knob('file').setValue(path_toVdpx)
        #    import nukeautomation.dailies_manager.dailies_gui as dg;reload(dg);dg.convert_from_nuke_node()
        #    nuke.delete(w_node)
    if Choise == 0:
        if Stills==1:
            nl = addLineLog(node,line,'CREATED_DAILIES+AVI+STILLS: v'+newnumber)
        else:
            nl = addLineLog(node,line,'CREATED_DAILIES+AVI: v'+newnumber)
    #if Choise == 1:
    #    nl = addLineLog(node,line,'CREATED_DAILIES: v'+newnumber)
    if Choise == 2 or Choise == 1:
        nl = addLineLog(node,line,'CREATED_AVI')
    if nuke.ask('Created Dailies!\nPath to avi File:\n'+dailiePathName+'\n\n copied to Buffer\nOpen Folder with AVI?\n'):
        pf = '/'.join(avifull_path.split('/')[:-1])
        if os.path.isdir(pf):
            outFolder = 'file:' + pf
            print outFolder
            import webbrowser as wb
            wb.open(outFolder)
        else:
            nuke.message('Not found this Folder:\n' + pf)
    node.begin()
    nuke.delete(lReader[0])
    searchListScriptManager(nl)
    QtGui.QApplication.clipboard().setText('\\'.join(avifull_path.split('/')))

def OpenFolder(Choise=0,forthissseeion=0):
    node = nuke.thisNode()
    if forthissseeion==0:
        line = str(QtGui.QApplication.clipboard().text().encode('utf8', 'ignore'))
        epsc = getEPSCformLine(line)
    else: 
        epsc = getEPSCCurent(1)
        line = epsc[3]
    #Choise = int(node['folder_menu'].getValue())
    path = ''
    if Choise == 0:
        path = getVariable(node,10,epsc[0],epsc[1])
    elif Choise == 1:
        path = getVariable(node,3,epsc[0],epsc[1])
    elif Choise == 2:
        path = getVariable(node,6,epsc[0],epsc[1])
    elif Choise == 3:
        path = getVariable(node,7,epsc[0],epsc[1])
    elif Choise == 4:
        path = getVariable(node,12,epsc[0],epsc[1])
    elif Choise == 5:
        path = getVariable(node,4,epsc[0],epsc[1])
    elif Choise == 6:
        path = getVariable(node,5,epsc[0],epsc[1])
    if os.path.isdir(path):
        outFolder = 'file:' + path
        print outFolder
        import webbrowser as wb
        wb.open(outFolder)
    else:
        nuke.message('Not found this Folder:\n' + path)

def getFirstNumFrameFile(filename):
    numer = 0
    firstframe = ''
    for ch in filename[::-1]:
        if numer == 0 or ch.isdigit():
            if ch.isdigit():
                firstframe = ch + firstframe
                numer = 1
        else:
            break        
    return firstframe

def LoadSequenceFromDir(directory,endfile):
    readers = []
    len_ext = len(endfile)
    with nuke.root().begin():
        files = os.listdir(directory)
        count = 1
        counts = []
        sequences = []
        WithoutDigitName = ''
        seqfiles = []
        for f in sorted(files):
            if endfile == f[-len_ext:]:
                WithoutDigitName = ''.join([i for i in f if not i.isdigit()])
                if WithoutDigitName not in  sequences:
                    if len(sequences) > 0:
                        count = 1
                    sequences.append(WithoutDigitName)
                    seqfiles.append(f)
                    counts.append(count)
                else:
                    count += 1
                    counts.append(count)
        if len(counts) > 0:
            numberofframes = max(counts)
            for seqF in seqfiles:
                firstFrame = getFirstNumFrameFile(seqF)
                intFF = int(firstFrame)
                intLF = int(firstFrame)+(numberofframes-1)
                padding = len(firstFrame)
                read = nuke.createNode('Read')
                read['file'].fromUserText(directory+'/'+seqF.replace(firstFrame,'%0'+str(padding)+'d'))
                read['first'].setValue(intFF)
                read['last'].setValue(intLF)
                readers.append(read)
    return readers

def getDirsWithEXR(directory,dirlist):
    for item in os.listdir(directory):
        itempath = directory+'/'+item
        if os.path.isdir(itempath):
            rawcontentdir = str(os.listdir(itempath))
            if 'exr' in rawcontentdir:
                dirlist.append(itempath)
            getDirsWithEXR(itempath,dirlist)

def LoadIntoNuke(Choise=0,forthissseeion=0):
    node = nuke.thisNode()
    if forthissseeion==0:
        line = str(QtGui.QApplication.clipboard().text().encode('utf8', 'ignore'))
        epsc = getEPSCformLine(line)
    else: 
        epsc = getEPSCCurent(1)
        line = epsc[3]
    #Choise = int(node['load_menu'].getValue())
    if Choise == 0:#LOAD DPX
        if int(node['stereo'].getValue()) == 0:
            dpxdir = getVariable(node,6,epsc[0],epsc[1],1)
            print dpxdir
            lReader = LoadSequenceFromDir(dpxdir,'tiff')
        else:
            dpxdirleft = getVariable(node,6,epsc[0],epsc[1],1)
            dpxdirright = getVariable(node,7,epsc[0],epsc[1],1)
            lReader = LoadSequenceFromDir(dpxdirleft,'tiff')
            rReader = LoadSequenceFromDir(dpxdirright,'tiff')
            with nuke.root().begin():
                nuke.selectAll()
                nuke.invertSelection()
                lReader[0].setSelected(1)
                rReader[0].setSelected(1)
                nuke.createNode('JoinViews')
    if Choise == 1:#LOAD PNG
        PNGdir = getVariable(node,4,epsc[0],epsc[1],1)
        readers = LoadSequenceFromDir(PNGdir,'png')
        with nuke.root().begin():
            nuke.selectAll()
            nuke.invertSelection()
            readers[0].setSelected(1)
            readers[1].setSelected(1)
            nuke.createNode('JoinViews')
    if Choise == 2:#LOAD LastDailies
        Dailiesdir = getVariable(node,5,epsc[0],epsc[1],1)
        lastfile = getlastFile(Dailiesdir, 'avi')
        with nuke.root().begin():
            if lastfile != '':
                read = nuke.createNode('Read')
                read['file'].fromUserText('mov64:'+Dailiesdir+'/'+lastfile)
                read['first'].setValue(1)
                l = read['last'].getValue()
                read['last'].getValue(int(l)+1)
            else:
                nuke.message('Dailies Not Found')
    if Choise == 3: #Load OutputAVI
        leftrightAVI = [getVariable(node,8,epsc[0],epsc[1],1),getVariable(node,9,epsc[0],epsc[1],1)]
        readers = []
        with nuke.root().begin():
            for avi in leftrightAVI:
                read = nuke.createNode('Read')
                read['file'].fromUserText(avi)
                read['first'].setValue(1)
                l = read['last'].getValue()
                read['last'].getValue(int(l)+1)
                readers.append(read)
            nuke.selectAll()
            nuke.invertSelection()
            for r in readers:
                r.setSelected(1)
            nuke.createNode('JoinViews')
    if Choise == 4: #Load Sources
        sourcespath = getVariable(node,10,epsc[0],epsc[1],1)
        dirlist = []
        getDirsWithEXR(sourcespath,dirlist)
        with nuke.root().begin():
            st = nuke.createNode('StickyNote')
            firstXpos = int(st['xpos'].getValue())
            firstYpos = int(st['ypos'].getValue())
            nuke.delete(st)
        readgroups = []
        for exrdir in dirlist:
            readgroups.append({'/'.join(exrdir.split('/')[-3:]):LoadSequenceFromDir(exrdir,'exr')})
        lastgrp = ''
        for group in readgroups:
            key = group.keys()[0]
            listnodes = group.values()[0]
            st = nuke.createNode('StickyNote')
            st['xpos'].setValue(firstXpos)
            st['ypos'].setValue(firstYpos+175)
            if 'left' in key.lower():
                st['tile_color'].setValue(1526684671)
            if 'right' in key.lower():
                st['tile_color'].setValue(4250754815)
            firstYpos = firstYpos+175
            Yposnodes = firstYpos+50
            if lastgrp.lower().replace('left','').replace('right','') == key.lower().replace('left','').replace('right',''):
                firstYpos = firstYpos+100
            st['label'].setValue(key+':')
            st['note_font_size'].setValue(40)
            xposoffsetnode = 0
            lastgrp = key
            i = 1
            numnodes = len(listnodes)
            for node in listnodes:
                node['xpos'].setValue(firstXpos+xposoffsetnode)
                node['ypos'].setValue(Yposnodes)
                if i != numnodes:
                    node['postage_stamp'].setValue(0)
                xposoffsetnode += 150
                i+=1

def View(Choise=0,forthissseeion=0):
    node = nuke.thisNode()
    if forthissseeion==0:
        line = str(QtGui.QApplication.clipboard().text().encode('utf8', 'ignore'))
        epsc = getEPSCformLine(line)
    else: 
        epsc = getEPSCCurent(1)
        line = epsc[3]
    #Choise = int(node['view_menu'].getValue())
    if Choise == 0: ## ViewLastDilies
        Dailiesdir = getVariable(node,5,epsc[0],epsc[1],1)
        lastfile = getlastFile(Dailiesdir, 'avi')
        pathToOpen = Dailiesdir+'/'+lastfile
        winPathToOpen = '\\'.join(pathToOpen.split('/'))
    elif Choise == 1: ## ViewPNG
        pngdir = getVariable(node,4,epsc[0],epsc[1],1)
        firstfile = os.listdir(pngdir)[0]
        pathToOpen = pngdir+'/'+firstfile
        winPathToOpen = '\\'.join(pathToOpen.split('/'))
    elif Choise == 2: ## ViewDPXLeft
        dpxleftdir = getVariable(node,6,epsc[0],epsc[1],1)
        firstfile = os.listdir(dpxleftdir)[0]
        pathToOpen = dpxleftdir+'/'+firstfile
        winPathToOpen = '\\'.join(pathToOpen.split('/'))
    elif Choise == 3: ## ViewDPXRight
        dpxrightdir = getVariable(node,7,epsc[0],epsc[1],1)
        firstfile = os.listdir(dpxrightdir)[0]
        pathToOpen = dpxrightdir+'/'+firstfile
        winPathToOpen = '\\'.join(pathToOpen.split('/'))
    elif Choise == 4: ## ViewAVILeft
        AviLeftFile = getVariable(node,8,epsc[0],epsc[1],1)
        winPathToOpen = '\\'.join(AviLeftFile.split('/'))
    elif Choise == 5: ## ViewAVIRight
        AviLeftFile = getVariable(node,9,epsc[0],epsc[1],1)
        winPathToOpen = '\\'.join(AviLeftFile.split('/'))
    else:
        nuke.message('dontknow')
    PATHLIN = toggleConvertPath(winPathToOpen)
    pdpcmdcontent = '--back_color=0,0,0\n--safe_area=none\n--mask_type=none\n--mask_size=2100,858\n--fps=24\n--frame_base=1\n--global_aspect=1\n--apply_transforms_to_mask=0\n\n"'+ PATHLIN +'"\n--alpha=ignore\n--color_space=default\n--disable_caching=1\n'
    pdpFile = os.environ['HOME']+'\\tempView.pdpcmd'
    with open(pdpFile , 'w') as b:
            b.write(pdpcmdcontent)
    if os.path.isfile(winPathToOpen):
        subprocess.Popen(["//dataServer/Project/lib/soft/Pdplayer64_1.07/pdplayer64.exe", pdpFile], stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
        #subprocess.Popen(['//server-3d/Project/lib/soft/Pdplayer/pdplayer.exe', pdpFile], stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
        #os.startfile(winPathToOpen)
    else:
        nuke.message('Not Found File:\n'+winPathToOpen)

def viewMultiple(Choise=0):
   #0 - Appended LastDailies; 1 - Incremental Montage; 2 - SpreadSheet; 3 - as Layers
   node = nuke.thisNode()
   line = str(QtGui.QApplication.clipboard().text().encode('utf8', 'ignore'))
   buff = line.split('\n')
   if Choise == 0: # View Last Dailies
      pdcmd = '--back_color=0,0,0\n--safe_area=none\n--mask_type=none\n--mask_size=2132,870\n--fps=24\n--zoom=40\n--pan=-47,32\n--frame_base=0\n--global_aspect=1\n--apply_transforms_to_mask=0\n'
      beginFrame = 1
      for line in buff:
         if line == '':
            raise Exception('Copy Multiple Lines to Buffer')
         duration = line.split(' \t')[0].split('|')[-1]
         epsc = getEPSCformLine(line)
         Dailiesdir = getVariable(node,5,epsc[0],epsc[1],1)
         lastfile = getlastFile(Dailiesdir, 'avi')
         pathToOpen = Dailiesdir+'/'+lastfile
         pdcmd += '\n"'+pathToOpen+'"\n'
         pdcmd += '--begin='+str(beginFrame)+'\n--alpha=ignore\n'
         beginFrame += int(duration)
      pdcmd += '\n--timeline='+str(beginFrame)+'\n--wa_begin=1\n--wa_end='+str(beginFrame)+'\n--time=1'
   if Choise == 1: #ViewIncrementalMontageOf Ep
      epsc = getEPSCformLine(buff[0])
      pngFolder = getVariable(node,4,epsc[0],epsc[1],1)
      pngIncrementMontageFolder = '/'.join(pngFolder.split('/')[:-3])+'/montage/incrementMontageSeq/'
      if os.path.isdir(pngIncrementMontageFolder):
         files = os.listdir(pngIncrementMontageFolder)
         firstfile = files[0]
         firstnum = firstfile[-8:-4]
         firstfile = files[-1]
         lastnum = firstfile[-8:-4]
         fullPathFile = pngIncrementMontageFolder + firstfile.replace(lastnum,'####')
         pdcmd = '--back_color=0,0,0\n--safe_area=none\n--mask_type=none\n--mask_size=2132,870\n--fps=3\n--zoom=40\n--pan=-47,32\n--frame_base=0\n--global_aspect=1\n--apply_transforms_to_mask=0\n'
         pdcmd += '\n"'+fullPathFile+'"\n'
         pdcmd += '--begin='+str(int(firstnum))+'\n--alpha=ignore\n'
         pdcmd += '\n--timeline='+str(int(lastnum))+'\n--wa_begin='+str(int(firstnum))+'\n--wa_end='+str(int(lastnum))+'\n--time='+str(int(firstnum))
      else:
         nuke.message('Not Folder For incremental Montage')
   if Choise == 2: #View Spreadsheet of BufferLines
      pdcmd = '--time=0\n--back_color=0,0,0\n--safe_area=none\n--mask_type=none\n--mask_size=2132,870\n--fps=3\n--zoom=20\n--pan=-230,54\n--frame_base=0\n--global_aspect=1\n--apply_transforms_to_mask=0\n--stereo_view=left\n--stereo_mode=anaglyph'
      colums = 5
      icol = 0
      hoffset = 0
      istring = 0
      voffset = 0
      for line in buff:
         if line == '':
            raise Exception('Copy Multiple Lines to Buffer')
         epsc = getEPSCformLine(line)
         Dailiesdir = getVariable(node,5,epsc[0],epsc[1],1)
         dailieStillFile = Dailiesdir + '/stills/ep'+ epsc[0] +'sc'+ epsc[1] +'_still_oldv###.png'
         pdcmd += '\n\n"'
         pdcmd += dailieStillFile
         pdcmd +=  '"\n--alpha=ignore\n--color_space=default\n--disable_caching=0'
         if icol < 5:
            hoffset = 2132*icol
            icol +=1
         else:
            istring += 1
            voffset = 870 * istring
            hoffset = 0
            icol = 1
         pdcmd += '\n--position=' + str(hoffset) + ',' + str(voffset)
      
      pdcmd += '\n\n--timeline=10\n--wa_begin=0\n--wa_end=10'
   if Choise == 3:#View All Dailies As Layers in PDPlayer
      epsc = getEPSCformLine(buff[0])
      Dailiesdir = getVariable(node,5,epsc[0],epsc[1],1)
      pdcmd = '--back_color=0,0,0\n--safe_area=none\n--mask_type=none\n--mask_size=2132,870\n--fps=24\n--zoom=40\n--pan=-47,32\n--frame_base=1\n--global_aspect=1\n--apply_transforms_to_mask=0\n'
      for f in os.listdir(Dailiesdir):
         if f[-3:] == 'avi':
            fpath = Dailiesdir+'/'+f
            pdcmd += '\n"'
            pdcmd += fpath
            pdcmd +=  '"\n--alpha=ignore\n--color_space=default\n--disable_caching=0'
   tmpDir = os.getenv('temp')
   tmpFile = tmpDir + '\\temp.pdpcmd'
   tmpFile = toggleConvertPath(tmpFile)
   with open(tmpFile, 'w') as tmp:
      tmp.write(pdcmd)
   tmpFile = toggleConvertPath(tmpFile)
   QtGui.QApplication.clipboard().setText(tmpFile)
   if nuke.ask('Writed:\n'+tmpFile+'\nthis path copyed to clipboard\n\nRun PdPlayer?'):
      #os.system('//server-3d/Project/lib/soft/Pdplayer/pdplayer.exe "'+tmpFile+'"')
      subprocess.Popen(["//dataServer/Project/lib/soft/Pdplayer64_1.07/pdplayer64.exe", tmpFile], stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
      #subprocess.Popen(['//server-3d/Project/lib/soft/Pdplayer/pdplayer.exe', tmpFile], stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)

def CopyToBufferThisSessionLine():
    node = nuke.thisNode()
    epsc = getEPSCCurent(1)
    line = epsc[3]
    patternEPSC = ' '+epsc[0]+'.'+epsc[1]+' '
    dirOfLogs = getVariable(node,1)
    Founded = {}
    for f in os.listdir(dirOfLogs):
        filepath = dirOfLogs+'/'+f
        if os.path.isfile(filepath):
            with open(filepath, 'r') as infile:
                for l in infile:
                    if patternEPSC in l:
                        el = l.split('  ->  ')
                        ID = str(int(el[0].split('_')[0])-1000).zfill(4)
                        DUR = el[0].split('_')[2]
                        sep = ' \t'
                        readline = ID + '|00.00.0000|00:00|' + DUR + sep + el[1] + sep + el[2] + sep + el[3]
                        QtGui.QApplication.clipboard().setText(readline)
                        break
                        
def CopyToBuffer(Choise=0,forthissseeion=0):
   node = nuke.thisNode()
   if forthissseeion==0:
      line = str(QtGui.QApplication.clipboard().text().encode('utf8', 'ignore'))
      epsc = getEPSCformLine(line)
   else: 
      epsc = getEPSCCurent(1)
      line = epsc[3]
   #Choise = int(node['copy_menu'].getValue())
   if Choise == 0 or Choise == 1: # Last Dailies copy to Buffer
      Dailiesdir = getVariable(node,5,epsc[0],epsc[1])
      lastfile = getlastFile(Dailiesdir, 'avi')
      pathToOpen = Dailiesdir+'/'+lastfile
      if Choise == 1:
         pathToOpen = '\\'.join(pathToOpen.split('/'))
      QtGui.QApplication.clipboard().setText(pathToOpen)
   if Choise == 2 or Choise == 3: # nkFile copy to Buffer
      nkdir = getVariable(node,3,epsc[0],epsc[1])
      nkfile = epsc[2]
      pathToOpen = nkdir+'/'+nkfile
      if Choise == 3:
         pathToOpen = '\\'.join(pathToOpen.split('/'))
      QtGui.QApplication.clipboard().setText(pathToOpen)
   if Choise == 4: #find TablePath
      patternEPSC = ' '+epsc[0]+'.'+epsc[1]+' '
      dirOfLogs = getVariable(node,1)
      Founded = {}
      for f in os.listdir(dirOfLogs):
         filepath = dirOfLogs+'/'+f
         if os.path.isfile(filepath):
            with open(filepath, 'r') as infile:
               for l in infile:
                  if patternEPSC in l:
                     if 'table:' in l:
                        key = l.split('_')[1]
                        Founded[-int(key)] = l
      if len(Founded) > 0: 
         lasttableStatusByDate = sorted(Founded)[0]
         lastline = Founded[lasttableStatusByDate]
         link = lastline.split('  ->  ')[-1].split(' ')[1:]
         QtGui.QApplication.clipboard().setText(' '.join(link)[:-1])
      else:
         nuke.message('Link to Table Not Found')

def toggleConvertPath(inp=''):
    if inp == '':
       line = str(QtGui.QApplication.clipboard().text().encode('utf8', 'ignore'))
    else: 
       line = inp
    if line[0] == '/': #confert to win \
        newline = '\\'.join(line.split('/'))
    else: #confert to unix 
        newline = '/'.join(line.split('\\'))
    if inp == '':
        QtGui.QApplication.clipboard().setText(newline)
    return newline

def Snippet(mode=0,recursive=0):
    node = nuke.thisNode()
    if recursive== 1:
        node = nuke.toNode('Manager')
    snippetDirs = getVariable(node,2) #withoutmirror
    userName = getVariable(node,0)
    srch = node['srch_snippet'].getValue()
    text = ''
    Folder_List = []
    if mode==0: #FindAllSnipets (Restore)
        for d in snippetDirs:
            if d != '':
                if os.path.isdir(d):
                    for folder in os.listdir(d):
                        if folder not in Folder_List:
                            if srch == '': #Find All
                                Folder_List.append(d+folder)
                            else:
                                if srch.lower() in '_'.join(folder.lower().split('_')[:-1]):
                                    Folder_List.append(d+folder)
                                else:
                                    continue
                else:
                    pass
            else:
                pass
        for f in Folder_List:
            #get descriptionFile
            name = ''
            for i in os.listdir(f):
                if i[0] == '#':
                    name = i
                    break
                else:
                    name = '#Not Description'
            if pathToLinnux('LINUX?') == 1:
                text += name + '\n'
            else:
                text += name.decode('cp1251').encode('utf8', 'ignore') + '\n'
            if node['ShowStickyVersion'].getValue() == 0:
                text += f + '/nodes.nk'
            else:
                text += f + '/nodes_sticky.nk'
            text += '\n\n'
        node['snippetList'].setText(text)
        return
    elif mode==1: #SaveSnippet Open Panel (Name Description)
        nuke.root().begin()
        if len(nuke.selectedNodes()) != 0:
            p = nuke.Panel('New Snippet')
            p.addSingleLineInput('NameTags:','')
            p.addNotepad('Description:','')
            p.addButton('Cancel')
            p.addButton('Create New Snippet')
            result = p.show()
            if result == 1:
                desciption = p.value('Description:')
                name = p.value('NameTags:')
                chars_to_remove = ['.', '?', '|', '\\', '/', '<' , '>' , '*', '"' , ':']
                for ch in chars_to_remove:
                    desciption = desciption.replace(ch, '')
                    name = name.replace(ch, '').upper()
                desciption = desciption.lower()
                name = name.upper()
                desciption = desciption.replace('\n','_^')
                time = timeStamp()
                #createDirs
                for d in snippetDirs:
                    if d != '':
                        snippetpath =  d+name.replace(' ','_')+'_'+time + '/'
                        os.makedirs(snippetpath)
                        open(snippetpath+'#'+name+'  -  '+desciption.decode('utf8', 'ignore')+' @'+userName,'a').close()
                        nuke.nodeCopy(snippetpath+'nodes_sticky.nk')
                        for n in nuke.selectedNodes():
                            if n.Class() == 'StickyNote':
                                n.setSelected(0)
                        nuke.nodeCopy(snippetpath+'nodes.nk')
                nuke.root().end()
                Snippet(mode=0,recursive=1)
    elif mode == 2: #DeleteDirWithSnipet
        p = str(QtGui.QApplication.clipboard().text().encode('utf8', 'ignore'))
        f = '/'.join(p.split('/')[:-1])
        if os.path.isdir(f):
            for s in snippetDirs:
                if os.path.isdir(s):
                    if s in f:
                        a = nuke.ask('Delete Snippet Folder?\n\n'+f)
                        if a==1:
                            import shutil
                            shutil.rmtree(f)
                            Snippet()
