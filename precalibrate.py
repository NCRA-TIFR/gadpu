def precalibrater(source_name):
    uvfits_files = glob.glob('*.UVFITS')
    #flag_files = glob.glob('*.FLAGS*')
    for i in range(0,len(uvfits_files)):
        if source_name in uvfits_files[i]:	
            spam.pre_calibrate_targets(uvfits_files[i])
