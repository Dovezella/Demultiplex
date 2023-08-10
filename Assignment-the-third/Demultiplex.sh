#!/bin/bash
#SBATCH --account=bgmp                    #REQUIRED: which account to use
#SBATCH --partition=compute               #REQUIRED: which partition to use
#SBATCH --job-name=Demultiplex   ### job name
#SBATCH --output=demux_%j.out   ### file in which to store job stdout
#SBATCH --error=demux_%j.err    ### file in which to store job stderr
#SBATCH --mem=16G          ### memory limit per node, in MB
#SBATCH --nodes=1               ### number of nodes to use
#SBATCH --cpus-per-task=4       ### number of cores for each task

conda activate bgmp_py311

f1=$1
f2=$2
f3=$3
f4=$4 
i=$5

/usr/bin/time -v ../Demux.py -f1 $f1 -f2 $f2 -f3 $f3 -f4 $f4 -i $i