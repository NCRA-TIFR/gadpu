import spam
import filter_lta 
import time
import os
import glob
import trace
#import test_validity
spam.set_aips_userid(13)
#List of all directories containing valid observations 
VALID_FILES = filter_lta.VALID_OBS()
#List of all directories for current threads to process
THREAD_FILES = VALID_FILES[2:len(VALID_FILES):5]
print 'Executing this thread'
lta_to_uvfits_log = open('lta_to_uvfits_log.txt', 'w+')
precalibrator_log = open('precalibrator_log.txt', 'w+')
os.system('pwd')

def lta_to_uvfits():
    os.chdir('fits/')
    lta_files = glob.glob('*.lta*')
    #flag_files = glob.glob('*.FLAGS*')
    for i in range(len(lta_files)):
        lta_file_name = lta_files[i]
        uvfits_file_name = lta_file_name +'.UVFITS'
        try:
            spam.convert_lta_to_uvfits( lta_file_name, uvfits_file_name )
            #In case of success in conversion remove the LTA file
            os.system('rm ' + lta_file_name)
        except RuntimeError:
            #Write to log file
            lta_to_uvfits_log.write(lta_file_name)
            #Remove the UVFITS file 
            os.system('rm *.UVFITS')
            continue
    os.chdir('../')
    return lta_files 

def precalibrator():
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

    and convert to string consisting of whitespace seperated strings (to write to file)

    i.e. 3C286 name_of_lta_file

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
    #Copy all LTA files in valid obs dir to fits directory for processing
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
