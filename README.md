# Metabopipeline

This pipeline aims to analyse metabolomics data, from the raw files to statistical analysis.

The pipeline is divised in three parts :
- file conversion : using <code>msconvert</code> from Proteowizard tools, we can convert files from vendro format (.d) to open source format (.mzML).
- metaboigniter : using [metaboigniter](https://github.com/nf-core/metaboigniter) pipeline, we can preprocess the .mzML files to get the intensity peak table, identification, ...
- notebooks : in Jupyter notebooks, we can explore, process and analyse the output of metaboigniter, using python and R languages.


## 0 - Install singularity images

Before using the pipeline, you have to run the shell script <code>run_install.sb</code> as a slurm job, using the following command :
```bash
sbatch run_install.sb
```

This script will pull and convert two Docker images to Singularity images. Singularity is a container runtime, like Docker, and is the one deployed on IARC's HPC :
- the first image is the <a href="https://hub.docker.com/r/chambm/pwiz-skyline-i-agree-to-the-vendor-licenses" target="_blank">Proteowizard docker image</a>. The Singularity image will be created and will be seen in the subfolder <code>msconvert/img_msconvert</code>;
- the second image is an image created for data science (<a href="https://hub.docker.com/r/maxvin/data_science_img" target="_blank">link to DockerHub</a>), with Python, R and Julia deployed in a JupyterLab environment. The Singularity image will be created and will be seen in the subfolder <code>notebooks/MLnotebooks_img</code>


You can follow the advancement of the slurm job with the following command, displaying all your current running jobs :
```bash
iarc_squeue -u <your_username>
```

If you don't see a job named "run_install", it surely means everything worked well :wink:



## 1 - Convert .d to .mzML files with dockerized msconvert

Corresponding [README](https://github.com/maxvincent24/metabopipeline/tree/main/msconvert).


## 2 - Run metaboigniter pipeline




## 3 - Jupyter notebooks to identify potential biomarkers

Corresponding [README](https://github.com/maxvincent24/metabopipeline/tree/main/notebooks).




