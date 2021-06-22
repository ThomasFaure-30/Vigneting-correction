"""
test module for vignetting correction

"""
import cv2 as cv
import numpy as np
import pandas as pd
import time
import os
import glob
import tifffile as tiff

from faure_utils import string_param
from faure_utils import reshape
from faure_utils import erase

timer_start = time.time()
image_count = 0
px, x, y, count_pixel_aberrant = 0, 0, 0, 0 # px de 0 à 2

correction_matrix_rgb = np.ones((3000,4096,3), dtype = float)
csv_file_path = r'C:\Users\thfaure\Desktop\Scripts_python\Vignetage_correction_Faure\correction_matrix.csv'
correction_matrix_rgb[:,:,0] = pd.read_csv(csv_file_path, header = None)
correction_matrix_rgb[:,:,1], correction_matrix_rgb[:,:,2] = correction_matrix_rgb[:,:,0], correction_matrix_rgb[:,:,0]

main_folder_path = r'C:\Users\thfaure\Desktop\2021\Pop_50025\Juin_14_2021\Tiff_brute'
main_output_path = r'C:\Users\thfaure\Desktop\2021\Pop_50025\Juin_14_2021\Tiff_corrige_vignetage'
os.chdir(main_folder_path)
folder_list=glob.glob('*_1')

erase.erase_folder_and_files(main_output_path)

for folder in folder_list:
	image_path = main_folder_path + '\\' + folder
	output_path = main_output_path + '\\' + folder

	print("\nFolder currently processed : " + folder)

	os.chdir(image_path)
	image_list = glob.glob('*.tif')
	if len(image_list) == 0:
		image_list = glob.glob('*.jpg')

	os.chdir(main_output_path)
	os.makedirs(folder)
	os.chdir(image_path)

	for image in image_list:

		os.chdir(image_path)
		image_to_be_corrected = tiff.imread(image)

		if image_to_be_corrected.shape != correction_matrix_rgb.shape:
			print("Different dimensions for images, starting resize processus ...")
			image_to_be_corrected = reshape.resize(image, correction_matrix_rgb.shape[:])

		image_corrected = image_to_be_corrected	
		image_corrected= np.uint16(image_corrected)	
		image_corrected = (image_to_be_corrected * correction_matrix_rgb)
		image_corrected[image_corrected[:,:,:] > 65535] = 65535
		image_corrected= np.uint16(image_corrected)
		
		quantile = np.quantile(image_corrected,0.99)
		if quantile > 65535*0.99:
			print(f"Quantile = {quantile}")
		corrected_name = string_param.suppress_string_char(image,'.tif')
		new_name = corrected_name + "_v.tif"				
		print(f"New de-vignetted image : {new_name}")
		os.chdir(output_path)
		tiff.imwrite(new_name,image_corrected, photometric='rgb', software="Pheno Vignetting correction Module by INRAE")
		image_count += 1

timer_end = time.time()
global_time = timer_end-timer_start
print("")
print("Program took " + str(global_time)+" seconds to fix vignetting effect on "+ str(image_count) +" images.")