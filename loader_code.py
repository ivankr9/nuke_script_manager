import os
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

def deletePadding_seq(f,n=4):
    newname = ''
    number = ''
    i = 0
    for char in f[::-1]:
        if char.isdigit():
            number += char
            i+=1
        if i == n:
            break
    number = number[::-1]
    return f.replace(number,'')

def LoadSequenceFromDir(directory,endfile):
    readers = []
    with nuke.root().begin():
        files = os.listdir(directory)
        count = 1
        counts = []
        sequences = []
        WithoutDigitName = ''
        seqfiles = []
        for f in sorted(files):
            if endfile == f[-3:]:
                #WithoutDigitName = ''.join([i for i in f if not i.isdigit()])
                WithoutDigitName = deletePadding_seq(f)
                if WithoutDigitName not in  sequences:
                    print WithoutDigitName
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
#node = nuke.toNode('Load_sequences_from_dir')
node = nuke.thisNode()
NODENAME = node.name()
root = nuke.Root()
root.begin()

directory = node.knob('set_folder_with_exr').value()
xp = node.xpos()
yp = node.ypos()
endfile='exr'
if directory[-3:] == endfile:
    directory = '/'.join(directory.split('/')[:-1])
node.knob('set_folder_with_exr').setValue(directory)
readers = LoadSequenceFromDir(directory,endfile)
ps = 1
exl = ['ryptomatt','custom','geometry']
read_final = None
for r in readers:
    file = r.knob('file').value()
    filename = file.split('/')[-1]
    expr = "[value "+NODENAME+".set_folder_with_exr]"
    new_file = expr + '/' + filename
    print new_file
    r.knob('file').setValue(new_file)
    if exl[0] not in file and exl[1] not in file and exl[2] not in file:
        read_final = r
    yp+=80
    r.setXYpos(xp,yp)
    r.knob('postage_stamp').setValue(0)
    r.setSelected(1)
g = nuke.createNode("Merge2")
g["operation"].setValue("plus")
g["metainput"].setValue("All")
g["also_merge"].setValue("all")
g["Achannels"].setValue("none")
g.setXYpos(xp+100,yp+100)
g.setName('ALL_PASSES')
n = nuke.createNode("PostageStamp")
n.connectInput(0,read_final)
n.setXYpos(xp-100,yp+100)
n.setName('Final')
