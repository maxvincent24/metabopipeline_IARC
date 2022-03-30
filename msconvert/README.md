
# 1 - Convert .d to .mzML files with dockerised msconvert

This folder contains 3 scripts :
- <code>run_commands_docker.sh</code>
- <code>run_commands_singularity.sh</code>
- <code>slurm_msconvert.sb</code>

The first two scripts (<code>run_commands_docker.sh</code> and <code>run_commands_singularity.sh</code>) contain the command to pull the docker image from the DockerHub, and convert it to a Singularity image if Singularity is used. These two scripts also contain the command to run the image and convert the data from .d to .mzML format.

The script with the _.sb_ extension contains slurm options and commands to use the above scripts via Slurm.
Slurm is the job scheduler of IARC's HPC. It allows to launch and monitor jobs, manage job parallelisation, allocate specific resources (computer nodes) to users. The first few lines (starting with <code>#</code>) of a slurm file (here code>slurm_msconvert.sb</code>) specify slurm options (job name, number of nodes, memory, ...). Then, the other lines are linux commands, here to launch <code>run_commands_docker.sh</code> or <code>run_commands_singularity.sh</code>.

Let's take an example with data organised as follows :

    data
    ├── Batch1
    │   ├── Blanks
    │   │   ├── Blank_1.d
    │   │   ├── Blank_2.d
    │   ├── MSMS
    │   │   ├── MSMS_1.d
    │   │   ├── MSMS_2.d
    │   ├── QCs
    │   │   ├── QC_1.d
    │   │   ├── QC_2.d
    │   ├── Samples
    │   │   ├── Sample_1.d
    │   │   ├── Sample_2.d

Remark : The data folder can have any name, not necessarly <code>data</code>, but without any spaces.

First, in a terminal, navigate to the directory containing your data folder (with <code>cd</code>).



## Option 1 : Use Docker

The first option is to use the container with Docker.

The only command to run is :

```bash
./run_commands_docker.sh data
```

The <code>data</code> corresponds to the data folder name.

The output folder containing <code>.mzML</code> files is created in the current working directory and named *<data_folder_name>\_mzML* (<code>data_mzML</code> for the example).



## Option 2 : Use Singularity

The second option is to use the container with Singularity.

The only command to run is :

```bash
./run_commands_singularity.sh data
```

The <code>data</code> corresponds to the data folder name.

The output folder containing <code>.mzML</code> files is created in the current working directory and named *<data_folder_name>\_mzML* (<code>data_mzML</code> for the example).




## Option 3 : Launch conversion with Slurm

The third option is to launch the conversion using Slurm.

The only command to run is :

```bash
sbatch slurm_msconvert.sb <container_choice> <data_folder>
```

The argument <code>container_choice</code> is either "docker" or "singularity", depending on which technology you wnat to use.

The <code>data_folder</code> is the folder containing your <code>.d</code> files, (<code>data</code> for the example).

The output folder containing <code>.mzML</code> files is created in the current working directory and named *<data_folder_name>\_mzML* (<code>data_mzML</code> for the example).




---


This folder contains a shell script (<code>slurm_msconvert.sb</code>) and a python script (<code>dtomzML.py</code>).

The shell script (extension _.sb_) contains slurm options and one command.

Slurm is the job scheduler of IARC's HPC. It allows to launch and monitor jobs, manage job parallelisation, allocate specific resources (computer nodes) to users. The first few lines (starting with <code>#</code>) of a slurm file (here _slurm_msconvert.sb_) specify slurm options (job name, number of nodes, memory, ...). Then, the other lines are linux commands (here we just have one) :
- the command launches the python script (<code>dtomzML.py</code>), which will convert all _.d_ files in the folder (and its subfolders) passed as argument.

For example, the data is organised as follows :

    data
    ├── Batch1
    │   ├── Blanks
    │   │   ├── Blank_1.d
    │   │   ├── Blank_2.d
    │   ├── MSMS
    │   │   ├── MSMS_1.d
    │   │   ├── MSMS_2.d
    │   ├── QCs
    │   │   ├── QC_1.d
    │   │   ├── QC_2.d
    │   ├── Samples
    │   │   ├── Sample_1.d
    │   │   ├── Sample_2.d

In this case, the command to launch to convert all _.d_ files is
```bash
sbatch slurm_msconvert.sb <absolute_or_relative_path>/data/Batch1
```

The <code>sbatch</code> command submits a slurm job with a shell script (<code>slurm_msconvert.sb</code> here), which will (as mentioned above) create the Singularity image for _msconvert_ and launches the python script with the path to data as argument.

The waiting time between the moment the job is submitted and the moment it is launched hugely depends on the queue size. Once the job is launched, it should take less than 5 minutes to create the Singularity image, and about 10 seconds per file for conversion. The logs can be seen in the <code>slurm-<job_ID>.out</code>.

In the example above, the path to data passed as argument was <code>data/Batch1</code>, then the created folder to store the _.mzML_ files will be called <code>Batch1_mzML</code> and will be stored in the current working directory. The subfolder organisation of the input data folder is preserved.


:white_check_mark: The _.d_ files are now converted to _.mzML_ !


