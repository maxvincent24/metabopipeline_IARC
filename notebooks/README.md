# 3 - Jupyter notebooks to identify potential biomarkers

Now that we have our peak table, identification and the associated metadata, we can use apply various machine learning methods to identify potential biomarkers. The objective is to find compounds which differentiate __Patient__ and __Control__ samples.

In the available notebooks, the point is to explore the data we got from _metaboigniter_, apply statistical analysis and machine learning models.


## Environment installation

First, open a terminal on your local machine and connect to IARC's HPC with _ssh_ using the following command :
```bash
ssh <user>@10.120.1.20 -L 8888:127.0.0.1:8888
```

Next, change directory :

```bash
cd <absolute_or_relative_path>/notebooks
```

Then, the following command will pull the __Docker__ image containing all the environment needed to use the __Jupyter notebooks__ and convert it to a __Singularity__ image, to be used on IARC's HPC.
```bash
singularity build --sandbox metabopipeline_notebooks docker://maxvin/metabopipeline_notebooks:latest
```
Building the image should take a few minutes. The Singularity image will be created and can be seen in the subfolder <code>metabopipeline_notebooks</code>.

Then, the image can be run interactively with the following command :
```bash
singularity run metabopipeline_notebooks/
```

The prompt, the short text message at the start of the command line (e.g. <code>vincentm@hn:~ $</code>) on IARC's HPC, will change to a sober <code>Singularity></code>. At this point, all commands run in the terminal are run inside the Singularity image.

By running (inside the image)
```bash
ls -la metabopipeline_notebooks/
```
we can see that the image is based on an Ubuntu image.

To launch a Jupyter session, we use this command :
```bash
jupyter notebook --ip=0.0.0.0 --port=8888 --no-browser --allow-root
```
A few lines will be displayed, in particular some URLs. Copy and paste the one with this form in a browser <code>http://127.0.0.1:8888/?token=&#60;blablabla&#62;</code>.


A Jupyter session should appear, we can navigate in the subfolders to <code>./metabopipeline_notebooks/home/ML_pipeline/</code> to access notebooks and useful python scripts. Needed packages are installed with specified versions, no need to manage package version, everything is already done :sunglasses:

The notebooks can now be launched :muscle:


