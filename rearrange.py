from pandas import DataFrame
import pandas as pd
import os
import numpy as np
from glob import glob
import shutil
from tqdm import *

def get_name(file):
	dirs = glob('G:/LDH/SAC数据/震时数据/%s/*/*.SAC'%file)
	name = []
	for i in dirs:
		j = i.split('/')[-1]
		name.append(j.split('.')[7])
	return np.unique(name)

def make_dir(file, name):
	for i in name:
		path = 'G:/LDH/SAC数据/震时数据/'+file+'/'+i
		if os.path.exists(path):
			pass
		else:
			os.mkdir(path)

def move_file(file):
	dirs = glob('G:/LDH/SAC数据/震时数据/%s/*/*.SAC'%file)
	for i in tqdm(dirs):
		j = i.split('/')[-1]
		name = i.split('/')[-2]
		station = j.split('.')[7]
		new = 'G:/LDH/SAC数据/震时数据/'+file+'/'+station+'/'
		shutil.move(i, new)

def removedir(path):
	dirs = os.listdir('G:/LDH/SAC数据/震时数据/'+path)
	for i in dirs:
		new_path='G:/LDH/SAC数据/震时数据/'+path+'/'+i
		if not os.listdir(new_path):
			os.rmdir(new_path)

def arrange(path):
	name = get_name(path)
	make_dir(path, name)
	move_file(path)
	removedir(path)
	print('------文件分配完毕------')
