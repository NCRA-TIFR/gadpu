import re
import os
import glob
import spam
data_dir = '/data2/archit/kaka1/partialcycle20/'   #directory containing cycle data
os.chdir(data_dir)
all_observations = os.listdir(data_dir)
for DIR_NAME in all_observations:
	os.chdir(data_dir+DIR_NAME+'/')
	lta_files = glob.glob('*.lta*')
	flag_files = glob.glob('*.FLAGS*')
	for i in range(len(lta_files)):
		lta_file_name = lta_files[i]
		uvfits_file_name = lta_files[i]+'.UVFITS'
		spam.convert_lta_to_uvfits( lta_file_name, uvfits_file_name )
		
	
	
