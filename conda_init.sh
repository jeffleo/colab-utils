#!/usr/bin/env bash
# Download and initalize an up-to-date conda python 3.6 environment

# remove default python path
echo    "before this script run:\
        %env PYTHONPATH=\
        !echo $PYTHONPATH"

# add conda python packages to sys.path
echo "after this script run:\
import sys\
 _ = (sys.path.append("/usr/local/lib/python3.6/site-packages"))\
# !ls /usr/local/lib/python3.6/dist-packages"

set +xe

# download
deliminator="----------------------------------------------------------"
echo $deliminator
echo "DOWNLOAD miniconda 3-4.5.4 to /usr/local to be able to access all dependancies on Colab"
echo $deliminator
# install to /usr/local to be able to access all dependancies on Colab
MINICONDA_INSTALLER_SCRIPT=Miniconda3-4.5.4-Linux-x86_64.sh
MINICONDA_PREFIX=/usr/local
wget https://repo.continuum.io/miniconda/$MINICONDA_INSTALLER_SCRIPT || (echo "ERROR wget conda download script failed "; exit 1)
chmod +x $MINICONDA_INSTALLER_SCRIPT
./$MINICONDA_INSTALLER_SCRIPT -b -f -p $MINICONDA_PREFIX
conda --version || (echo "ERROR conda not downloaded";exit 1)

echo $deliminator
echo "UPDATE miniconda and maintain python 3.6"
echo $deliminator
conda install --channel defaults conda python=3.6 --yes
conda update --channel defaults --all --yes
conda --version

# start environment
echo $deliminator
echo "Create conda python 3.6 env"
echo $deliminator
conda create -n colab-env python=3.6 -y
source activate colab-env
echo $deliminator
conda env list