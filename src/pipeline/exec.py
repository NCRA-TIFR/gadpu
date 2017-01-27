import spam
import filter_lta 
import time
import os
import glob
import trace
import test_validity
pid = os.getpid()
os.system('taskset -cp 0 ' + str(pid))
spam.set_aips_userid(11)
#List of all directories containing valid observations 
VALID_FILES = filter_lta.VALID_OBS()
#List of all directories for current threads to process
THREAD_FILES = VALID_FILES
print 'Executing this thread'
lta_to_uvfits_log = open('lta_to_uvfits_log.txt', 'w+')
precalibrator_log = open('precalibrator_log.txt', 'w+')
directory_log = open('directory_log.txt','w+')
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
            #os.system('rm ' + lta_file_name)
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
    final_list = []
    for i in range(0,len(uvfits_files)):
        #if source_name in uvfits_files[i]:
        #print source_name
        os.system('pwd')
        print('\n\n\nPrinting user ID AIPS\n\n\n')
        print spam.get_aips_userid()
	
        try:
            old_files = os.listdir('./')
      	    spam.pre_calibrate_targets(uvfits_files[i])
	    new_files = os.listdir('./')
	    added_files = [z for z in new_files if z not in old_files]
	    mid_list = [uvfits_files[i]]
	    for j in added_files:	
	    	mid_list.append(j)
        except RuntimeError:
            for uvfits_file in uvfits_files:
                precalibrator_log.write(uvfits_file)
            continue
	final_list.append(mid_list)
    os.chdir('../')
    return final_list

        
def main():     
    #Copy all LTA files in valid obs dir to fits directory for processing
    
    for CURRENT_DIR in THREAD_FILES:
        if CURRENT_DIR != '':
            os.system('mv ' + CURRENT_DIR + '/* ' + 'fits/')
            #Write the list of sources to the current directory
            os.chdir('fits/')
            source_with_lta = test_validity.test_validity()                   #[[source1,lta_file1],[source2,lta_file2]]
            os.chdir('../')
	    lta_to_uvfits()            
            uvfits_with_newuvfits = precalibrator()    #[[uvfits1,newuvfits1_1,newuvfits1_2,..],[uvfits2,newuvfits2_1,newuvfits2_2,..]]        
	    print "Preprocessing " + str(source_with_lta)
	    print "Preprocessing "+ str(uvfits_with_newuvfits)
	    os.chdir('fits/')
	    source_lta = open('source_lta.txt','w+')
	    uvfits_newuvfits = open('uvfits_newuvfits.txt','w+')
	    string = ""
	    for i in source_with_lta:
	    	for j in i:
	    		string += j + ' '
	    	string += '\n'
	    source_lta.write(string)
	    string = ""
	    for i in uvfits_with_newuvfits:
	    	for j in i:
	    		string += j + ' '
	    	string += '\n'
	    uvfits_newuvfits.write(string)
	    os.chdir('../')
            os.system('mv fits/* ' + CURRENT_DIR)
	    directory_log.write(CURRENT_DIR + '\n')
    
#process target files
def post():
    for CURRENT_DIR in THREAD_FILES:
    	if CURRENT_DIR != '':
    		os.system('mv ' + CURRENT_DIR + '/* ' + 'fits/')
    		os.chdir('fits/')
    		new_source_lta = open('source_lta.txt','r').read().split('\n')
	    	new_uvfits_newuvfits = open('uvfits_newuvfits.txt','r').read().split('\n')
		a = os.listdir('./')
		print a		
		print "From file " + str(new_source_lta)
		print "From file " + str(new_uvfits_newuvfits)	   	
		source_with_lta = []
	   	uvfits_with_newuvfits = []
	   	for i in range(len(new_source_lta)-1):
	   		source_with_lta.append(new_source_lta[i].split())
	   	for i in range(len(new_uvfits_newuvfits)-1):
	   		uvfits_with_newuvfits.append(new_uvfits_newuvfits[i].split())
	   	print "Main processing " + str(source_with_lta)
	   	print "Main processing " + str(uvfits_with_newuvfits)
    		for source,lta in source_with_lta:
		    	for i in range(len(uvfits_with_newuvfits)):
		    		if lta in uvfits_with_newuvfits[i][0]:
		    			for j in range(1,len(uvfits_with_newuvfits[i])):
		    				if source in uvfits_with_newuvfits[i][j]:
		    					try:	
		    						spam.process_target(uvfits_with_newuvfits[i][j])
		    					except RuntimeError:
		    						break
            	os.chdir('../')
	    
	    	os.system('mv fits/* ' + CURRENT_DIR)
main()
post()
print "Done"

