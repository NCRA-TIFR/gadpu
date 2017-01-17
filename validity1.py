import pandas as pd
import numpy as np
import operator
from sys import argv

def extract( file_name ):
        with open(file_name) as f:
                for i,line in enumerate(f,1):
                        if "SCN" in line:
                                return i

dictionary = {}
lta_file = str(argv[1])
skipped_rows = extract(lta_file)-1

header = pd.read_csv(lta_file,skiprows=skipped_rows,delimiter=r"\s+")
flux = list(set(header["OBJECT"]))
print flux

header['Nrecs'] = header['Nrecs'].astype(float)

for i in flux :
        temp = header.loc[header.OBJECT==i,'Nrecs'].values
        temp = np.mean(temp)
        dictionary[i]=temp
print dictionary

source = max(dictionary.iteritems(),key=operator.itemgetter(1))[0]
print source


