import spam
import time
import os, re
import glob
import trace
import test_validity
import sys
import time
#Assign core to the process
pid = os.getpid()
os.system('taskset -cp 5 ' + str(pid))
spam.set_aips_userid(15)
#List of all directories containing valid observations 
#List of all directories for current threads to process
print 'Executing this thread'

failed_files = open('datfil/failed_files.log','w+')
succeeded_files = open('datfil/succeeded_files.log','w+')
succeeded_files.write('Successful final processing\n\n')
succeeded_files.flush()
failed_files.write('Failed files\n\n')
failed_files.flush()
directory_log_pre = open('directory_log_pre.txt','w+')
directory_log_post = open('directory_log_post.txt','w+')
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
	
	lta_file_name = lta_files[0]
	uvfits_file_name = lta_file_name +'.UVFITS'		
	try:
		spam.convert_lta_to_uvfits( lta_file_name, uvfits_file_name )
		lta_to_uvfits_log.write("Successful conversion of " + str(lta_file_name) + " to " + str(lta_file_name+'.UVFITS')+'\n')
		lta_to_uvfits_log.flush()
		print "*****LTA to UVFITS conversion DONE*****"
		#In case of success in conversion remove the LTA file
		#os.system('rm ' + lta_file_name)
	except Exception,r:
		#Write to log file
		lta_to_uvfits_log.write("Error in conversion of " + str(lta_file_name) + " to " + str(lta_file_name+'.UVFITS')+'\n' + str(r) +'\n********************************************************\n')
		lta_to_uvfits_log.flush()
		failed_files.write(CURRENT_DIR + '/' +str(lta_file_name)+" : LTA to UVFITS conversion error\n")
		failed_files.flush()
		os.system('rm -rf ./*')
		print "*****LTA to UVFITS conversion STOPPED*****"
		#print r 
		#Remove the UVFITS file 
		#os.system('rm ' + str(lta_file_name)+ '.UVFITS')
		
	sys.stdout = original_stdout
	sys.stderr = original_stderr
	os.chdir('../')
	#return lta_files 

def precalibrator(CURRENT_DIR):
	os.chdir('fits/')
	original_stdout = sys.stdout
	original_stderr = sys.stderr
	l2u_precal_log = open('l2u_precal.log','a')
	sys.stdout = l2u_precal_log
	sys.stderr = l2u_precal_log
	uvfits_files = glob.glob('*.UVFITS')
	print uvfits_files
	final_list = []
	precalibrator_log = open('precalibrator_log.txt', 'w+')
	os.system('pwd')
	print('\n\n\nPrinting user ID AIPS\n\n\n')
	print spam.get_aips_userid()
	try:
		#To get a list of newly added files after precalibration
  		spam.pre_calibrate_targets(uvfits_files[0])
		precalibrator_log.write("Successful precalibration of " + str(uvfits_files[0]) +'\n')
		precalibrator_log.flush()
		print "*****Precalibration of UVFITS DONE*****"
	except Exception,r:
		precalibrator_log.write("Error in precalibration of " + str(uvfits_files[0]) + '\n' +str(r)+'\n********************************************************\n')
		precalibrator_log.flush()
		failed_files.write(CURRENT_DIR + '/' +str(uvfits_files[0]).replace('.UVFITS','')+" : Precalibration error\n")
		failed_files.flush()
		#os.system('rm -rf ./*')
		print "*****Precalibration of UVFITS STOPPED*****"
			
	sys.stdout = original_stdout
	sys.stderr = original_stderr
	os.chdir('../')

		
def main():	 
	#Copy all LTA files in valid obs dir to fits directory for processing
	
	for CURRENT_DIR in THREAD_FILES:
		#if valid.log present in directory, skip the directory else process
		if "valid.log" in os.listdir(CURRENT_DIR+'/'):
			continue
		else:
			if CURRENT_DIR != '':
				directory_log_pre.write(CURRENT_DIR + '\n')
				directory_log_pre.flush()
				pre(CURRENT_DIR)
	
	#WRITE CODE TO BREAK PROCESS WHEN ONE STEP FAILS WHEN SETTING FLAGS
								

#conversion and precalibration
def pre(CURRENT_DIR):
	os.system('touch ' + CURRENT_DIR +'/valid.log')
	os.system('echo "Valid File" > ' + CURRENT_DIR +'/valid.log')
	os.chdir(CURRENT_DIR+'/')

	lta_list = glob.glob('*.lta*')
	
	os.chdir(c_path +'/')

	os.system('cp ' + CURRENT_DIR + '/' + lta_list[0] + ' fits/')

	os.chdir('fits/')
				
	source_with_lta = test_validity.test_validity()				   #[[source1,lta_file1],[source2,lta_file2]]

	os.chdir('../')
			
	lta_to_uvfits(CURRENT_DIR)	   #can be optimized, dont need to write them in the file source_lta
	before_precal = os.listdir('fits/')
	precalibrator(CURRENT_DIR)   #can be optimized, dont need to write them in the file uvfits_newuvfits
	after_precal = os.listdir('fits/')
	added_precal = [z for z in after_precal if z not in before_precal]
	
	precal_uvfits = ''
	for precal_file in added_precal:
		if source_with_lta in precal_file:
			if 'S.UVFITS' not in precal_file:
				precal_uvfits = precal_file
				break
	
	
	directory_log_post.write(CURRENT_DIR + '\n')
	directory_log_post.flush()
		
	post(CURRENT_DIR,precal_uvfits,lta_list[0])
	os.chdir('fits/')
	for added_precal_file in added_precal:
		if '.UVFITS' in added_precal_file:	
			os.system('mv ' + added_precal_file + ' ' + added_precal_file.replace('.UVFITS','') + '_' + lta_list[0].replace('.','_')+ '.UVFITS')
	#os.system('mkdir ' + lta_list[0].replace('.','_'))
	#os.system('mv ./*.* '  + lta_list[0].replace('.','_'))
	os.chdir('../')
	os.system('mkdir /data2/archit/FITS/' + lta_list[0].replace('.','_'))
	os.system('mv fits/*' + ' /data2/archit/FITS/'+ lta_list[0].replace('.','_'))
	


	
#process target files
def post(CURRENT_DIR,precal_uvfits,lta):
	os.chdir('fits/')
	start = time.time()
	
	
	process_target_log = open('process_log.txt','w+')
	old_datfil_log = os.listdir('../datfil/')
	old_files = os.listdir('./')
	try:	
		spam.process_target(precal_uvfits)
		process_target_log.write("Successful final processing of "+str(precal_uvfits)+'\n')
		process_target_log.flush()
		succeeded_files.write(CURRENT_DIR + '/'+'\n')
		succeeded_files.flush()
		print "*****Final Processing of UVFITS DONE*****"
	except Exception,r:
		process_target_log.write("Error in final processing of "+str(precal_uvfits)+'\n' + str(r) + '\n*******************************************************\n')
		process_target_log.flush()
		failed_files.write(CURRENT_DIR + '/' + " : Final Processing error\n")
		failed_files.flush()
		#os.system('rm -rf ./*')
		print "*****Final Processing of UVFITS STOPPED*****"
		print r
	
	new_files = os.listdir('./')	
	added_files = [z for z in new_files if z not in old_files]
	for added_file in added_files:
		if "obit_lowfrfi.py" not in added_file:
			os.system('mv ' + added_file + ' ' + added_file.replace('.FITS','')+'_'+lta.replace('.','_')+'.FITS')
	end = time.time()
	timefile = open('time_process.txt','w+')
	timefile.write(str((end-start)/3600.0))
	timefile.flush()
	new_datfil_log = os.listdir('../datfil/')
	added_datfil_log = [z for z in new_datfil_log if z not in old_datfil_log]
	for spam_log in added_datfil_log:
		if 'spam' in spam_log and '.log' in spam_log:
			os.system('mv ../datfil/' + str(spam_log) + ' ./')
	
	
	os.chdir('../')
	

SOURCE_DIR = '/data2/archit/datum/'	

THREAD_FILES = os.listdir(SOURCE_DIR)
for i in THREAD_FILES:
	THREAD_FILES[THREAD_FILES.index(i)] = SOURCE_DIR + i	
print THREAD_FILES	
c_path = os.getcwd()
main()


print "Done"

