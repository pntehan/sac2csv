import glob
import re
import os
from pandas import DataFrame
import obspy
import numpy as np
import pandas as pd
import time

def get_file(i):
	return glob.glob('../20090630/'+i+'/**.SAC')

def be_csv(dirs,name):
	BHE = DataFrame([])
	BHN = DataFrame([])
	BHZ = DataFrame([])
	for i in dirs:
		fp = obspy.read()
		data = np.array(fp)[0]
		print(data)
		data = data[::6000]
		print(data)
		infor = fp[0].stats
		time_list = get_time(infor, len(data))
		time = list(map(to_time, time_list))
		frame = get_frame(data, time)
		if i[-9:-6] == 'BHE':
			BHE = pd.concat([BHE, frame])
		elif i[-9:-6] == 'BHN':
			BHN = pd.concat([BHN, frame])
		elif i[-9:-6] == 'BHZ':
			BHZ = pd.concat([BHZ, frame])
		print(i,'be done')
	os.mkdir('./CSV/20090630/%s'%name)
	write_csv(BHE, name, 'BHE')
	write_csv(BHN, name, 'BHN')
	write_csv(BHZ, name, 'BHZ')
	print(name,'be done')

def write_csv(x, name, y):
	x = x.set_index('Time')
	x.to_csv('./CSV/20090630/%s/20090630.%s.%s.%s.csv'%(name,name,y,'T'))

def get_frame(data, time):
	y = {'Time':time,'Data':data}
	return DataFrame(y,columns=['Time','Data'])

def to_time(time_list):
	return time.strftime('%Y%m%d%H%M', time.localtime(time_list))

def get_time(infor,l):
	start = infor['starttime']
	start = str(start).replace('T00','')
	startArray = time.strptime(str(start)[:19], '%Y-%m-%d:%H:%M.%S')
	startStamp = int(time.mktime(startArray))
	#2009-08-24T00:20:03.000000Z
	return list(range(int(startStamp),int(startStamp)+int(l*60),60))


def main(file_dirs):
	for i in os.listdir(file_dirs):
		dirs = get_file(i)
		be_csv(dirs,i)

main('./20090630')