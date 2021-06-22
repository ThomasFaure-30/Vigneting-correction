import re
import glob
import os
import cv2 as cv

class string_param:

	@staticmethod
	def suppress_string_char(file_name,char):
			new_name = file_name.replace(char, "")
			return new_name


class erase:
	
	@staticmethod
	def erase_folder_and_files(main_folder_path):
		os.chdir(main_folder_path)
		print("")
		print("Folder currently processed : " + main_folder_path)

		folder_list = glob.glob('*_1')
		folder_count = 0
		file_count = 0

		for folder in folder_list:				# Supprime tous les DOSSIERS détectés par le glob.glob dans le dossier
			folder_path = main_folder_path + '\\' + folder
			os.chdir(folder_path)
			file_list = glob.glob('*')

			for file in file_list:					# Supprime tous les FICHIERS détectés par le glob.glob dans le sous-dossier folder indiqué par le path
				file_path = folder_path + '\\' + file
				os.remove(file_path)
				file_count = file_count + 1

			os.chdir(main_folder_path)
			os.rmdir(folder_path)
			folder_count = folder_count + 1

		print("Program erased "+ str(file_count) +" files inside "+ str(folder_count) +" folders. ")

class reshape:

	@staticmethod
	def resize(image_path, shape, message=True):

		image = image_path 
		source = cv.imread(image)
		dim = shape

		new_image = cv.resize(source, dim, interpolation = cv.INTER_AREA)
		if message == True:
			print("Resized dimension : ", new_image.shape)
		return new_image
