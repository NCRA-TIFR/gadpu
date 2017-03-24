import re
import os
import glob
import spam
data_dir = '/data2/archit/kaka1/partialcycle20/'
os.chdir(data_dir)
all_observations = os.listdir(data_dir)
for DIR_NAME in all_observations:
	os.chdir(data_dir+DIR_NAME+'/')
	lta_files = glob.glob('*.lta')
	uvfits_files = glob.glob('*.UVFITS')
	flag_files = glob.glob('*.FLAGS*')
	for i in range(1,len(uvfits_files)):
		spam.pre_calibrate_targets(uvfits_files[i])

