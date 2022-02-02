

import os
import subprocess
import sys

#path_data= input('Enter absolute path to data : ')
#path_data = '/data/EPIC-Pancreatic-Metabolome/work/Raw_Data/RP_POS'
#path_data = '/home/vincentm/data/EPIC-Pancreatic/toy_RP_POS'
path_data = sys.argv[1]
print(f'Original data is located in : {path_data}')

print(f'List of all file conditions : {os.listdir(path_data)}')

# Create output folder mzML
subprocess.run(f'mkdir mzML'.split(' '))

# For all conditions
for condition in os.listdir(path_data):

	print('\n')
	print(200 * '-')
	print(100 * '-', condition, (100 - (len(condition) + 2)) * '-')
	print(200 * '-')

	# Create subdirectory for current condition in mzML folder
	subprocess.run(f'mkdir mzML/{condition}'.split(' '))	

	for file in os.listdir(f'{path_data}/{condition}'):
		
		print(f'Processing conversion of file : {file}')

		pwd = subprocess.run('pwd'.split(' '), encoding='utf-8', stdout=subprocess.PIPE)
		pwd = pwd.stdout.replace('\n', '')
		command = f'singularity run --writable --bind {pwd}:/data test_msconvert/ wine msconvert {path_data}/{condition}/{file} --filter "peakPicking true 1" -o mzML/{condition}/'
		subprocess.run(command.split(' '))
		print()







