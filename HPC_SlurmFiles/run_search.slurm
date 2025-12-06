#!/bin/bash
#SBATCH --job-name=faiss_search
#SBATCH --output=../logs/faiss_search.out
#SBATCH --error=../logs/faiss_search.err
#SBATCH -p short-40core
#SBATCH --time=00:30:00
#SBATCH --mem=32G
#SBATCH --cpus-per-task=4

module load python/3.9.7

cd /gpfs/projects/AMS598/class2025/Shah_SakshiJanak/AMS560/560/scripts

python3 query_embed_and_search.py
