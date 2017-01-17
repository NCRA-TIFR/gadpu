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
def main(lta_name):
    os.system('ltahdr -i'+ lta_name + '> lta_file.txt')
    dictionary = {}
    #lta_file = str(argv[1])
    skipped_rows = extract('lta_file.txt')-1

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
    return source
