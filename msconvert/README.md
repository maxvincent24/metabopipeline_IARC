
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

:white_check_mark: The _.d_ files are now converted to _.mzML_ !

