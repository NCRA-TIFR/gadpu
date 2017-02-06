import spam
import filter_lta 
import time
import os, re
import glob
import trace
import test_validity
import sys
import time
#Assign core to the process
pid = os.getpid()
os.system('taskset -cp 0 ' + str(pid))
spam.set_aips_userid(11)
#List of all directories containing valid observations 
VALID_FILES = filter_lta.VALID_OBS()
#List of all directories for current threads to process
THREAD_FILES = VALID_FILES
print 'Executing this thread'

failed_files = open('datfil/failed_files.log','w+')
succeeded_files = open('datfil/succeeded_files.log','w+')
succeeded_files.write('Successful final processing\n\n')
succeeded_files.flush()
failed_files.write('Failed files\n\n')
failed_files.flush()
directory_log = open('directory_log.txt','w+')
os.system('pwd')

def lta_to_uvfits(CURRENT_DIR):
    os.chdir('fits/')
    original_stdout = sys.stdout
    original_stderr = sys.stderr
    l2u_precal_log = open('l2u_precal.log','w+')
    sys.stdout = l2u_precal_log
    sys.stderr = l2u_precal_log
    lta_files = glob.glob('*.lta*')
    #flag_files = glob.glob('*.FLAGS*')
    lta_to_uvfits_log = open('lta_to_uvfits_log.txt', 'w+')
    for i in range(len(lta_files)):
        lta_file_name = lta_files[i]
        uvfits_file_name = lta_file_name +'.UVFITS'        
	try:
            spam.convert_lta_to_uvfits( lta_file_name, uvfits_file_name )
	    lta_to_uvfits_log.write("Successful conversion of " + str(lta_file_name) + " to " + str(lta_file_name+'.UVFITS')+'\n')
	    lta_to_uvfits_log.flush()
	    print "*****LTA to UVFITS conversion DONE*****"
            #In case of success in conversion remove the LTA file
            #os.system('rm ' + lta_file_name)
        except RuntimeError,r:
            #Write to log file
            lta_to_uvfits_log.write("Error in conversion of " + str(lta_file_name) + " to " + str(lta_file_name+'.UVFITS')+'\n' + str(r) +'\n********************************************************\n')
            lta_to_uvfits_log.flush()
            failed_files.write(CURRENT_DIR + '/' +str(lta_file_name)+" : LTA to UVFITS conversion error\n")
	    failed_files.flush()
	    print "*****LTA to UVFITS conversion STOPPED*****"
	    print r 
            #Remove the UVFITS file 
            #os.system('rm ' + str(lta_file_name)+ '.UVFITS')
            continue
    sys.stdout = original_stdout
    sys.stderr = original_stderr
    os.chdir('../')
    return lta_files 

def precalibrator(CURRENT_DIR):
    os.chdir('fits/')
    original_stdout = sys.stdout
    original_stderr = sys.stderr
    l2u_precal_log = open('l2u_precal.log','a')
    sys.stdout = l2u_precal_log
    sys.stderr = l2u_precal_log
    uvfits_files = glob.glob('*.UVFITS')
    print uvfits_files
    #flag_files = glob.glob('*.FLAGS*')
    final_list = []
    precalibrator_log = open('precalibrator_log.txt', 'w+')
    for i in range(0,len(uvfits_files)):
        #if source_name in uvfits_files[i]:
        #print source_name
        os.system('pwd')
        print('\n\n\nPrinting user ID AIPS\n\n\n')
        print spam.get_aips_userid()
        try:
	    #To get a list of newly added files after precalibration
            old_files = os.listdir('./') 
      	    spam.pre_calibrate_targets(uvfits_files[i])
	    precalibrator_log.write("Successful precalibration of " + str(uvfits_files[i]) +'\n')
	    precalibrator_log.flush()
	    print "*****Precalibration of UVFITS DONE*****"
	    new_files = os.listdir('./')
	    add_files = [z for z in new_files if z not in old_files]
	    for k in add_files:
		file_no = ''
		file_list = re.findall(r'[.][\d]+[.]',uvfits_files[i])
		if file_list != []:
			file_no = file_list[0][1:-1]
	    	
	    	os.system('mv ' + str(k) + ' ' + str(k).replace('.UVFITS','')+'_' + str(file_no) + str('.UVFITS'))
	    mid_list = [uvfits_files[i]]                                # [uvfits_file]
	    newer_files = os.listdir('./')
	    added_files = [z for z in newer_files if z not in old_files]
	    for j in added_files:	
	    	mid_list.append(j)
        except RuntimeError,r:
            precalibrator_log.write("Error in precalibration of " + str(uvfits_files[i]) + '\n' +str(r)+'\n********************************************************\n')
            precalibrator_log.flush()
            failed_files.write(CURRENT_DIR + '/' +str(uvfits_files[i]).replace('.UVFITS','')+" : Precalibration error\n")
	    failed_files.flush()
	    print "*****Precalibration of UVFITS STOPPED*****"
	    print r
	    new_files_partial = os.listdir('./')
	    added_files_partial = [z for z in new_files_partial if z not in old_files]
	    
	    #for i in added_files_partial:
	    	#os.system('rm ' + str(i))
	    continue	
	final_list.append(mid_list)
    sys.stdout = original_stdout
    sys.stderr = original_stderr
    os.chdir('../')
    return final_list #Returns final_list in the form [[uvfits_file1,newuvfits1_1,newuvfits1_2,..],[uvfits_file2,newuvfits2_1,newuvfits2_2,..]]

        
def main():     
    #Copy all LTA files in valid obs dir to fits directory for processing
    
    for CURRENT_DIR in THREAD_FILES:
    	directory_log.write(CURRENT_DIR + '\n')
    	directory_log.flush()
        if CURRENT_DIR != '':

            os.system('touch ' + CURRENT_DIR +'/valid.log')

            os.system('echo "Valid File" > ' + CURRENT_DIR +'/valid.log')

	    os.chdir(CURRENT_DIR+'/')

	    lta_list = glob.glob('*.lta*')
	    
	    for lta_list_file in lta_list:	

		os.chdir(c_path +'/')

		#os.system('mv ' + CURRENT_DIR + '/* ' + 'fits/')
            	#Write the list of sources to the current directory
            	os.system('mv ' + CURRENT_DIR + '/' + lta_list_file + ' fits/')

            	os.chdir('fits/')
            	
            	source_with_lta = test_validity.test_validity()                   #[[source1,lta_file1],[source2,lta_file2]]

            	os.chdir('../')
	    	
	    	lta_to_uvfits(CURRENT_DIR)                           #can be optimized, dont need to write them in the file source_lta
            	uvfits_with_newuvfits = precalibrator(CURRENT_DIR)   #can be optimized, dont need to write them in the file uvfits_newuvfits  
	    	#print "Preprocessing " + str(source_with_lta)
	    	#print "Preprocessing "+ str(uvfits_with_newuvfits)
	    	os.chdir('fits/')

	    	source_lta = open('source_lta.txt','w+')
	    	uvfits_newuvfits = open('uvfits_newuvfits.txt','w+')
	    	'''Writes to the source_lta file in the format 
	
			source1 <space> lta_file1
			source2 <space> lta_file2		    
	
	    	'''
	    	string = ""
	    	for i in source_with_lta:
	    		for j in i:
	    			string += j + ' '
	    		string += '\n'
	    	source_lta.write(string)
	    	source_lta.flush()
	    	'''Writes to the uvfits file in the format 
	
			uvfits1 <space> new_uvfits1 <space> new_uvfits2 <space> new_uvfits3
			uvfits1 <space> new_uvfits1 <space> new_uvfits2 <space> new_uvfits3   
	
	    	'''
	    	string = ""            
	    	for i in uvfits_with_newuvfits:
	    		for j in i:
	    			string += j + ' '
	    		string += '\n'
	    	uvfits_newuvfits.write(string)
	    	uvfits_newuvfits.flush()

	    	os.system('mkdir ' + lta_list_file.replace('.','_'))

	    	os.system('mv ./*.* '  + lta_list_file.replace('.','_'))

	    	os.chdir('../')

            	os.system('mv fits/* ' + CURRENT_DIR)
	    	

    else:

        os.system('touch ' + CURRENT_DIR + '/valid.log')

        os.system('echo "Invalid File" > ' + CURRENT_DIR+'/valid.log')
    	files = glob.glob(CURRENT_DIR + '/*.lta')
    	for i in files:	
    		failed_files.write(str(i) + " : Invalid file")	    
    		failed_files.flush()
    
#process target files
def post():
    
    for CURRENT_DIR in THREAD_FILES:
    	if CURRENT_DIR != '':
    		os.chdir(CURRENT_DIR+'/')
    		directory_list = [x[0][2:] for x in os.walk('./')][1:] #gives list of directories
    		os.chdir(c_path+'/')
    		for directory_list_name in directory_list:
    			os.system('mv ' + CURRENT_DIR +'/'+directory_list_name+'/*' + ' fits/' )
    			start = time.time()
    			#os.system('mv ' + CURRENT_DIR + '/* ' + 'fits/')
    			os.chdir('fits/')
    		
    			new_source_lta = open('source_lta.txt','r').read().split('\n')
	    		new_uvfits_newuvfits = open('uvfits_newuvfits.txt','r').read().split('\n')
			a = os.listdir('./')
			print a		
			#print "From file " + str(new_source_lta)
			#print "From file " + str(new_uvfits_newuvfits)	   	
			source_with_lta = []
	   		uvfits_with_newuvfits = []
	   		for i in range(len(new_source_lta)-1):
	   			source_with_lta.append(new_source_lta[i].split())
	   		for i in range(len(new_uvfits_newuvfits)-1):
	   			uvfits_with_newuvfits.append(new_uvfits_newuvfits[i].split())
	   		#print "Main processing " + str(source_with_lta)
	   		#print "Main processing " + str(uvfits_with_newuvfits)
	
			'''
			Checks for the lta_file name in uvfits_file, selects the list with the relevant uvfits_file,
			then checks for source name in the list with the relevant new_uvfits file.
			'''
			process_target_log = open('process_log.txt','w+')
	
    			for source,lta in source_with_lta:
				flag = 0
		    		for i in range(len(uvfits_with_newuvfits)):
		    			if lta in uvfits_with_newuvfits[i][0]:
		    				for j in range(1,len(uvfits_with_newuvfits[i])):
		    					if source in uvfits_with_newuvfits[i][j]:
		    						try:	
		    							old_files_process = os.listdir('./')
		    							spam.process_target(uvfits_with_newuvfits[i][j])
									process_target_log.write("Successful final processing of "+str(uvfits_with_newuvfits[i][j])+'\n')
									process_target_log.flush()
									succeeded_files.write(CURRENT_DIR + '/' +str(lta)+'\n')
									succeeded_files.flush()
									new_files_process = os.listdir('./')
									added_files_process = [z for z in new_files_process if z not in old_files_process]
									file_no = ''
									file_list = re.findall(r'[.][\d]+[.]',uvfits_with_newuvfits[i][0])
									if file_list != []:
										file_no = file_list[0][1:-1]
									for k in added_files_process:
										os.system('mv ' + str(k) + ' ' + str(k).replace('.FITS','')+'_' + str(file_no) + str('.FITS'))	
		    							print "*****Final Processing of UVFITS DONE*****"
		    							flag = 1
		    						except RuntimeError,r:
		    							new_files_process_error = os.listdir('./')
									added_files_process_error = [z for z in new_files_process_error if z not in old_files_process]
									#for i in added_files_process_error:
									#	os.system('rm ' + str(i))
		    							process_target_log.write("Error in final processing of "+str(uvfits_with_newuvfits[i][j])+'\n' + str(r) + '\n*******************************************************\n')
		    							process_target_log.flush()
            								failed_files.write(CURRENT_DIR + '/' +str(lta)+" : Final Processing error\n")
		    							failed_files.flush()
		    							print "*****Final Processing of UVFITS STOPPED*****"
		    							print r
		    							flag = 1
		    							break
		    				if flag == 1:
		    					break
	            	end = time.time()
        	    	timefile = open('time_process.txt','w+')
        	    	timefile.write(str((end-start)/3600.0))
			timefile.flush()
        	    	os.chdir('../')
		    
		    	os.system('mv fits/* ' + CURRENT_DIR+'/'+directory_list_name+'/')
	    	


c_path = os.getcwd()
main()

post()

print "Done"

