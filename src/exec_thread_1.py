import spam
import filter_lta 
import time
import os
import glob
import trace
import test_validity

#Set AIPS user id seperately for each thread
spam.set_aips_userid(11)

"""
Function for list of all directories containing valid observations
INPUT : Path name of the directory with all lta files - /data2/gmrtarch/cycle20
OUTPUT : Path of directory with valid LTA files - /data2/gmrtarch/cycle20/11DT013_25MAY11

WORKING :
valid_observations is the list of all valid obslog extracted from healty2_file.txt
all_observations is the list of all directories in the particular directory(cycle20)
current_obslog is the list of all obslog in the directory(cycle20)
Compares current obslog and valid_observations and stores the directory path in valid_obs
Returns valid_obs
VALID_FILES = valid_obs
""" 

VALID_FILES = filter_lta.VALID_OBS()

#Assigning directories thread wise to each thread.
THREAD_FILES = VALID_FILES[0:len(VALID_FILES):5]

print 'Executing this thread'

#Log files for storing error files for lta_to_uvfits and precalibrator
lta_to_uvfits_log = open('lta_to_uvfits_log.txt', 'w+')
precalibrator_log = open('precalibrator_log.txt', 'w+')
#os.system('pwd')


def lta_to_uvfits():
    """ 
Function for converting lta to lta.UVFITS
INPUT : lta files
OUTPUT : lta.UVFITS files
FLOW : All the files in the directories assigned to a thread are moved into fits/
Each thread has its seperate fits directory
gadpu -> THREADi -> fits -> All relevant files
1.Changes Directory to fits/
2.lta_files stores all lta_files present 
3.Converts to lta.UVFITS
4.If fails , write name of lta file to log and delete incomplete lta.UVFITS 
5.Change directory to THREADi

"""
    os.chdir('fits/')
    lta_files = glob.glob('*.lta*')
    #flag_files = glob.glob('*.FLAGS*')
    for i in range(len(lta_files)):
        lta_file_name = lta_files[i]
        uvfits_file_name = lta_file_name +'.UVFITS'
        try:
            spam.convert_lta_to_uvfits( lta_file_name, uvfits_file_name )
            #In case of success in conversion remove the LTA file
#           os.system('rm ' + lta_file_name)
        except RuntimeError:
            #Write to log file
            lta_to_uvfits_log.write(lta_file_name)
            #Remove the UVFITS file 
            os.system('rm *.UVFITS')
            continue
    os.chdir('../')
    return lta_files 

def precalibrator():
    """
Function for converting lta.UVFITS to UVFITS(Target and Callibrator)
INPUT : lta.UVFITS
OUTPUT : .UVFITS
FLOW : fits/ directory has all files including .lta.UVFITS. Run pre-calibrate
targets on all the available .lta.UVFITS files
1. Change directory to /fits
2. uvfits_files is list of all UVFITS
3. Precalibrate uvfits_files
4. If fails , write in log name of uv_fits files
5. Change directory to THREADi

"""
    os.chdir('fits/')
    uvfits_files = glob.glob('*.UVFITS')
    print uvfits_files
    #flag_files = glob.glob('*.FLAGS*')
    for i in range(0,len(uvfits_files)):
        #if source_name in uvfits_files[i]:
        #print source_name
        os.system('pwd')
        print('\n\n\nPrinting user ID AIPS\n\n\n')
        print spam.get_aips_userid()
        try:
            spam.pre_calibrate_targets(uvfits_files[i])
        except RuntimeError:
            for uvfits_file in uvfits_files:
                precalibrator_log.write(uvfits_file)
            continue
    os.chdir('../')


def write_source_list(source_list):
    """
    Parse through the input source list 

    i.e. source_list = [('3C286', 'name_of_lta_file')]

    and convert to string consisting of a whitespace seperated string (to write to file)

    i.e. "3C286 name_of_lta_file"

    Inputs:

    - source_list : A list of sources and LTA files that they have been extracted from
                    that have been extracted using the validity function which runs the
                    LTAHDR utility.
    """
    write_string = ""
    for SOURCES in source_list:
        for i in SOURCES:
            write_string += i + '\t'
        write_string += '\n'
    return write_string

def main():     
    #Copy all files in valid obs dir to fits directory for processing
    for CURRENT_DIR in THREAD_FILES:
        #source_name_file = open(CURRENT_DIR+'/'+'source_name_file.txt', 'w')
        if CURRENT_DIR != '':
            os.system('mv ' + CURRENT_DIR + '/* ' + 'fits/')
            lta_to_uvfits()
            #Write the list of sources to the current directory
            #source_list = test_validity.test_validity()
            #write_string = write_source_list(source_list)
            #source_name_file.write(write_string)
            precalibrator()  
            os.system('mv fits/* ' + CURRENT_DIR)
        """
        #Convert the LTA file to the UVFITS format
        #Generates UVFITS file with same basename as LTA file 
        spam.convert_lta_to_uvfits('Name of the file')

        #Take generated UVFITS file as input and precalibrate targets
        #Generates files (RRLL with the name of the source (can be obtained using ltahdr)
        spam.precalibrate_targets('Name of UVFITS output file')

        #Take the generated RRLL UVFITS file and process to generate the image
        #Generates final image <source name>.SP2B.PBCOR.FITS
        #Also generates log file spam_<source name>_<start date>_start_time>.log in
        #datfil dir
        spam.process_target()
        """
main()

