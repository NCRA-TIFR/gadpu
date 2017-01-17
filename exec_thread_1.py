#import spam
import filter_lta
import os
#List of all directories containing valid observations 
VALID_FILES = filter_lta.VALID_OBS()

#List of all directories for current threads to process
THREAD_FILES = VALID_FILES[0:len(VALID_FILES):5]
print 'Executing this thread'
os.system('pwd')

def main():

    for i in THREAD_FILES:
        LTA_FILES = os.chdir(i)
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
