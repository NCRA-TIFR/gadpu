import pandas as pd
import numpy as np
import operator
import os 
import re
import glob

data_dir = '/data2/gmrtarch/cycle20/'
VALID_LIST = 'parser/filter_healthy/healthy2_file.txt'
valid_observations = open(VALID_LIST, 'r').read().split('\n')[0:-1]
all_observations = os.listdir(data_dir)
ltahdr_error_dir = open('ltahdr_error.txt', 'w')

def INVALID_OBS():
    for DIR_NAME in all_observations:
        current_obslog = glob.glob(data_dir+DIR_NAME+'/'+'*.obslog')
        """
        if current_obslog == []:
            print DIR_NAME
            break
        """
        #Extract substring that contains obslog relative path
        relative_path = re.findall(r'[/][\d]+[.]obslog', current_obslog[0])[0][1:] 
        #Invalid file (not fitting given constraints i.e. < 900 MHz and IF BW != 6,16,32)
        if relative_path not in valid_observations:
            print data_dir+DIR_NAME
        #Valid obslog file with no LTA file in the DIR
        
        if relative_path in valid_observations:
            if glob.glob(data_dir+DIR_NAME+'/'+'*.lta') == []:
                print data_dir+DIR_NAME

def VALID_OBS():
    valid_obs = []
    for DIR_NAME in all_observations:
            current_obslog = glob.glob(data_dir+DIR_NAME+'/'+'*.obslog')
            
            #Extract substring that contains obslog relative path
            relative_path = re.findall(r'[/][\d]+[.]obslog', current_obslog[0])[0][1:] 
                                    
            if relative_path in valid_observations:
                if glob.glob(data_dir+DIR_NAME+'/'+'*.lta') != []:
                    valid_obs.append(data_dir+DIR_NAME)
    return valid_obs

def extract( file_name ):
    with open(file_name) as f:
        for i,line in enumerate(f,1):
            if "SCN" in line:
                return i

def main(lta_name):
    calibrator_list = ['3C48', '3C147', '3C286']
    os.system('ltahdr -i'+ lta_name + '> lta_file.txt')
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
                os.system('rm lta_file.txt')
                return source
    except:
        pass 

valid_observations = VALID_OBS()

for DIR in valid_observations:
    all_lta_files = glob.glob(DIR + '/*.lta.*')
    for LTA_FILE in all_lta_files:
        try:
            print(LTA_FILE)
            print main(LTA_FILE)
        except:
            #Log the error directory to a file
            ltahdr_error_dir.write(DIR+ '/' + LTA_FILE + '\n')
