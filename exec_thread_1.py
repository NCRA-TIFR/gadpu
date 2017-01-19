import spam
import filter_lta
import os
import glob
spam.set_aips_userid(11)
#List of all directories containing valid observations 
VALID_FILES = filter_lta.VALID_OBS()

#List of all directories for current threads to process
THREAD_FILES = VALID_FILES[0:len(VALID_FILES):5]
print 'Executing this thread'
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
        except RuntimeError:
            #Write to log file
            lta_to_uvfits_log.write()
            continue
    os.chdir('../')
    return lta_files 

def precalibrater():
    uvfits_files = glob.glob('fits/*.UVFITS')
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
            precalibrate_log.write()
            continue
    os.chdir('../')

def main():     

    #Copy all LTA files in valid obs dir to fits directory for processing
        os.system('mv ' + THREAD_FILES + '/* ' + 'fits/')
        lta_to_uvfits()
        precalibrater()
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
