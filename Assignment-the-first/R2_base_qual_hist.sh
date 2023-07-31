#!/bin/bash
#SBATCH --account=bgmp                    #REQUIRED: which account to use
#SBATCH --partition=compute               #REQUIRED: which partition to use
#SBATCH --job-name=base_qual_hist   ### job name
#SBATCH --output=qhist_%j.out   ### file in which to store job stdout
#SBATCH --error=qhist_%j.err    ### file in which to store job stderr
#SBATCH --mem=16G          ### memory limit per node, in MB
#SBATCH --nodes=1               ### number of nodes to use
#SBATCH --cpus-per-task=4       ### number of cores for each task

conda activate bgmp_py311

f2=$1    #if you want to run these in parts just comment out the correspoding files and apply $1 and so on to the appropriate file


/usr/bin/time -v ./baseq_hist.py -f $f2 -o R2 -bp 7

