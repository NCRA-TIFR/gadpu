import pandas as pd
import numpy as np
import operator
from sys import argv
import os

PATH = "/data2/gmrtarch/cycle20"
dir_list = os.listdir(PATH)

search_string = ".lta"
source_list = []

for directory in dir_list:
	for files in os.listdir(directory):
		for file in files:
			if search_string in files:
				processing(files)				

def extract( file_name ):
        with open(file_name,'r') as f:
                for i,line in enumerate(f,1):
                        if "SCN" in line:
                                return i


def processing(filename):


	dictionary = {}
	lta_file = "lta_file.txt"
	os.system("ltahdr -i"+ filename + ">" +  lta_file)
	

	skipped_rows = extract(lta_file)-1

	header = pd.read_csv('lta_file.txt',skiprows=skipped_rows,delimiter=r"\s+")
	flux = list(set(header["OBJECT"]))
	#print flux

	header['Nrecs'] = header['Nrecs'].astype(float)

	for i in flux :
        	temp = header.loc[header.OBJECT==i,'Nrecs'].values
        	temp = np.mean(temp)
        	dictionary[i]=temp
	#print dictionary

	source = max(dictionary.iteritems(),key=operator.itemgetter(1))[0]

	
	source_list.append(source)


