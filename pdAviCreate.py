#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os, sys, subprocess
import pyperclip
import time


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


if __name__ == '__main__':
	#print('#init MAIN -------------------')
	droped = None
	if getattr( sys, 'frozen', False ) :
	# running in a bundle
		filepy = sys.executable
		try:
			droped = sys.argv[1]
		except:
			u = input("\n\n\nDrop To App Launcher One Folder with TIFF sequence begining at 0001 for generate PRORES mov")
	else :
	# running live
		filepy = sys.argv[0]
		try:
			droped = sys.argv[1]
		except:
			u = input("\n\n\nDrop To App Launcher One Folder with TIFF sequence begining at 0001 generate PRORES mov")
	if droped != None:
		fpss = filepy.split('.')[0][-2:]

		dirpy = os.path.abspath(droped)
		parfolder = os.path.dirname(dirpy)
		#if '\\' in droped:
		#	dirpy = droped.replace('\\','/')

		print('\n#From Folder:  ',dirpy)
		df = os.listdir(dirpy)
		firstfile = None
		last = len(df)
		first = 1
		for i in sorted(df):
			if os.path.isfile(dirpy+'/'+i):
				if 'tif' in i:
					firstfile = i
					break
		print('\n#FirstFile:  ',firstfile)
		res_x = 1998
		res_y = 1080
		if firstfile != None:
			if '0001' in firstfile:
				#correct
				firstfile = firstfile.replace('0001', '%04d')
				pathfirstfile = dirpy+'/'+firstfile
				meta_txt = 'D:/wxBrowser/bin_portables/mrViewer-v5.3.1-Windows-64/bin/meta_to_avi.txt'
				ffmbc = 'D:/wxBrowser/bin_portables/mrViewer-v5.3.1-Windows-64/bin/ffmpeg.exe'
				pd_programm = r'"\\dataServer\Project\lib\soft\Pdplayer64_1.07\pdplayer64.exe"'
				#pd_programm = r'"E:\\Work\\sequences\\Pdplayer64_1.07\\pdplayer64.exe"'
				avifull_path = dirpy+'.avi'
				pdplaercmd = pd_programm + r' --timeline='+ str(last+1) + r' --wa_begin='+str(first)+r' --wa_end='+ str(last+1) + r' --time=33 --back_color=0,0,0 --safe_area=none --mask_type=none --mask_size='+ str(res_x) + r','+ str(res_y) + r' --fps='+fpss+r' --zoom=100 --pan=0,0 --frame_base=0 --global_aspect=1 --apply_transforms_to_mask=0 --stereo_view=left "'+dirpy+'\\'+firstfile+r'" --name="None" --begin=1 --alpha=ignore --color_space=default --disable_caching=0 --save_mask_as_sequence='+avifull_path+', --exit'

				if os.path.isfile(avifull_path):
					os.remove(avifull_path)
				
				print(pdplaercmd,'\n')
				#os.system(pdplaercmd)
				p = subprocess.Popen(pdplaercmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
				dots = '.'
				while p.poll() is None:
					print('Progress: '+dots , end='\r')
					time.sleep(1)
					dots += '.'
				#p.wait()
				pyperclip.copy(avifull_path)
				print(avifull_path)
				print(' Avi generated ... Path Copied to Clipboard  autoclose 3 sec.....')
				time.sleep(3)
			else:
				u = input("\n\n\nSequence not From 0001 or padding not correct")

#9662 kb


#\\cacheserver\Project\lib\HOU\mapyPipe\programs\mrViewer-v5.3.1-Windows-64\bin\ffmbc.exe
#//cacheserver/Project/lib/HOU/mapyPipe/programs/mrViewer-v5.3.1-Windows-64/bin/mrViewer.exe

#ffmbc.exe -i E:\Work\sequences\OUT\ep32sc06_%04d.tif -r 23.98  -vcodec prores -profile hq -pix_fmt yuv444p10le E:\Work\sequences\teset_prores4.mov


#\\dataserver\Project\Tsarevny\output\seria031\AVI\sr031ep04\sr031ep04sc10.avi

#"E:\\Work\\sequences\\Pdplayer64_1.07\\pdplayer64.exe" --timeline=163 --wa_begin=1 --wa_end=163 --time=33 --back_color=0,0,0 --safe_area=none --mask_type=none --mask_size=2048,858 --fps=24 --zoom=100 --pan=0,0 --frame_base=0 --global_aspect=1 --apply_transforms_to_mask=0 --stereo_view=left "E:\\Work\\sequences\\OUT\\ep32sc06_%04d.tif" --name="None" --begin=1 --alpha=ignore --color_space=default --disable_caching=0 --save_mask_as_sequence="E:\\Work\\sequences\\OUT.avi", --exit
