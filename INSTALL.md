**Contents**

- [Installation procedure using Conda](#installation-procedure-using-conda)
  - [creating a new environment (recommended)](#creating-a-new-environment-recommended)
  - [Install dependencies](#install-dependencies)
  - [Install materialslab package](#install-materialslab-package)
    - [from source](#from-source)
    - [from pypi (not yet implemented)](#from-pypi-not-yet-implemented)

#  Installation procedure using Conda

## creating a new environment (recommended)

This is the recommended method.

```bash
> conda create -n materialslab python=3
> conda activate materialslab 

```

Alternatively *if you are running low on space on a SSD * drive you can use the prefix option (**IMPORTANT:** read through the following [StackOverflow Question: how to specify new environment location for conda create](https://stackoverflow.com/questions/37926940/how-to-specify-new-environment-location-for-conda-create))


## Install dependencies

Activate the new conda environment and install the following:

```bash
> conda activate materialslab
> conda install opencv numpy scipy
> conda install matplotlib  pandas seaborn
> conda install ipython jupyter
> conda install openpyxl
```


## Install materialslab package 

### from source

Clone the repository from online to <hmu.materialslab.tools>.

Change directory into **<hmu.materialslab.tools>/pypkg/**

> cd ./pypkg

Install the package locally:

> python setup.py install

### from pypi (not yet implemented)

This will be simpler but not yet implemented

```bash
> pip install materialslab-whatevername
```
