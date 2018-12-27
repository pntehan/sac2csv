from obspy import UTCDateTime
import pandas as pd
import os
from glob import *
from tqdm import *
import obspy
from pandas import DataFrame

def getDirs(Station):
	#得到每个台站的所有SAC数据文件
	dirs = glob('%s/*.SAC'%Station)
	return dirs

def sac2csv(DataName):
	#将事件内所有SAC文件转化为CSV文件格式，并且降采样到一分钟
	if os.path.exists('../CSV/震时数据/%s'%DataName):
		pass
	else:
		os.mkdir('../CSV/震时数据/%s'%DataName)
	dirs = os.listdir('G:/LDH/SAC数据/震时数据/'+DataName)
	print('>>>>>>>>>>>>正在处理%s事件<<<<<<<<<<<<'%DataName)
	for i in dirs:
		print('>>>>>>>>>>>>正在处理%s台站<<<<<<<<<<<<'%i)
		files = getDirs('G:/LDH/SAC数据/震时数据/'+DataName+'/'+i)
		transfile(files, DataName, i)
		print('>>>>>>>>>>>>台站%s已完成<<<<<<<<<<<<'%i)
	print('>>>>>>>>>>>>%s事件已完成<<<<<<<<<<<<'%DataName)

def transfile(dirs, DataName, station):
	#进行SAC to CSV的主要功能函数
	if os.path.exists('../CSV/震时数据/%s/%s'%(DataName, station)):
		pass
	else:
		os.mkdir('../CSV/震时数据/%s/%s'%(DataName, station))
	LHE = DataFrame()
	LHZ = DataFrame()
	LHN = DataFrame()
	for i in tqdm(dirs):
		channel = i.split('.')[-3]
		y = read_file(i)
		if channel == 'LHE':
			LHE = pd.concat([LHE, y], axis=0, ignore_index=True)
		elif channel == 'LHN':
			LHN = pd.concat([LHN, y], axis=0, ignore_index=True)
		elif channel == 'LHZ':
			LHZ = pd.concat([LHZ, y], axis=0, ignore_index=True)
	writeFile(LHZ, DataName, 'LHZ', station)
	writeFile(LHN, DataName, 'LHN', station)
	writeFile(LHE, DataName, 'LHE', station)

def writeFile(result, DataName, channel, station):
	#将数据集写入csv文件中
	path = '../CSV/震时数据/'+DataName+'/'+station+'/'+DataName+'.'+station+'.'+channel+'.60s.csv'
	try:	
		result = result.set_index('Time')
	except:
		pass
	result.to_csv(path)

def read_file(fp):
	#读取SAC文件的内容
	tr = obspy.read(fp)[0]
	st = tr.resample(1/60)
	data = st.data
	time = getTime(st)
	content = {'Time':time, 'Data':data}
	return DataFrame(content, columns=['Time', 'Data'])

def getTime(fp):
	#得到数据的时间序列
	start = fp.stats.starttime.timestamp * 100
	npts = fp.stats.npts
	delta = fp.stats.delta * 100
	time = list(range(int(start), int(start)+npts*int(delta), int(delta)))
	return list(map(timestamp2time, time))

def timestamp2time(timestamp):
	#将时间戳转换为格式要求的时间格式
	utctime = str(UTCDateTime(timestamp/100))
	time = utctime[:4] + utctime[5:7] + utctime[8:10] + utctime[11:13] + utctime[14:16] + utctime[17:19] + utctime[20:22]
	return int(time)

#sac2csv('20090630')
