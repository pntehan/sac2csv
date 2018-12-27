from tqdm import *
import os
from glob import *
from pandas import DataFrame
import pandas as pd
import numpy as np

def get_path(name):
	path = '../CSV/震时数据/'+name+'/'
	dirs = os.listdir(path)
	return dirs

def merge_data(i):
	if os.path.exists('G:/LDH/CSV数据/震时数据/'+i):
		pass
	else:
		os.mkdir('G:/LDH/CSV数据/震时数据/'+i)
	dirs = get_path(i)
	LHE = DataFrame([])
	LHZ = DataFrame([])
	LHN = DataFrame([])
	for j in tqdm(dirs):
		path = glob('../CSV/震时数据/%s/%s/*.csv'%(i,j))
		for k in path:
			f = open(k)
			df = pd.read_csv(f)
			df.rename(columns={'Data': j}, inplace=True)
			if k.split('.')[-3] == 'LHE':
				try:
					df = df.set_index('Time')
					LHE = pd.concat([LHE, df], axis=1)
				except:
					print(j)
			if k.split('.')[-3] == 'LHN':
				try:
					df = df.set_index('Time')
					LHN = pd.concat([LHN, df], axis=1)
				except:
					print(j)
			if k.split('.')[-3] == 'LHZ':
				try:
					df = df.set_index('Time')
					LHZ = pd.concat([LHN, df], axis=1)
				except:
					print(j)
	LHE.to_csv('G:/LDH/CSV数据/震时数据/%s/%s.csv'%(i, i+'.LHE'))
	LHN.to_csv('G:/LDH/CSV数据/震时数据/%s/%s.csv'%(i, i+'.LHN'))
	LHZ.to_csv('G:/LDH/CSV数据/震时数据/%s/%s.csv'%(i, i+'.LHZ'))
	print('------',i,'拼装完成------')

def merge(path):
	merge_data(path)
