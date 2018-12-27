import obspy
from glob import glob
from tqdm import *

def test():
	dirs = glob('/media/pntehan/Elements/LDH/地震波形数据前一百小时/SAC/20091128/XSB/*.SAC')
	BHE = obspy.read()
	BHZ = obspy.read()
	BHN = obspy.read()
	for i in tqdm(dirs):
		channel = i.split('.')[-3]
		if channel == 'BHE':
			BHE += obspy.read(i)
		elif channel == 'BHN':
			BHN += obspy.read(i)
		elif channel == 'BHZ':
			BHZ += obspy.read(i)
	read_file(BHE, 'XSB')
	read_file(BHN, 'XSB')
	read_file(BHZ, 'XSB')

def read_file(fp, key):
	fp = fp.merge(method=1)
	print('--------------------------------------------')
	for i in fp:
		print(i.stats)
		if str(i.stats.station) == key:
			tr = i
		print('--------------------------------------------')
	st = tr.resample(1/60)
	data = st.data
	time = getTime(st)
	content = {'Time':time, 'Data':data}
	return DataFrame(content, columns=['Time', 'Data'])

test()

