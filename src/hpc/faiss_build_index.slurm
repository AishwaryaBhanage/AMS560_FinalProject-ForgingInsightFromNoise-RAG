#!/bin/bash
#SBATCH --job-name=faiss_index
#SBATCH --output=../logs/faiss_index.out
#SBATCH --error=../logs/faiss_index.err
#SBATCH -p short-40core
#SBATCH --time=02:00:00
#SBATCH --mem=32G
#SBATCH --cpus-per-task=4

module purge
module load python/3.9.7

# MAKE LOCAL SITE-PACKAGES VISIBLE
export PYTHONUSERBASE=/gpfs/home/sakshah/.local
export PYTHONPATH=$PYTHONUSERBASE/lib/python3.9/site-packages:$PYTHONPATH

cd /gpfs/projects/AMS598/class2025/Shah_SakshiJanak/AMS560/560/scripts

python3 faiss_build_index.py

