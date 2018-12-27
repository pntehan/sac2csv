from merge_data import merge
from sac2csv import *
from rearrange import arrange
import sys

def main(name):
	arrange(name)
	sac2csv(name)
	merge(name)

if __name__ == '__main__':
	main(str(sys.argv[1]))
