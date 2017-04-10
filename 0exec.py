import spam
import time
import os, re
import glob
import trace
import sys
import time,datetime
import socket
hostname=socket.gethostname()
spam.set_aips_userid(10)

failed_files = open('datfil/failed_files.log','a+')
succeeded_files = open('datfil/succeeded_files.log','a+')
succeeded_files.write('Successful final processing\n\n')
succeeded_files.flush()

failed_files.write('Failed files\n\n')
failed_files.flush()
directory_log_pre = open('directory_log_pre.txt','a+')
directory_log_post = open('directory_log_post.txt','a+')
os.system('pwd')

def precalibrator(CURRENT_DIR):
	os.chdir('fits/')
	original_stdout = sys.stdout
	original_stderr = sys.stderr
	l2u_precal_log = open('l2u_precal.log','a+')
	l2u_precal_log.write('\n\n\n******PRECALIBRATION STARTED******\n\n\n')
	sys.stdout = l2u_precal_log
	sys.stderr = l2u_precal_log
	uvfits_files = glob.glob('*.UVFITS')
	#print uvfits_files
	final_list = []
	precalibrator_log = open('precalibrator_log.txt', 'a+')
	#os.system('pwd')	
	#print('\n\n\nPrinting user ID AIPS\n\n\n')
	#print spam.get_aips_userid()
	if uvfits_files != []:
		try:
			#To get a list of newly added files after precalibration
  			spam.pre_calibrate_targets(uvfits_files[0])
			precalibrator_log.write(hostname+"\n"+"Successful precalibration of " + str(uvfits_files[0]) +'\n********************************************************\n')
			precalibrator_log.flush()
			os.remove(str(uvfits_files[0]))
			#print "*****Precalibration of UVFITS DONE*****"
		except Exception,r:
			precalibrator_log.write(hostname+"\n"+"Error in precalibration of " + str(uvfits_files[0]) + '\n' +str(r)+'\n********************************************************\n')
			precalibrator_log.flush()
			failed_files.write(CURRENT_DIR + '/' +str(uvfits_files[0]).replace('.UVFITS','')+" : Precalibration error\n")
			failed_files.flush()
			#os.system('rm -rf ./*')
			#print "*****Precalibration of UVFITS STOPPED*****"
	else:
		failed_files.write(CURRENT_DIR + '/' +" : UVFITS FILE not found, LTA_to_UVFITS no output\n")
		failed_files.flush()
		precalibrator_log.write("Error in precalibration due to no UVFITS file "+'\n********************************************************\n')
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

#conversion and precalibration
def pre(CURRENT_DIR):
	os.system('touch ' + CURRENT_DIR +'/valid.log')
	os.system('echo "Valid File" > ' + CURRENT_DIR +'/valid.log')
	os.chdir(CURRENT_DIR+'/')

	uv_fits_list = glob.glob('*.UVFITS')
	lta_list = uv_fits_list[0].replace('.UVFITS','') #since there's only one single uvfits file
	os.chdir(c_path +'/')

	os.system('cp ' + CURRENT_DIR + '/' + uv_fits_list[0] + ' fits/')

	before_precal = os.listdir('fits/')
	precalibrator(CURRENT_DIR)   #can be optimized, dont need to write them in the file uvfits_newuvfits
	after_precal = os.listdir('fits/')
	added_precal = [z for z in after_precal if z not in before_precal]
	
	directory_log_post.write(CURRENT_DIR + '\n')
	directory_log_post.flush()
	
	start = time.time()
	for precal_file in added_precal:
		if '.UVFITS' in precal_file:
			precal_uvfits = ''
			if 'S.UVFITS' not in precal_file:
				precal_uvfits = precal_file
				post(CURRENT_DIR,precal_uvfits,lta_list[0])
				
	end = time.time()
	os.chdir('fits/')
	timefile = open('time_process.txt','a+')
	timefile.write(str(datetime.timedelta(seconds=end-start)))
	timefile.flush()
	for added_precal_file in added_precal:
		if '.UVFITS' in added_precal_file:	
			os.system('mv ' + added_precal_file + ' ' + added_precal_file.replace('.UVFITS','') + '_' + lta_list[0].replace('.','_')+ '.UVFITS')
	os.chdir('../')
	os.system('mkdir /gadpu/scratch/IMAGES/' + lta_list.replace('.','_'))
	os.system('mv fits/*' + ' /gadpu/scratch/IMAGES/'+ lta_list.replace('.','_'))
	
#process target files
def post(CURRENT_DIR,precal_uvfits,lta):
	os.chdir('fits/')
	
	
	
	process_target_log = open('process_log.txt','a+')
	old_datfil_log = os.listdir('../datfil/')
	old_files = os.listdir('./')
	try:	
		spam.process_target(precal_uvfits)
		process_target_log.write(hostname+"\n"+"Successful final processing of "+str(precal_uvfits)+'\n')
		process_target_log.flush()
		succeeded_files.write(CURRENT_DIR + '/'+'\n')
		succeeded_files.flush()
		#print "*****Final Processing of UVFITS DONE*****"
	except Exception,r:
		process_target_log.write(hostname+"\n"+"Error in final processing of "+str(precal_uvfits)+'\n' + str(r) + '\n*******************************************************\n')
		process_target_log.flush()
		failed_files.write(CURRENT_DIR + '/' + " : Final Processing error\n")
		failed_files.flush()
		#os.system('rm -rf ./*')
		#print "*****Final Processing of UVFITS STOPPED*****"
		#print r
	
	new_files = os.listdir('./')	
	added_files = [z for z in new_files if z not in old_files]
	for added_file in added_files:
		if "obit_lowfrfi.py" not in added_file:
			if ".FITS" in added_file:	
				os.system('mv ' + added_file + ' ' + added_file.replace('.FITS','')+'_'+lta.replace('.','_')+'.FITS')
			if ".UVFITS" in added_file:
				os.system('mv ' + added_file + ' ' + added_file.replace('.UVFITS','')+'_'+lta.replace('.','_')+'.UVFITS')

	
	new_datfil_log = os.listdir('../datfil/')
	added_datfil_log = [z for z in new_datfil_log if z not in old_datfil_log]
	for spam_log in added_datfil_log:
		if 'spam' in spam_log and '.log' in spam_log:
			os.system('mv ../datfil/' + str(spam_log) + ' ./')
	
	
	os.chdir('../')
	

SOURCE_DIR = '/gadpu/scratch/FILES/'	

THREAD_FILES = os.listdir(SOURCE_DIR)
for i in THREAD_FILES:
	THREAD_FILES[THREAD_FILES.index(i)] = SOURCE_DIR + i	
#print THREAD_FILES	
c_path = os.getcwd()
main()
