import pandas as pd
import numpy as np
import operator,os

def extract( file_name ):
    with open(file_name) as f:
        for i,line in enumerate(f,1):
            if "SCN" in line:
                return i

def main(lta_file):
    os.system('ltahdr -i ' + lta_file + '>  lta_header')
    dictionary = {}
    skipped_rows = extract(lta_header)-1

    header = pd.read_csv(lta_header,skiprows=skipped_rows,delimiter=r"\s+")
    flux = list(set(header["OBJECT"]))


    header['Nrecs'] = header['Nrecs'].astype(float)

    for i in flux :
        temp = header.loc[header.OBJECT==i,'Nrecs'].values
        temp = np.mean(temp)
        dictionary[i]=temp

    source = max(dictionary.iteritems(),key=operator.itemgetter(1))[0]
    return source
