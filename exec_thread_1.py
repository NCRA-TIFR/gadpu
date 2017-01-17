#import spam
import filter_lta

#VALID_FILES = filter_lta.VALID_OBS().split('\n') 
print filter_lta.VALID_OBS()

#def extract_basename():

def main():
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
