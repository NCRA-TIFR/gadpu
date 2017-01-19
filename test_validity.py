import pandas as pd
import numpy as np
import operator
import os 
import re
import glob
import trace
data_dir = '/data2/gmrtarch/cycle20/'
VALID_LIST = 'parser/filter_healthy/healthy2_file.txt'
valid_observations = open(VALID_LIST, 'r').read().split('\n')[0:-1]
all_observations = os.listdir(data_dir)
ltahdr_error_dir = open('ltahdr_error.txt', 'wa')
lta_success_file = open('ltahdr_success.txt', 'wa')

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

def NUM_LTA():
    valid_obs = []
    all_lta_files = []
    for DIR_NAME in all_observations:
        current_obslog = glob.glob(data_dir+DIR_NAME+'/'+'*.obslog')

        #Extract substring that contains obslog relative path
        relative_path = re.findall(r'[/][\d]+[.]obslog', current_obslog[0])[0][1:] 

        if relative_path in valid_observations:
            current_dir_lta_files = glob.glob(data_dir+DIR_NAME+'/'+'*.lta*') 
            #print current_dir_lta_files
            if(current_dir_lta_files != []):
                valid_obs.append(data_dir+DIR_NAME)
                all_lta_files.append(current_dir_lta_files)
    return len([i for j in all_lta_files for i in j])


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

        #Sort the list of targets according to the number of recordings
        list_of_targets = sorted(dictionary.iteritems(),key=operator.itemgetter(1), reverse=True)
        for i in list_of_targets:
            if i[0] in calibrator_list:
                continue
            else:
                os.system('rm lta_file.txt')
                return i[0]
        #Return this value if entire list of targets is populated with calibrators
        return -1
    except:
        pass 
valid_observations = VALID_OBS()
lta_file_count = 0
for DIR in valid_observations:
    all_lta_files = glob.glob(DIR + '/*.lta*')
    for LTA_FILE in all_lta_files:
        try:
            output = main(LTA_FILE)
            #Check if valid target name is found
            if output != -1:
                lta_success_file.write(LTA_FILE + '\n' + output + '\n')
                lta_file_count += 1
                print(LTA_FILE)
                print output
                print lta_file_count
            else:
                continue
                ltahdr_error_dir.write(DIR+ '/' + LTA_FILE + '\n') 
                lta_file_count += 1
        except:
            #Log the error directory to a file
            ltahdr_error_dir.write(DIR+ '/' + LTA_FILE + '\n')
            lta_file_count += 1
 
