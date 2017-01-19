import pandas as pd
import numpy as np
import operator
from sys import argv
import os 

def extract( file_name ):
    with open(file_name) as f:
        for i,line in enumerate(f,1):
            if "SCN" in line:
                return i

def main():
    lta_file = str(argv[1])
    calibrator_list = ['3C48', '3C147', '3C286']
    os.system('ltahdr -i'+ lta_file + '> lta_file.txt')
    dictionary = {}
    try:
        skipped_rows = extract('lta_file.txt')-1

        header = pd.read_csv('lta_file.txt',skiprows=skipped_rows,delimiter=r"\s+")
        flux = list(set(header["OBJECT"]))
        #print flux

        header['Nrecs'] = header['Nrecs'].astype(float)

        for i in flux :
            temp = header.loc[header.OBJECT==i,'Nrecs'].values
            temp = np.mean(temp)
            dictionary[i]=temp
        print dictionary
    
        #Sort the list of targets according to the number of recordings
        list_of_targets = [ i for i,j in sorted(dictionary.iteritems(),key=operator.itemgetter(1), reverse=True)]
        source = max(list_of_targets)
        for i in len(flux): 
            if source in calibrator_list:
                continue
            else:
                return source
    except:
        pass 

print main()
