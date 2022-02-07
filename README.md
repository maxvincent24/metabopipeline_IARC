# Metabopipeline

This pipeline aims to analyse metabolomics data, from the raw files to statistical analysis.

The pipeline is divised in three parts :
- file conversion : using <code>msconvert</code> from Proteowizard tools, we can convert files from vendro format (.d) to open source format (.mzML).
- metaboigniter : using [metaboigniter](https://github.com/nf-core/metaboigniter) pipeline, we can preprocess the .mzML files to get the intensity peak table, identification, ...
- notebooks : in Jupyter notebooks, we can explore, process and analyse the output of metaboigniter, using python and R languages.


## 1 - Convert .d to .mzML files with dockerized msconvert

Corresponding [README](https://github.com/maxvincent24/metabopipeline/tree/main/msconvert).


## 2 - Run metaboigniter pipeline




## 3 - Jupyter notebooks to identify potential biomarkers






