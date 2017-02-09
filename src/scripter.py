import filter_lta
import os, re
import glob
import sys


#List of all directories containing valid observations 
VALID_FILES = filter_lta.VALID_OBS()
#List of all directories for current threads to process
THREAD_FILES = VALID_FILES



#source = '/data2/archit/data/'
dest = '/data2/archit/datum/'
#directories = os.listdir(source)
for directory in THREAD_FILES:
	os.chdir(directory)
	files = glob.glob('*.lta*')
	for file in files:
		dir_name = file.replace('.','_')
		os.system('mkdir ' + dest + dir_name)
		os.system('mv ' + file + ' ' + dest + dir_name)
