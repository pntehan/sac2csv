import os

dirs = os.listdir('/media/pntehan/Elements/LDH/SAC数据/非震时数据')
for i in dirs[:]:
	os.system('python /media/pntehan/Elements/LDH/SAC2CSV代码/sac2csv/main.py '+i)
