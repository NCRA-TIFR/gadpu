def lta_to_uvfits():
	os.chdir(data_dir+DIR_NAME+'/fits')
	lta_files = glob.glob('*.lta*')
	flag_files = glob.glob('*.FLAGS*')
	for i in range(len(lta_files)):
		lta_file_name = lta_files[i]
		uvfits_file_name = lta_files[i]+'.UVFITS'
		spam.convert_lta_to_uvfits( lta_file_name, uvfits_file_name )
		
	
	
