

import os
import subprocess
import sys


path_data = sys.argv[1]
if path_data[-1] == '/':
	path_data = path_data[:-1]
print(f'Original data is located in : {path_data}')

path_data_basename = path_data.split('/')[-1]
path_data_prefix = '/'.join(path_data.split('/')[:-1])
if path_data_prefix != '':
	path_data_prefix += '/'
print(f'path_data_prefix : {path_data_prefix}')
subprocess.run(f'mkdir {path_data_basename}_mzML'.split(' '))

command = f'find {path_data} -type d -name "*.d"'
output = subprocess.check_output(command, encoding='utf-8', shell=True)

list_d_files = output.split('\n')
list_d_files = [file for file in list_d_files if file != '']
list_d_files_msconvert = list_d_files
list_d_files = [file.replace(path_data_prefix, '') for file in list_d_files]
list_d_files = ['/'.join(file.split('/')[:-1]) for file in list_d_files]
list_d_files = list(set(list_d_files))
list_d_files = sorted(list_d_files)

dir_to_create = []
for directory in list_d_files:	
	for i in range(1, len(directory.split('/'))):
		dir_to_create.append('/'.join(directory.split('/')[:i+1]))


dir_to_create = sorted(list(set(dir_to_create)))
dir_to_create = [dir_.replace(path_data_basename, path_data_basename + '_mzML') for dir_ in dir_to_create]
for elt in dir_to_create:
	print(f'elt : {elt}')
	subprocess.run(f'mkdir {elt}'.split(' '))

print()

pwd = subprocess.run('pwd'.split(' '), encoding='utf-8', stdout=subprocess.PIPE)
pwd = pwd.stdout.replace('\n', '')

for file in list_d_files_msconvert:

	print(f'file : {file}')
	output = '/'.join(file.replace(path_data_prefix, '').split('/')[:-1]).replace(path_data_basename, path_data_basename + '_mzML')
	print(f'output : {output}')
	print()
	command = f'singularity run --writable --bind {pwd}:/data img_msconvert/ wine msconvert {file} --filter "peakPicking true 1" -o {output}'
	print(f'command : {command}')
	subprocess.run(command.split(' '))
