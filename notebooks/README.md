# 3 - Jupyter notebooks to identify potential biomarkers


Now that we have our peak table, identification and the associated metadata, we can use apply various machine learning methods to identify potential biomarkers. The objective is to find compounds which differentiate __Patient__ and __Control__ samples.

In the available notebooks, the point is to explore the data we got from _metaboigniter_, apply statistical analysis and machine learning models.


This folder contains 3 scripts :
- <code>run_commands_docker.sh</code>
- <code>run_commands_singularity.sh</code>
- <code>slurm_notebooks.sb</code>

The first two scripts (<code>run_commands_docker.sh</code> and <code>run_commands_singularity.sh</code>) contain the command to pull the docker image from the DockerHub, and convert it to a Singularity image if Singularity is used. These two scripts also contain the command to run the image to launch the Jupyter notebooks, which will create an URL to paste in a browser to access JupyterLab.

The script with the _.sb_ extension contains slurm options and commands to use the above scripts via Slurm.
Slurm is the job scheduler of IARC's HPC. It allows to launch and monitor jobs, manage job parallelisation, allocate specific resources (computer nodes) to users. The first few lines (starting with <code>#</code>) of a slurm file (here code>slurm_msconvert.sb</code>) specify slurm options (job name, number of nodes, memory, ...). Then, the other lines are linux commands, here to launch <code>run_commands_docker.sh</code> or <code>run_commands_singularity.sh</code>.


First, open a terminal on your local machine and connect to IARC's HPC with _ssh_ using the following command :
```bash
ssh <user>@10.120.1.20 -L 8888:127.0.0.1:8888
```
The <code>-L</code> option specifies which port on client (local) will be forwarded to which host and port on remote ([cf doc](https://explainshell.com/explain?cmd=ssh+-L)).


Next, change directory :

```bash
cd <absolute_or_relative_path>/notebooks
```


At this point you have four options to use the notebooks :
- option 1 : Use Docker
- option 2 : Use Singularity
- option 3 : Launch notebooks with Slurm
- option 4 : Launch each notebook in Binder


## Option 1 - Use Docker

The first option is to use the container with Docker.

First, you have to clone this repository, then the only command to run is :

```bash
./run_commands_docker.sh
```

It could take a while to launch the Jupyter environment if it is the first time. First, it will pull and build the Docker image based on the image on [DockerHub](https://hub.docker.com/r/maxvin/data_science_img).

Then, it will clone the repository containing the Jupyter notebooks [link](https://github.com/maxvincent24/metabopipeline_notebooks).

Finally, it will run the Docker image, launching a JupyterLab environment to use the notebooks. On your terminal will appear a URL of this form <code>http://127.0.0.1:8888/lab?token=*token*</code> that you will have to paste in a browser to launch the JupyterLab session.



## Option 2 - Use Singularity

The second option is to use the container with Singularity.

First, you have to clone this repository, then the only command to run is :

```bash
./run_commands_singularity.sh
```

It could take a while to launch the Jupyter environment if it is the first time. First, it will pull the Docker image from [DockerHub](https://hub.docker.com/r/maxvin/data_science_img) and build the Singularity image.

Then, it will clone the repository containing the Jupyter notebooks [link](https://github.com/maxvincent24/metabopipeline_notebooks).

Finally, it will run the Singularity image, launching a JupyterLab environment to use the notebooks. On your terminal will appear a URL of this form <code>http://127.0.0.1:8888/lab?token=*token*</code> that you will have to paste in a browser to launch the JupyterLab session.





## Option 3 - Launch notebooks with Slurm

The third option is to launch the notebooks using Slurm.

The only command to run is :

```bash
sbatch slurm_notebooks.sb <container_choice>
```

The argument <code>container_choice</code> is either "docker" or "singularity", depending on which technology you wnat to use.

Depending on the container choice, it will run either the file <code>run_commands_docker.sh</code> or <code>run_commands_singularity.sh</code>. In the <code>.out</code> file of your slurm job, you will see a URL of this form <code>http://127.0.0.1:8888/lab?token=*token*</code> that you will have to paste in a browser to launch the JupyterLab session.






## Option 4 - Launch each notebook in Binder

The notebooks and their links to Binder can be found on this repository : [maxvincent24/metabopipeline_notebooks](https://github.com/maxvincent24/metabopipeline_notebooks)




