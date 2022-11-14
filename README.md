# Metabopipeline

This pipeline aims to analyse metabolomics data, from the raw files to statistical analysis.

The pipeline is divised in three parts :
- file conversion : using <code>msconvert</code> from Proteowizard tools, we can convert files from vendro format (.d) to open source format (.mzML).
- metaboigniter : using [metaboigniter](https://github.com/nf-core/metaboigniter) pipeline, we can preprocess the .mzML files to get the intensity peak table, identification, ...
- notebooks : in Jupyter notebooks, we can explore, process and analyse the output of metaboigniter, using python and R languages.



## 1 - Convert .d to .mzML files with dockerized msconvert

This part allows to easily convert files from Agilent vendor format *.d* to open-source format *.mzML*.

Corresponding [README](https://github.com/maxvincent24/metabopipeline/tree/main/msconvert).


## 2 - Run metaboigniter pipeline

This part allows to preprocess *.mzML* files with *metaboigniter* pipeline, giving peak tables as output : table of feature intensities for each sample.

**For now, _metaboigniter_ part is still in development.**


## 3 - Jupyter notebooks to identify potential biomarkers

This part allows to launch a JupyterLab session, with notebooks to analyse peak tables.

Corresponding [README](https://github.com/maxvincent24/metabopipeline/tree/main/notebooks).




